"""
Model of GitLab CI [rules](https://docs.gitlab.com/ee/ci/yaml/#rules)
"""
from __future__ import annotations

from enum import Enum


class When(Enum):
    """Holds different [when](https://docs.gitlab.com/ee/ci/yaml/#when)
    statements for Rules

    Args:
        Enum (When): statements for Rules
    """

    ALWAYS = "always"
    DELAYED = "delayed"
    MANUAL = "manual"
    NEVER = "never"
    ON_FAILURE = "on_failure"
    ON_SUCCESS = "on_success"


class Rule:
    """Represents a [rule](https://docs.gitlab.com/ee/ci/yaml/#rules)

    Rules are used to include or exclude jobs in Pipelines
    """

    pass
