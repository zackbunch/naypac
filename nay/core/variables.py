import os
from typing import Any, Optional


class EnvProxy:
    """The EnvProxy class defers the retrieval of environment variables until their values are requested.

    In a Gitlab CI pipeline execution, predefined environment variables like `CI_COMMIT_REF_SLUG`
    are expected to be available. To optimize performance and only retrieve these values when needed,
    we use the EnvProxy class.

    Here's how you can use EnvProxy to retrieve the value of a Gitlab `CI_*` variable:

    ```python
    CI_COMMIT_REF_SLUG = EnvProxy("CI_COMMIT_REF_SLUG")
    ...
    ```

    When you use an EnvProxy object in a statement, it will return the value of the corresponding `CI_*` variable
    if it's available. If the variable is not found (which shouldn't happen in a Gitlab CI pipeline), it will raise
    a `KeyError`.

    ```python
    ...
    if CI_COMMIT_REF_SLUG == "foobar":  # Value is retrieved only when needed
        ...
    ```

    However, the behavior of the proxy is different when it's not used within a Gitlab CI pipeline execution. In such
    cases, when the `CI` environment variable is unset (as per the official Gitlab CI documentation), the proxy will
    not raise a KeyError for `CI_*` variables. Instead, it will return the dummy string `notRunningInAPipeline` for all
    `CI_*` variables, except for the `CI` variable itself, where an empty string is returned to indicate that we are not
    running within a pipeline.

    Args:
        key (str): The name of the environment variable to query when its value is requested.
    """

    def __init__(self, key: str) -> None:
        self._key = key

    def __get__(self, obj: Any, objtype: Any = None) -> str:
        if os.getenv("CI"):  # When running within a Gitlab CI pipeline
            return os.environ[self._key]

        # Indicate that we are not running within a pipeline by
        # returning an empty string
        if self._key == "CI":
            return ""

        # In the case we are not running within a pipeline ($CI is empty)
        # for all other variables, we return a dummy value which
        # explicitly describes this state
        return os.getenv(self._key, "notRunningInAPipeline")


class OptionalEnvProxy:
    """This class represents an optional environment variable.

    It returns `os.getenv(<key>)` on the key given in the `__init__()` method.

    The class can be used in every expression where the `Optional[str]` of `os.getenv()` is expected:

    ```
    myvar = OptionalEnvProxy("MY_ENVIRONMENT_VARIABLE")
    ```

    The purpose of this class is to delay the execution of `os.getenv()`. In the upper example `myvar` is
    only set to this `OptionalEnvProxy` object. The value itself is retrieved with `os.getenv()` in the moment
    when `myvar` is used.
    """

    def __init__(self, key: str) -> None:
        self._key = key

    def __get__(self, obj: Any, objtype: Any = None) -> Optional[str]:
        return os.getenv(self._key)


class PredefinedVariables:
    """This class contains constants for [Gitlab CI predefined variables](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html)"""

    CHAT_CHANNEL: EnvProxy = EnvProxy("CHAT_CHANNEL")

    CI_PIPELINE_ID: EnvProxy = EnvProxy("CI_PIPELINE_ID")
    """
    The unique identifier of the current pipeline.

    Raises:
        KeyError: If environment variable not available.
    """
