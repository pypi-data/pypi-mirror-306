from typing import Any, Dict, Literal, Optional

__all__ = [
    "start",
]


def start(
    export: Optional[Dict[str, Any]] = None,
    shell: Optional[Literal["ipython", "code"]] = None,
) -> None:
    """
    Start the interactive shell.

    Parameters
    ---
        export : A dict of variables to be exported to the interactive shell.
    """
    try:
        if shell == "code":
            raise ImportError
        from IPython import start_ipython

        start_ipython(argv=[], user_ns=export, display_banner=False)
    except ImportError:
        if shell == "ipython":
            raise ImportError("IPython is not installed.")
        from code import interact

        interact(local=export, banner="")
