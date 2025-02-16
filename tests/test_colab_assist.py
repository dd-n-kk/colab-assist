import sys
from unittest.mock import Mock, patch

mock_colab_module = Mock()
sys.modules["colab_assist._colab"] = mock_colab_module

import colab_assist.colab_assist as A  # noqa: E402


def test_import_colab_assist():
    mock_colab_module._load_state.assert_called_once()
    mock_colab_module._update_uv.assert_called_once()


def test_restart():
    mock_ishell = Mock()
    with (
        patch("colab_assist.colab_assist._colab") as mock_colab,
        patch(
            "colab_assist.colab_assist.get_ipython", return_value=mock_ishell
        ) as mock_get_ipython,
    ):
        A.restart()
        mock_colab._save_state.assert_called_once()
        mock_get_ipython.assert_called_once()
        mock_ishell.ask_exit.assert_called_once()


def test_mount():
    with patch("colab_assist.colab_assist._colab.drive.mount") as mock_mount:
        A.mount()
        mock_mount.assert_called_once_with("/content/drive/", force_remount=False)


def test_unmount():
    with patch("colab_assist.colab_assist._colab.drive.flush_and_unmount") as mock_unmount:
        A.unmount()
        mock_unmount.assert_called_once()


def test_end():
    with (
        patch("colab_assist.colab_assist.shutil") as mock_shutil,
        patch("colab_assist.colab_assist._colab") as mock_colab,
    ):
        A.end()
        mock_shutil.rmtree.assert_called_once_with("/content/repos/", ignore_errors=True)
        mock_colab.drive.flush_and_unmount.assert_called_once()
        mock_colab.runtime.unassign.assert_called_once()


def test_get_auth():
    with patch("colab_assist.colab_assist.getpass", return_value="input") as mock_getpass:
        assert A._get_auth("$") == "input"
        mock_getpass.assert_called_once()

    with patch("colab_assist.colab_assist._colab.userdata.get", return_value="secret") as mock_get:
        assert A._get_auth("$key") == "secret"
        mock_get.assert_called_once_with("key")

    assert A._get_auth("token") == "token"


def test_parse_package_spec():
    assert A._parse_package_spec("a-b/c_d") == "git+https://github.com/a-b/c_d"

    assert A._parse_package_spec("google.com/ef/g-h@main") == "git+https://google.com/ef/g-h@main"

    assert A._parse_package_spec("i-j-k/lm@v1.2.3") == "git+https://github.com/i-j-k/lm@v1.2.3"

    assert A._parse_package_spec("$bb/op1/q2@5e2c291") == "git+https://bitbucket.org/op1/q2@5e2c291"

    with patch("colab_assist.colab_assist.getpass", return_value="xxx") as mock_getpass:
        assert (
            A._parse_package_spec("$@$gl/r-4/s-5@feat/foo")
            == "git+https://xxx@gitlab.com/r-4/s-5@feat/foo"
        )
        mock_getpass.assert_called_once()

    with patch("colab_assist.colab_assist._colab.userdata.get", return_value="yyy") as mock_get:
        assert (
            A._parse_package_spec("$zzz@t0t/uv_6@rc/v0.2.0")
            == "git+https://yyy@github.com/t0t/uv_6@rc/v0.2.0"
        )
        mock_get.assert_called_once_with("zzz")
