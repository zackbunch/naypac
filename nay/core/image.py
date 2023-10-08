from __future__ import annotations

from copy import deepcopy
from typing import Dict, List, Union, Optional
from dataclasses import dataclass


@dataclass
class Image:
    """This class represents the Nay [Image](https://docs.gitlab.com/ee/ci/yaml/#image) keyword.

    Use `Image` to specify a Docker image to use for the `nay.core.job.Job`.

    Objects of this class are not meant to be altered. Image objects are typically defined
    centrally and often re-used. Altering the object at one place may lead to unpredictable changes
    at any reference to that object. That's why this class has no setter methods. However, you can use the
    `.with_tag()` and `.with_entrypoint()` methods on an Image object, which will return an altered copy
    of that image. Thus, you can re-use a centrally maintained Image object and modify it for just the
    place you are using the altered image (copy).

    Args:
        name (str): The fully qualified image name. Could include the repository and tag as usual.
        tag (Optional[str]): Container image tag in the registry to use.
        entrypoint (Optional[List[str]]): Overwrites the container's entrypoint. Defaults to None.
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
