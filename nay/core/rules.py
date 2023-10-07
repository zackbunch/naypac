from __future__ import annotations

from copy import deepcopy
from enum import Enum
from typing import Dict, List, Optional, Union


class When(Enum):
    """Holds different GitLab CI/CD `when` statements for Rules.

    This enum class defines possible values for the `when` parameter in GitLab CI/CD rules.

    Args:
        Enum (When): The base class for GitLab CI/CD `when` statements.

    Attributes:
        ALWAYS (str): The job should always run.
        DELAYED (str): The job should run after manual action.
        MANUAL (str): The job should run manually.
        NEVER (str): The job should never run.
        ON_FAILURE (str): The job should run on failure.
        ON_SUCCESS (str): The job should run on success.

    See Also:
        - GitLab CI/CD [when](https://docs.gitlab.com/ee/ci/yaml/#when) documentation
    """

    ALWAYS = "always"
    DELAYED = "delayed"
    MANUAL = "manual"
    NEVER = "never"
    ON_FAILURE = "on_failure"
    ON_SUCCESS = "on_success"


class Rule:
    """Represents a GitLab CI/CD rule.

    Rules are used to include or exclude jobs in Pipelines based on specific conditions.

    Args:
        if_statement (str, optional): The conditional expression for this rule. Default is None.
        when (When, optional): Specifies when the rule should be applied. Default is When.ON_SUCCESS.
        allow_failure (bool): Indicates whether the job associated with this rule can fail without affecting the pipeline. Default is False.
        changes (list of str, optional): List of file patterns to match changes against. Default is None.
        exists (list of str, optional): List of file patterns to check for the existence of files. Default is None.
        variables (dict, optional): Dictionary of custom variables to be used in the condition. Default is an empty dictionary.

    See Also:
        - GitLab CI/CD [Rules](https://docs.gitlab.com/ee/ci/yaml/#rules) documentation
    """

    def __init__(
        self,
        *,
        if_statement: Optional[str] = None,
        when: When = When.ON_SUCCESS,
        allow_failure: bool = False,
        changes: Optional[List[str]] = None,
        exists: Optional[List[str]] = None,
        variables: Optional[Dict[str, str]] = None,
    ) -> None:
        self._if = if_statement
        self._changes = changes
        self._when = when
        self._exists = exists
        self._allow_failure = allow_failure
        self._variables = variables if variables is not None else {}

    def never(self) -> Rule:
        """Returns a copy of this rule with the `when` attribute set to `When.NEVER`.

        This method is intended to be used for predefined rules. For instance, you have defined an
        often-used rule `on_main` whose if statement checks if the pipeline is executed on branch
        `main`. Then you can either run a job if on main...

        ```
        my_job.append_rules(on_main)
        ```

        ... or do not run a job if on main...

        ```
        my_job.append_rules(on_main.never())
        ```

        Returns:
            Rule: A new rule object with `when` set to `When.NEVER`.
        """
        rule_copy = deepcopy(self)
        rule_copy._when = When.NEVER
        return rule_copy

    def add_variables(self, **variables: str) -> Rule:
        """Adds one or more variables to the rule.

        Args:
            **variables (str): Each variable is provided as a keyword argument:
            ```
            rule.add_variables(GREETING="hello", LANGUAGE="python")
            ```

        Returns:
            Rule: The modified Rule object.
        """
        self._variables.update(variables)
        return self

    def _equals(self, rule: Optional[Rule]) -> bool:
        """Check if this rule equals another rule.

        Args:
            rule (Rule, optional): The other rule to compare to.

        Returns:
            bool: True if self equals `rule`.
        """
        if not rule:
            return False

        return self.render() == rule.render()

    def render(self) -> Dict[str, Union[str, bool, List[str], Dict[str, str]]]:
        """Return a representation of this Rule object as a dictionary with static values.

        The rendered representation is used by the GitLab CI/CD pipeline to dump it
        in YAML format as part of the .gitlab-ci.yml file.

        Returns:
            Dict[str, Union[str, bool, List[str], Dict[str, str]]]: A dictionary representing the rule object in GitLab CI.
        """
        rendered_rule: Dict[str, Union[str, bool, List[str], Dict[str, str]]] = {}
        if self._if:
            rendered_rule.update({"if": self._if})

        if self._changes:
            rendered_rule["changes"] = self._changes

        if self._exists:
            rendered_rule["exists"] = self._exists

        if self._variables:
            rendered_rule["variables"] = self._variables

        rendered_rule.update(
            {
                "when": self._when.value,
                "allow_failure": self._allow_failure,
            }
        )
        return rendered_rule
