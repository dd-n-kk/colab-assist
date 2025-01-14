__all__ = (
    "sync_gh",
    "reload",
    "install",
    "update_uv",
)


import importlib
import shlex
import subprocess
import sys
from getpass import getpass
from types import ModuleType

from google.colab import userdata

_uv_updated: bool = False


def sync_gh(
    owner: str,
    repo: str,
    branch: str | None = None,
    *,
    secret: str | None = None,
    auth: str | None = None,
    prompt: bool = True,
    timeout: int | None = 60,
) -> None:
    """Install or reinstall a package hosted in a GitHub repository with `uv`.

    - This function is mainly for (re)installing on Colab your in-development GitHub repository.
        Currently the supported authentication mechanism for a private repository
        is a [PAT (personal access token)](https://is.gd/qWZkuT).

    - Currently the recommended way to manage a PAT is via [Colab Secrets](
        https://stackoverflow.com/a/77737451).
        Use the Colab Secret by passing its key to `secret`.

    - You may also load your PAT into a variable in your preferred way,
        and then pass it to `auth`. Otherwise, by default a [`getpass`](
        https://docs.python.org/3/library/getpass.html)
        prompt will show up for you to paste your PAT.

    Args:
        owner: Name of the GitHub repository owner.

        repo: Name of the GitHub repository.

        branch: Name of the GitHub repository branch to install from.

            - `None`: Use the repository's default branch.

        secret: Colab Secrets key to your GitHub authentication info.

            - If `secret` is provided, `auth` and `prompt` are ignored.

        auth: Your GitHub authentication info.

            - If `auth` is provided, `prompt` is ignored.
            - Explicitly providing the authentication info as a string literal is discouraged.

        prompt: Option to prompt for your GitHub authentication info.

            - `True`: When neither `secret` nor `auth` is provided,
                a `getpass` prompt for your GitHub authentication info will show up.
            - `False`: When neither `secret` nor `auth` is provided, this function simply proceeds
                with the assumption that the GitHub repository does not require authentication.

        timeout: Timeout in seconds for the spawned subprocess.

            - `None`: No timeout.

    Examples:
        ```py
        import colab_utils as U
        U.sync_gh("me", "my_private_repo", "dev", secret="my_secret_key")
        ```
    """

    update_uv()

    if secret:
        try:
            auth = userdata.get(secret)
        except (userdata.NotebookAccessError, userdata.SecretNotFoundError) as err:
            print(err)
            return
    elif not auth and prompt:
        auth = getpass("Authentication (or enter nothing to skip): ")

    prefix = f"git+https://{auth}@github.com/" if auth else "git+https://github.com/"
    suffix = f"{owner}/{repo}@{branch}" if branch else f"{owner}/{repo}"
    try:
        result = subprocess.run(
            ("uv", "pip", "install", "--system", "-Uq", shlex.quote(f"{prefix}{suffix}")),
            capture_output=True,
            encoding="utf-8",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        print(exc)
    else:
        if result.returncode != 0:
            print(result.stderr, end="")


def reload(obj: object) -> object:
    """Reimport a module, function, or class.

    - This function internally uses [`importlib.reload()`](
        https://docs.python.org/3/library/importlib.html#importlib.reload)
        to reimport modules, and [`getattr()`](
        https://docs.python.org/3/library/functions.html#getattr)
        to retrieve attributes from reimported modules.
        So the limitations and caveats of `importlib.reload()` persist. In particular:

        - Reloading a module does _not_ automatically reload its parent modules or submodules.
        - Names defined in the old version of the module but not in the new version
            (e.g. when an attribute is removed in an update) are _not_ automatically deleted.
        - This function can correctly reload a non-module object
            only if the object has valid `__name__` and `__module__` attributes.
            So, usually, functions and classes are the only directly reloadable non-modules.
            However, after a module is reimported,
            its non-module attributes can be updated via `import` statements.
        - Reloading a class does _not_ affect previously created instances.
        - To properly reload a non-module, the return value must be captured.
            It is recommended to always use the `xxx = reload(xxx)` pattern.

    - This function should mainly be used on modules, functions, or classes in your package
        after an updated version is reinstalled, and only when the changes are localized enough
        that restarting the Colab session is overkill.

    Args:
        obj: Object to reload. Usually should be a module, function, or class.

    Returns:
        The reloaded object if reloading is successful.
            Otherwise, the original object is returned as is.

    Examples:
        ```py
        import colab_utils as U
        from my_pkg import my_func, MyClass

        # ... (Behavior before update)

        # (Update made to the source code of `my_pkg` on GitHub)
        U.sync_gh("my_name", "my_pkg")

        my_func = U.reload(my_func)
        MyClass = U.reload(MyClass)
        my_obj = MyClass()

        # ... (Updated behavior)
        ```
    """

    if (name := getattr(obj, "__name__", None)) is None:
        print(f"Failed to reload {obj}: Missing attribute `__name__`.")
        return obj

    if isinstance(obj, ModuleType):  # [inspect.ismodule()](https://is.gd/7slO1C)
        if name == "__main__":
            print(f"Failed to reload {obj}: Cannot reload top-level module.")
            return obj
        return importlib.reload(obj)

    if (module_name := getattr(obj, "__module__", None)) is None:
        print(f"Failed to reload {obj}: Failed to determine the object's module.")
        return obj

    if module_name == "__main__":
        print(f"Failed to reload {obj}: Cannot reload objects defined at top level.")
        return obj

    return getattr(importlib.reload(sys.modules[module_name]), name)


def install(*packages: str, timeout: int | None = 180) -> None:
    """Install or update package(s) with `uv`.

    - This function wraps around the `uv pip install --system` command,
        which works well in the Colab environment.

    Args:
        packages: Specification(s) of the package(s) to install or update.

            - See [`uv` docs](https://docs.astral.sh/uv/pip/packages/#installing-a-package)
                for ways to specify packages.

        timeout: Timeout in seconds for the spawned subprocess.

            - `None`: No timeout.

    Examples:
        ```py
        import colab_utils as U
        U.install('polars')
        U.install('numpy==2.2.0', 'scipy', timeout=None)
        ```
    """

    update_uv()

    if not packages:
        return

    packages = tuple(shlex.quote(package) for package in packages)
    try:
        result = subprocess.run(
            shlex.split(f"uv pip install --system -q {' '.join(packages)}"),
            capture_output=True,
            encoding="utf-8",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        print(exc)
    else:
        if result.returncode != 0:
            print(result.stderr, end="")


def update_uv() -> None:
    """Update the `uv` package pre-installed on Colab.

    - This function tries to run only once by setting a global flag.
    """

    global _uv_updated
    if _uv_updated:
        return

    try:
        result = subprocess.run(
            ("uv", "pip", "install", "--system", "-q", "uv"),
            capture_output=True,
            encoding="utf-8",
            timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        print(exc)
    else:
        if result.returncode != 0:
            print(result.stderr, end="")
        else:
            _uv_updated = True
