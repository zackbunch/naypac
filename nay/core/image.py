from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Optional, Union


@dataclass
class Image:
    """Represents the [Image](https://docs.gitlab.com/ee/ci/yaml/#image) keyword.

    Use `Image` to specify a Docker image for the `nay.core.job.Job`.

    Objects of this class are typically defined centrally and re-used to maintain consistency. Avoid altering
    instances of this class, as it may lead to unpredictable changes in other references. Instead, use the
    `.with_tag()` and `.with_entrypoint()` methods to create modified copies for specific use cases.

    Args:
        name (str): The fully qualified image name, including the repository and tag.
        tag (Optional[str]): Container image tag in the registry to use.
        entrypoint (Optional[List[str]]): Overrides the container's entrypoint. Defaults to None.
    """

    name: str
    tag: Optional[str] = None
    entrypoint: Optional[List[str]] = None

    def with_tag(self, tag: str) -> Image:
        """
        Returns a copy of that image with an altered tag.
        You can still use the original Image object with its original tag.
        """
        copy = deepcopy(self)
        copy.tag = tag
        return copy

    def with_entrypoint(self, *entrypoint: str) -> Image:
        """
        Returns a copy of that image with an altered entrypoint.
        You can still use the original Image object with its original entrypoint.
        """
        copy = deepcopy(self)
        copy.entrypoint = list(entrypoint)
        return copy

    def render(self) -> Dict[str, Union[str, List[str]]]:
        """Return a representation of this Image object as a dictionary with static values.

        The rendered representation is used by Nay to dump it
        in YAML format as part of the .gitlab-ci.yml pipeline.

        Returns:
            Dict[str, Union[str, List[str]]]: A dictionary representing the image object in Gitlab CI.
        """
        rendered: Dict[str, Union[str, List[str]]] = {}

        rendered["name"] = self.name + (f":{self.tag}" if self.tag else "")

        if self.entrypoint:
            rendered["entrypoint"] = self.entrypoint

        return rendered

    def _equals(self, image: Optional[Image]) -> bool:
        """
        Returns:
            bool: True if self equals `image`.
        """
        if not image:
            return False

        return self.render() == image.render()
