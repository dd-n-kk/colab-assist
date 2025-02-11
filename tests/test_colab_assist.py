import sys
from unittest.mock import Mock, patch

_colab = Mock()
with patch.dict(sys.modules, {"colab_assist._colab": _colab}):
    import colab_assist as A


def test_import_colab_assist():
    assert _colab._load_state.call_count == 1
    assert _colab._update_uv.call_count == 1
