import os
import pickle
import subprocess
import sys

from google.colab import drive, files, runtime, userdata  # type: ignore  # noqa

_STATE_PATH = "/content/.colab_state"

_git_updated = False
_uv_updated = False
_sys_path_extensions = []


def _load_state() -> None:
    global _git_updated, _uv_updated, _sys_path_extensions
    if os.path.isfile(_STATE_PATH):
        with open(_STATE_PATH, "rb") as file:
            state = pickle.load(file)
            if "git_updated" in state:
                _git_updated = state["git_updated"]
            if "uv_updated" in state:
                _uv_updated = state["uv_updated"]
            if "sys_path_extensions" in state:
                _sys_path_extensions = state["sys_path_extensions"]
                sys.path.extend(_sys_path_extensions)

    # Temporary workaround for colabtools/issues#5237
    os.environ["UV_CONSTRAINT"] = os.environ["UV_BUILD_CONSTRAINT"] = ""


def _save_state() -> None:
    with open(_STATE_PATH, "wb") as file:
        pickle.dump(
            {
                "git_updated": _git_updated,
                "uv_updated": _uv_updated,
                "sys_path_extensions": _sys_path_extensions,
            },
            file,
            pickle.HIGHEST_PROTOCOL,
        )


def _update_uv() -> None:
    global _uv_updated
    if _uv_updated:
        return

    try:
        result = subprocess.run(
            ("uv", "pip", "install", "--system", "-Uq", "uv"),
            capture_output=True,
            encoding="utf-8",
            timeout=10,
        )
    except subprocess.TimeoutExpired as exc:
        print(exc)
    else:
        if result.returncode != 0:
            print(result.stderr, end="")
        else:
            _uv_updated = True
