class ScriptArgumentNotAllowedError(Exception):
    """
    Exception raised when the 'script' argument is not allowed in the constructor.

    This exception is mainly used in subclasses of the 'Job' class, which define custom scripts,
    and allow arbitrary keyword arguments to be passed to the superclass constructor.
    In such cases, the 'script' argument should not be allowed to prevent conflicts.

    Attributes:
        message (str): A descriptive error message.
    """

    def __init__(self) -> None:
        """
        Initialize the exception with a message.
        """
        super().__init__(
            "The 'script' argument is not supported by this subclass of 'Job' because "
            "the class provides its custom script. You can prepend/append scripts as usual."
        )
