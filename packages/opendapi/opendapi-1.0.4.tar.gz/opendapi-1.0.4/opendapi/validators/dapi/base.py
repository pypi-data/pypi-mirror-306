"""DAPI validator module"""

import copy
from abc import abstractmethod
from collections import Counter
from functools import cached_property
from typing import Dict, List, Tuple

from opendapi.config import construct_project_full_path, get_project_path_from_full_path
from opendapi.defs import DAPI_SUFFIX, OPENDAPI_SPEC_URL, OpenDAPIEntity
from opendapi.models import ConfigParam, OverrideConfig, PlaybookConfig, ProjectConfig
from opendapi.utils import find_files_with_suffix, has_underlying_model_changed
from opendapi.validators.base import (
    BaseValidator,
    MultiValidationError,
    ValidationError,
)
from opendapi.validators.dapi.models import PackageScopedProjectInfo, ProjectInfo


class BaseDapiValidator(BaseValidator):
    """
    Abstract base validator class for DAPI files
    """

    INTEGRATION_NAME: str = NotImplementedError
    SUFFIX = DAPI_SUFFIX
    SPEC_VERSION = "0-0-1"
    ENTITY = OpenDAPIEntity.DAPI

    # Paths & keys to use for uniqueness check within a list of dicts when autoupdating
    AUTOUPDATE_UNIQUE_LOOKUP_KEYS: List[Tuple[List[str], str]] = [(["fields"], "name")]

    # Paths to disallow new entries when autoupdating
    AUTOUPDATE_DISALLOW_NEW_ENTRIES_PATH: List[List[str]] = [["fields"]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_field_names(self, content: dict) -> List[str]:
        """Get the field names"""
        return [field["name"] for field in content["fields"]]

    def _validate_primary_key_is_a_valid_field(self, file: str, content: Dict):
        """Validate if the primary key is a valid field"""
        primary_key = content.get("primary_key") or []
        field_names = self._get_field_names(content)
        for key in primary_key:
            if key not in field_names:
                raise ValidationError(
                    f"Primary key element '{key}' not a valid field in '{file}'"
                )

    def _validate_field_data_subjects_and_categories_unique(
        self, file: str, content: Dict
    ):
        """Validate if the field data subjects and categories are unique"""
        errors = []
        for field in content.get("fields", []):
            data_subjects_and_categories_counts = Counter(
                (subj_and_cat["subject_urn"], subj_and_cat["category_urn"])
                for subj_and_cat in field.get("data_subjects_and_categories", [])
            )
            non_unique_data_subjects_and_categories = {
                subj_and_cat
                for subj_and_cat, count in data_subjects_and_categories_counts.items()
                if count > 1
            }
            if non_unique_data_subjects_and_categories:
                errors.append(
                    (
                        f"In file '{file}', the following 'data_subjects_and_categories' pairs are "
                        f"repeated in field '{field['name']}': "
                        f"{non_unique_data_subjects_and_categories}"
                    )
                )
        if errors:
            raise MultiValidationError(
                errors, "Non-unique data subjects and categories pairs within fields"
            )

    def _is_personal_data_is_direct_identifier_matched(self, file: str, content: dict):
        """Validate that you cannot have a direct identifier without it also being personal data"""

        errors = []
        for field in content.get("fields", []):
            if field.get("is_direct_identifier") and not field.get("is_personal_data"):
                errors.append(
                    f"Field '{field['name']}' in file '{file}' is a direct identifier "
                    "but not marked as personal data"
                )

        if errors:
            raise MultiValidationError(
                errors,
                f"Mismatched personal data designations for mappings in '{file}'",
            )

    @cached_property
    def settings(self) -> ProjectConfig:
        """Get the settings from the config file for this integration"""
        settings = copy.deepcopy(
            self.config.get_integration_settings(self.INTEGRATION_NAME)
        )

        override_config = settings.get(ConfigParam.PROJECTS.value, {}).get(
            ConfigParam.OVERRIDES.value, []
        )

        overrides = []
        for override in override_config:
            playbooks = [
                PlaybookConfig.from_dict(playbook)
                for playbook in override.get(ConfigParam.PLAYBOOKS.value, [])
            ]
            override[ConfigParam.PLAYBOOKS.value] = playbooks
            overrides.append(OverrideConfig.from_dict(override))

        settings[ConfigParam.PROJECTS.value][ConfigParam.OVERRIDES.value] = overrides

        return ProjectConfig.from_dict(settings[ConfigParam.PROJECTS.value])

    def validate_content(self, file: str, content: Dict):
        """Validate the content of the files"""
        self._validate_primary_key_is_a_valid_field(file, content)
        self._validate_field_data_subjects_and_categories_unique(file, content)
        self._is_personal_data_is_direct_identifier_matched(file, content)
        super().validate_content(file, content)

    def base_dir_for_autoupdate(self) -> str:
        return self.root_dir

    def base_template_for_autoupdate(self) -> Dict[str, Dict]:
        """Set Autoupdate templates in {file_path: content} format"""
        return {
            f"{self.base_dir_for_autoupdate()}/sample_dataset.dapi.yaml": {
                "schema": OPENDAPI_SPEC_URL.format(
                    version=self.SPEC_VERSION, entity="dapi"
                ),
                "urn": "my_company.sample.dataset",
                "type": "entity",
                "description": "Sample dataset that shows how DAPI is created",
                "owner_team_urn": "my_company.sample.team",
                "datastores": {
                    "sources": [
                        {
                            "urn": "my_company.sample.datastore_1",
                            "data": {
                                "identifier": "sample_dataset",
                                "namespace": "sample_db.sample_schema",
                            },
                        }
                    ],
                    "sinks": [
                        {
                            "urn": "my_company.sample.datastore_2",
                            "data": {
                                "identifier": "sample_dataset",
                                "namespace": "sample_db.sample_schema",
                            },
                        }
                    ],
                },
                "fields": [
                    {
                        "name": "field1",
                        "data_type": "string",
                        "description": "Sample field 1 in the sample dataset",
                        "is_nullable": False,
                        "is_pii": False,
                        "access": "public",
                        "data_subjects_and_categories": [],
                        "sensitivity_level": None,
                        "is_personal_data": None,
                        "is_direct_identifier": None,
                    }
                ],
                "primary_key": ["field1"],
                "context": {
                    "integration": "custom_dapi",
                },
            }
        }

    def skip_autoupdate(  # pylint: disable=unused-argument
        self, new_content: Dict, current_content: Dict, filepath: str
    ) -> bool:
        """
        Skip autoupdate if there is no material change to the model

        This is necessary for organic onboarding, since otherwise features being on will
        always lead to Dapis being autoupdated, since more will be returned from
        base_template_for_autoupdate, and the content will have changed, regardless of if
        the model was updated organically

        NOTE: To work properly, needs base_commit_files - otherwise the fallback is to always
              autoupdate, which is safest, but noisiest
        """
        if base_content := self.base_commit_files.get(filepath):
            return not (
                has_underlying_model_changed(new_content, base_content)
                # if someone manually edited the dapi to remove fields,
                # the base file may say no change while the current file has changes.
                # therefore, check both
                or has_underlying_model_changed(new_content, current_content)
            )
        return False


class DapiValidator(BaseDapiValidator):
    """
    Abstract validator class for DAPI files
    """

    def selected_projects(self, validate: bool = True) -> List[ProjectInfo]:
        """Get the selected projects"""
        projects = {}

        if self.settings.include_all:
            for project in self.get_all_projects():
                projects[project.full_path] = project

        for override in self.settings.overrides:
            project = self.get_project(override)
            projects[project.full_path] = project

        projects = list(projects.values())

        if validate:
            self.validate_projects(projects)

        return projects

    @abstractmethod
    def get_all_projects(self) -> List[ProjectInfo]:
        """Generate a list of all projects that this validator should check"""

    @abstractmethod
    def get_project(self, override_config: OverrideConfig) -> ProjectInfo:
        """Given a project override config, return an ProjectConfig object"""

    @abstractmethod
    def validate_projects(self, projects: List[ProjectInfo]):
        """Validate the projects"""


class PackageScopedDapiValidatorBase(BaseDapiValidator):
    """Base class for DAPI validators that are scoped to packages."""

    PACKAGE_JSON: str = "package.json"
    LOOKUP_FILE_SUFFIXES: List[str] = NotImplementedError

    def get_all_projects(self) -> List[PackageScopedProjectInfo]:
        """Get all package.json files in the project."""
        package_file = f"/{self.settings.artifact_path or self.PACKAGE_JSON}"
        files = find_files_with_suffix(self.root_dir, [package_file])
        packages = [filename.replace(package_file, "") for filename in files]

        if self.settings.include_all:
            projects = [
                PackageScopedProjectInfo(
                    org_name_snakecase=self.config.org_name_snakecase,
                    override=OverrideConfig(
                        project_path=get_project_path_from_full_path(
                            self.root_dir, package
                        )
                    ),
                    root_path=self.root_dir,
                    full_path=package,
                )
                for package in packages
            ]
        else:
            projects = []

        for override in self.settings.overrides:
            full_path = construct_project_full_path(
                self.root_dir, override.project_path
            )
            if full_path not in packages:
                continue

            project = PackageScopedProjectInfo(
                org_name_snakecase=self.config.org_name_snakecase,
                override=override,
                root_path=self.root_dir,
                full_path=construct_project_full_path(
                    self.root_dir, override.project_path
                ),
            )
            projects.append(project)

        # Update the file contents in the projects
        for project in projects:
            pkg_files = find_files_with_suffix(
                project.full_path, self.LOOKUP_FILE_SUFFIXES
            )
            for filename in pkg_files:
                with open(filename, encoding="utf-8") as f:
                    project.file_contents[filename] = f.read()

        return projects
