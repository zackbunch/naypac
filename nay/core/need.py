from __future__ import annotations

from typing import Dict, Optional, Union

from nay.core.variables import PredefinedVariables


class Need:
    """Represents the GitLab CI [needs](https://docs.gitlab.com/ee/ci/yaml/#needs) keyword.


    Args:
        job (str, optional): The name of the job to depend on. Must be provided if `pipeline` is not set. Defaults to None.
        project (str, optional): The name of the project if the `job` resides in another pipeline. Defaults to None.
        ref (str, optional): The branch of the remote project to depend on. Defaults to None.
        pipeline (str, optional): The CI_PIPELINE_ID of another pipeline to depend on, or the name of another project
            to mirror the status of an upstream pipeline. Must be provided if `job` is not set. Defaults to None.
        artifacts (bool): Whether to download artifacts from the `job` to depend on. Defaults to True.

    Raises:
        ValueError: If neither `job` nor `pipeline` is set.
        ValueError: If `ref` is set but `project` is missing.
        ValueError: If `pipeline` equals the CI_PIPELINE_ID of the own project.
        ValueError: If both `project` and `pipeline` are set.
    """

    def __init__(
        self,
        job: Optional[str] = None,
        *,
        project: Optional[str] = None,
        ref: Optional[str] = None,
        pipeline: Optional[str] = None,
        artifacts: bool = True,
    ):
        if not job and not pipeline:
            raise ValueError("At least one of `job` or `pipeline` must be set.")

        if ref and not project:
            raise ValueError("'ref' parameter requires the 'project' parameter.")

        if project and pipeline:
            raise ValueError(
                "Needs accepts either `project` or `pipeline` but not both."
            )

        if pipeline and pipeline == PredefinedVariables.CI_PIPELINE_ID:
            raise ValueError(
                "The pipeline attribute does not accept the current pipeline ($CI_PIPELINE_ID). "
                "To download artifacts from a job in the current pipeline, use the basic form of needs."
            )

        self._job = job
        self._project = project
        self._ref = ref
        self._artifacts = artifacts
        self._pipeline = pipeline

        if self._project and not self._ref:
            self._ref = "main"

    def render(self) -> Dict[str, Union[str, bool]]:
        """Return a representation of this Need object as dictionary with static values.

        The rendered representation is used by the gcip to dump it
        in YAML format as part of the .gitlab-ci.yml pipeline.

        Returns:
            Dict[str, Any]: A dictionary representing the need object in Gitlab CI.
        """

        rendered_need: Dict[str, Union[str, bool]] = {}

        if self._job:
            rendered_need.update(
                {
                    "job": self._job,
                    "artifacts": self._artifacts,
                }
            )

        if self._project and self._ref:
            rendered_need.update({"project": self._project, "ref": self._ref})

        if self._pipeline:
            rendered_need["pipeline"] = self._pipeline

        return rendered_need

    def _equals(self, need: Optional[Need]) -> bool:
        """
        Returns:
            bool: True if self equals to `need`.
        """
        if not need:
            return False

        return self.render() == need.render()
