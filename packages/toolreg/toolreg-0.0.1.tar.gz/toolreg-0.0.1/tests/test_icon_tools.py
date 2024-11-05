from __future__ import annotations

import pytest

from toolreg.tools import icon


def test_material_key_conversion():
    assert icon.get_pyconify_key("file") == "mdi:file"
    assert icon.get_pyconify_key("mdi:file") == "mdi:file"
    assert icon.get_pyconify_key("material/file") == "mdi:file"
    assert icon.get_pyconify_key(":material-file:") == "mdi:file"


def test_noto_key_conversion():
    assert icon.get_pyconify_key("noto:wrench") == "noto:wrench"
    assert icon.get_pyconify_key(":noto-wrench:") == "noto:wrench"
    assert icon.get_pyconify_key("simple/shieldsdotio") == "simple-icons:shieldsdotio"
    assert (
        icon.get_pyconify_key(":fontawesome-regular-keyboard:") == "fa6-regular:keyboard"
    )
    assert icon.get_pyconify_key("fontawesome/regular/keyboard") == "fa6-regular:keyboard"


if __name__ == "__main__":
    pytest.main([__file__])
