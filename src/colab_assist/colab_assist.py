__all__ = (
    "install",
    "update",
    "reinstall",
    "clone_gh",
    "pull_gh",
    "reload",
    "edit",
    "download",
    "restart",
    "mount",
    "unmount",
    "end",
    "update_git",
)


import importlib
import os
import re
import shutil
import subprocess
import sys
from email.message import EmailMessage
from getpass import getpass
from itertools import chain
from shlex import split
from types import ModuleType
from urllib.parse import urlparse

import requests
from IPython.core.getipython import get_ipython
from tqdm.auto import tqdm

from colab_assist import _colab

_COLAB_ROOT = "/content/"
_DRIVE_MNTPT = "/content/drive/"
_DRIVE_ROOT = "/content/drive/MyDrive/"
_REPOS_ROOT = "/content/repos/"
_HOST_NAMES = {"gh": "github.com", "gl": "gitlab.com", "bb": "bitbucket.org"}


def install(*packages: str, o: str = "", timeout: int | None = 60) -> None:
    """Install package(s) using uv.

    - This function is a convenience interface of the uv command
        `uv pip install --system ⟨o⟩ -- ⟨packages⟩`.
        See also its convenience aliases [`update()`][colab_assist.update]
        and [`reinstall()`][colab_assist.reinstall].

    Args:
        packages: Specifiers of the packages to install.
            In addition to the uv-supported [package specifiers](
            https://docs.astral.sh/uv/pip/packages/#installing-a-package), colab-assist provides
            a shorthand for installing packages in remote Git repositories via HTTP:
            ```
            [⟨auth⟩@][⟨host⟩/]⟨owner⟩/⟨repo⟩[@⟨ref⟩]
            ```
            - `⟨auth⟩` is optional authorization info for a private repository,
                such as a [GitHub personal access token (PAT)](
                https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

                - If `⟨auth⟩` is `$`, an input prompt for authorization info will spawn.

                - If `⟨auth⟩` is prefixed with `$`, the part after `$` is treated as
                    the name of a [Colab Secret](https://stackoverflow.com/a/77737451)
                    containing the authorization info. Currently this is the recommended way
                    of managing private info on Colab.

                - Otherwise, `⟨auth⟩` is assumed to be the authorization info proper.

            - `⟨host⟩` is an optional specification of the remote repository host.

                - If `⟨host⟩` is not provided, `github.com` is used as the host domain name.

                - If `⟨host⟩` is prefixed with `$`, it is treated as an abbreviation tag:
                    - `$gh` for `github.com`.
                    - `$gl` for `gitlab.com`.
                    - `$bb` for `bitbucket.org`.

                - Otherwise `⟨host⟩` is assumed to be a host domain name.

            - `⟨owner⟩/⟨repo⟩` is the required identifier of the remote repository.

            - `⟨ref⟩` is an optional specification of a branch, a tag, or a commit.

        o: Additional [options](https://docs.astral.sh/uv/reference/cli/#uv-pip-install)
            for the `uv pip install` command.

        timeout: Timeout in seconds for the spawned subprocess.

            - `None`: No timeout.

    Examples:
        ```py
        import colab_assist as A

        # Install the latest versions of DuckDB and Polars.
        A.install("duckdb", "polars", o="-U")

        # Use the PAT stored in the Colab Secret named `my-token` to install the Python package
        # hosted in the `feat/foo` branch of the private GitHub repository `me/my-repo`.
        A.install("$my-token@me/my-repo@feat/foo")
        ```
    """
    if not packages:
        return

    try:
        result = subprocess.run(
            tuple(
                chain(
                    ("uv", "pip", "install", "--system"),
                    split(o),
                    ("--",),
                    (_parse_package_spec(p) for p in packages),
                )
            ),
            capture_output=True,
            encoding="utf-8",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        print(exc)
    else:
        if result.returncode != 0:
            print(result.stderr, end="")


def update(*packages: str, o: str = "", timeout: int | None = 60) -> None:
    """Update package(s) and dependencies using uv.

    - This is a convenience alias of [`install()`][colab_assist.install]
        with `--upgrade` included in `o`.
        The command `uv pip install` used by `install()` is relatively conservative by default:
        Already installed packages will not be updated unless an update is required to
        satisfy an explicit version restriction or to resolve an incompatibility.
        With `--upgrade`, uv will always try to update the packages and their dependencies
        to the latest versions, but this also increases the risk of breaking the Colab environment.
    """
    install(*packages, o="-U " + o, timeout=timeout)


def reinstall(*packages: str, o: str = "", timeout: int | None = 60) -> None:
    """Reinstall package(s) and dependencies using uv.

    - This is a convenience alias of [`install()`][colab_assist.install]
        with `--reinstall` included in `o`.
        `--reinstall` is more drastic than [`--upgrade`][colab_assist.update]:
        It forces reinstalling packages and all dependencies even if they are already
        the latest versions. However, according to the [uv documentation](
        https://docs.astral.sh/uv/concepts/projects/init/#projects-with-extension-modules),
        `--reinstall` is required for changes in non-Python extension code to take effect.
    """
    install(*packages, o="--reinstall " + o, timeout=timeout)


def clone_gh(
    repo: str,
    branch: str | None = None,
    *,
    opt: str = "",
    dir_name: str | None = None,
    auth: str | None = None,
    secret: str | None = None,
    timeout: int | None = 60,
) -> None:
    """Clone a GitHub repository and optionally make it importable if it is a Python package.

    - See [`install_gh()`][colab_assist.install_gh] for details on GitHub authentication.

    - By default, this function just clones the GitHub repository into a subdirectory
        in `/content/repos/`.
        If you are cloning a Python package, automatic actions to make the package importable
        can be enabled with some options in `opt`.

    Args:
        repo: Identifier of the GitHub repository, in the form `⟨owner⟩/⟨repo_name⟩`.

        branch: Name of the branch to clone from.

            - `None`: Clone the history of all branches and use the default branch.

        opt: A string as an order-agnostic set of single-letter option flags.
            An option is enabled if and only if its corresponding letter is in the string.

            - `p` for _path_:
                This option shadows, and should not be used together with, `e`.
                This option assumes that the GitHub repository hosts a Python package,
                and will add the top-level module directory of the clone to `sys.path`.
                This allows importing the package without installing it,
                which may be useful when the many packages pre-installed on Colab
                cause distracting dependency issues.

                Notable implications include:

                - The cloned package is immediately importable without needing a session restart.
                - Changes in the clone (e.g. by [`pull_gh()`][colab_assist.pull_gh])
                    can take effect via [`reload()`][colab_assist.reload];
                    a session restart is not mandatory.
                - If a Colab session restart is triggered by [`restart()`][colab_assist.restart],
                    `colab_assist` module will try to recover `sys.path` upon the next import.
                    But otherwise you will need to manually re-add the top-module directory
                    to `sys.path` after a session restart.

            - `e` for _editable_:
                This option is shadowed by, and should not be used together with, `p`.
                This option assumes that the GitHub repository hosts a Python package,
                and will install the clone in [editable/development mode](
                https://setuptools.pypa.io/en/latest/userguide/development_mode.html).

                Notable implications include:

                - Currently an editable install seems to require a session restart to take effect.
                - But after the installation, changes in the clone can take effect
                    via [`reload()`][colab_assist.reload]; a session restart is not mandatory.
                - Unlike `sys.path`, editable install is not reset by session restarts.

            - `q` for _quiet_:
                Suppress the skippable prompt for GitHub authentication info
                when neither `auth` nor `secret` is provided.
                The function will then assume GitHub authentication is not required.

        dir_name: Directory name of the clone.

            - `None`: Use the repository name.

        auth: Your GitHub authentication info.

            - If `auth` is provided, `secret` is ignored.

        secret: Name of the Colab Secret storing your GitHub authentication info.

        timeout: Timeout in seconds for the spawned subprocess.

            - `None`: No timeout.

    Examples:
        ```py
        import colab_assist as A
        A.clone_gh("me/my_public_repo", opt="eq")
        ```
    """

    owner, repo = repo.split("/")
    repo_path = os.path.join(_REPOS_ROOT, dir_name or repo)
    if os.path.exists(repo_path):
        print(f"{repo_path} already exists. Consider `pull_gh('{dir_name or repo}')` instead?")
        return

    if auth := auth or _get_auth(secret, "q" not in opt):
        url = shlex.quote(f"https://{auth}@github.com/{owner}/{repo}.git")
    else:
        url = shlex.quote(f"https://github.com/{owner}/{repo}.git")

    if branch:
        cmd = f"git clone --single-branch -b {branch} -- {url} {shlex.quote(repo_path)}"
    else:
        cmd = f"git clone -- {url} {shlex.quote(repo_path)}"
    try:
        result = subprocess.run(
            shlex.split(cmd),
            capture_output=True,
            encoding="utf-8",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        print(exc)
        return

    if result.returncode != 0:
        print(result.stderr, end="")
        return

    if "p" in opt:
        if os.path.isdir(src_path := os.path.join(repo_path, "src")):
            sys.path.append(src_path)
            _colab._sys_path_extensions.append(src_path)
        else:
            sys.path.append(repo_path)
            _colab._sys_path_extensions.append(repo_path)
        return

    if "e" in opt:
        _install_editable(repo_path)
        return


def pull_gh(dir_name: str, timeout: int | None = 60) -> None:
    """Pull from the GitHub repository.

    Args:
        dir_name: Basename of the repository in `/content/repos`.

        timeout: Timeout in seconds for the spawned subprocess.

            - `None`: No timeout.
    """

    repo_path = os.path.join(_REPOS_ROOT, dir_name)
    if not os.path.isdir(repo_path):
        print(f"{repo_path} does not exist or is not a directory.")
        return

    try:
        result = subprocess.run(
            ("git", "pull"),
            cwd=repo_path,
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
        for an update to take effect, and only when the changes are localized enough
        that restarting the Colab session is overkill.

    - See also [`%autoreload`](
        https://ipython.readthedocs.io/en/stable/config/extensions/autoreload.html)
        for automatically reloading multiple or all modules at once.

    Args:
        obj: Object to reload. Usually should be a module, function, or class.

    Returns:
        The reloaded object if reloading is successful.
            Otherwise, the original object is returned as is.

    Examples:
        ```py
        import colab_assist as A
        from my_pkg import my_func, MyClass

        # ... (Behavior before update)

        # (Update made to the source code of `my_pkg` on GitHub)
        A.install_gh("my_name", "my_pkg")

        my_func = A.reload(my_func)
        MyClass = A.reload(MyClass)
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


def edit(path: str, opt: str = "") -> None:
    """Open an editor tab for a file.

    - This function wraps `google.colab.files.view()`,
        which currently does not support editing certain file types, e.g. `.md`.

    Args:
        path: Path to the text file to edit.

        opt: A string as an order-agnostic set of single-letter option flags.
            An option is enabled if and only if its corresponding letter is in the string.

            - `c` for _create_:
                By default, `edit()` does not create a new file.
                This option creates a blank file (and all its parent directories if necessary)
                if `path` does not exist.
    """
    if not os.path.exists(path):
        if "c" in opt:
            if parent := os.path.dirname(path):
                os.makedirs(parent, exist_ok=True)
            open(path, "w").close()  # os.mknod() is not implemented for Google Drive.
        else:
            print(f"{path} does not exist.")
            return

    if os.path.isfile(path):
        _colab.files.view(path)
    else:
        print(f"{path} is not a file.")


def download(url: str, path: str | None = None, *, chunk_size: int = 131072) -> str | None:
    """Download a file from a URL.

    Args:
        url: URL of the file to download.

        path: Destination path of the downloaded file.

            - `None`: The file is saved in the current working directory
                and the file name is inferred from the response headers or the URL.

        chunk_size: Number of bytes read into memory while iterating over the response data.

            - This argument is passed directly to [`request.Response.iter_content()`](
                https://requests.readthedocs.io/en/latest/api/#requests.Response.iter_content).

    Returns:
        Absolute path of the downloaded file, or `None` if the download was not successful.
    """
    with requests.get(url, stream=True) as resp:
        if resp.status_code != 200:
            print(f"{url} responded with status {resp.status_code}:\n{_get_resp_reason(resp)}")
            return

        if path is None:
            if h := resp.headers.get("Content-Disposition"):
                em = EmailMessage()
                em["Content-Disposition"] = h
                path = f"{os.getcwd()}/{em.get_filename()}"
            elif filename := os.path.basename(urlparse(url).path):
                path = f"{os.getcwd()}/{filename}"
            else:
                print(f"Failed to infer file name from {url}. Please specify `path`.")
                return

        file_size = int(resp.headers.get("Content-Length", 0))
        with (
            open(path, "wb") as file,
            tqdm(
                total=file_size,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar,
        ):
            for chunk in resp.iter_content(chunk_size=chunk_size):
                bar.update(file.write(chunk))

    return path


def restart() -> None:
    """Trigger a Colab session restart after some bookkeeping operations.

    - Colab is expected to issue a notification: "Your session crashed for an unknown reason."
    - Explicitly restarting the Colab session, e.g., with this function,
        with `exit()`, or with the `Restart session` command in the Colab `Runtime` menu,
        resets all imports and variables in the Python interpreter session.
        However, as long as the runtime is not deleted, the installed packages,
        files in the virtual disk, and Google Drive (if mounted) are preserved.
        This function does some extra bookkeeping so that certain session states
        can be recovered upon importing `colab_assist` in the next session.
    """
    _colab._save_state()

    if (ishell := get_ipython()) is None:
        print("Global interactive shell not found. Try `exit()` or `Runtime -> Restart session`.")
    else:
        ishell.ask_exit()  # type: ignore


def mount(force: bool = False) -> None:
    """Mount Google Drive.

    Args:
        force: Option to force remounting if Google Drive is already mounted.
    """
    _colab.drive.mount(_DRIVE_MNTPT, force_remount=force)


def unmount() -> None:
    """Flush and unmount Google Drive."""
    _colab.drive.flush_and_unmount()


def end() -> None:
    """Terminate the Colab runtime after some cleanup operations."""
    _clear_repos()
    _colab.drive.flush_and_unmount()
    _colab.runtime.unassign()


def update_git(timeout: int | None = 90) -> None:
    """Update Git.

    - With the current implementation (using APT), the update process is relatively long (~30s).

    Args:
        timeout: Timeout in seconds for the spawned subprocess.

            - `None`: No timeout.
    """
    if _colab._git_updated:
        return

    try:
        result = subprocess.run(
            "add-apt-repository -y 'ppa:git-core/ppa' && apt-get -y install git",
            shell=True,  # For `&&`.
            capture_output=True,
            encoding="utf-8",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        print(exc)
    else:
        if result.returncode != 0:
            print(result.stderr, end="")
        else:
            _git_updated = True


def _clear_repos() -> None:
    shutil.rmtree(_REPOS_ROOT, ignore_errors=True)


def _get_auth(auth: str) -> str:
    if auth == "$":
        return getpass("Authentication (or enter nothing to skip): ")

    if auth.startswith("$"):
        return _colab.userdata.get(auth[1:])

    return auth


def _get_resp_reason(resp: requests.Response) -> str:
    reason = resp.reason
    if isinstance(reason, bytes):
        try:
            reason = reason.decode("utf-8")
        except UnicodeDecodeError:
            reason = reason.decode("iso-8859-1", errors="backslashreplace")

    return reason if reason else "Reason not provided"


def _parse_package_spec(spec: str) -> str:
    pattern = (
        r"(?:(\$?[-%+.:\w]*)@)?"  # auth
        r"(?:\$(gh|gl|bb)/|([-a-zA-Z0-9]+\.[-.a-zA-Z0-9]+)/)?"  # host
        r"([-\w]+/[-.\w]+(?:@[-./\w]+)?)"  # owner/repo@ref
    )

    if matched := re.fullmatch(pattern, spec):
        auth, host_tag, host_name, repo = matched.groups()
    else:
        return spec

    host_name = _HOST_NAMES.get(host_tag) or host_name or "github.com"

    if auth:
        return f"git+https://{_get_auth(auth)}@{host_name}/{repo}"
    return f"git+https://{host_name}/{repo}"


_colab._load_state()
_colab._update_uv()
