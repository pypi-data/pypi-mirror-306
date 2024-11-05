from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from toolreg.tools import serialize


if TYPE_CHECKING:
    from collections.abc import Callable


def test_serialize_deserialize():
    text = {"abc": {"def": "ghi"}}
    fmts: list[serialize.SerializeFormatStr] = ["yaml", "json", "ini", "toml"]
    for fmt in fmts:
        serialized = serialize.serialize(text, fmt)
        assert serialize.deserialize(serialized, fmt) == text


def test_dig():
    data = {
        "section1": {
            "section2": {
                "section3": "Hello, World!",
            },
        },
    }
    assert serialize.dig(data, "section1", "section2", "section3") == "Hello, World!"
    assert serialize.dig(data, "section1", "section2", "nonexistent") is None


def test_dig_with_list():
    data = {
        "section1": [
            {"section1": "Wrong one!"},
            {"section2": "Hello, World!"},
        ],
    }
    assert serialize.dig(data, "section1", "section2") == "Hello, World!"


def test_dig_with_keep_path():
    data = {
        "section1": {
            "section2": {
                "section3": "Hello, World!",
                "something": "else!",
            },
        },
    }
    assert serialize.dig(
        data,
        "section1",
        "section2",
        "section3",
        keep_path=True,
    ) == {
        "section1": {"section2": {"section3": "Hello, World!"}},
    }


def test_dig_with_keep_path_and_list():
    # TODO: this behaviour needs to get implemented correctly.
    data = {
        "section1": [
            {"section1": "Wrong one!"},
            {"section2": "Hello, World!"},
        ],
    }
    assert serialize.dig(data, "section1", "section2", keep_path=True) == {
        "section1": {"section2": "Hello, World!"},
    }


@pytest.fixture
def nested_dict() -> dict[str, Any]:
    return {
        "level1": {
            "level2": {
                "key": "value",
                "numbers": [1, 2, 3],
            },
        },
    }


@pytest.fixture
def simple_dict() -> dict[str, str]:
    return {"a": "1", "b": "2"}


@pytest.fixture
def simple_list() -> list[int]:
    return [1, 2, 3]


def test_merge_dicts_basic() -> None:
    dict1 = {"a": 1, "b": 2}
    dict2 = {"c": 3, "d": 4}
    expected = {"a": 1, "b": 2, "c": 3, "d": 4}

    result = serialize.merge(dict1, dict2)
    assert result == expected


def test_merge_dicts_with_overlap() -> None:
    dict1 = {"a": 1, "b": 2}
    dict2 = {"b": 3, "c": 4}
    expected = {"a": 1, "b": 3, "c": 4}

    result = serialize.merge(dict1, dict2)
    assert result == expected


def test_merge_lists() -> None:
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    expected = [1, 2, 3, 4, 5, 6]

    result = serialize.merge(list1, list2)
    assert result == expected


def test_merge_nested_structures(nested_dict: dict[str, Any]) -> None:
    source = {
        "level1": {
            "level2": {
                "new_key": "new_value",
                "numbers": [4, 5, 6],
            },
        },
    }
    expected = {
        "level1": {
            "level2": {
                "key": "value",
                "new_key": "new_value",
                "numbers": [1, 2, 3, 4, 5, 6],
            },
        },
    }

    result = serialize.merge(nested_dict, source)
    assert result == expected


def test_deepcopy_option(simple_dict: dict[str, str]) -> None:
    source = {"c": "3"}
    result = serialize.merge(simple_dict, source, deepcopy=True)
    assert isinstance(result, dict)
    # Modify the original dict
    simple_dict["a"] = "modified"

    # Result should remain unchanged due to deepcopy
    assert result["a"] == "1"


def test_multiple_sources() -> None:
    target = {"a": 1}
    source1 = {"b": 2}
    source2 = {"c": 3}
    expected = {"a": 1, "b": 2, "c": 3}

    result = serialize.merge(target, source1, source2)
    assert result == expected


def test_custom_merger() -> None:
    def custom_list_merger(_merger, target: list[int], source: list[int]) -> list[int]:
        return sorted(set(target + source))

    mergers: dict[type, Callable[[Any, Any, Any], Any]] = {list: custom_list_merger}
    list1 = [3, 1, 2]
    list2 = [2, 3, 4]
    expected = [1, 2, 3, 4]

    result = serialize.merge(list1, list2, mergers=mergers)
    assert result == expected


def test_merge_empty_structures() -> None:
    dict1: dict[str, Any] = {}
    dict2 = {"a": 1}
    result = serialize.merge(dict1, dict2)
    assert result == {"a": 1}

    list1: list[Any] = []
    list2 = [1, 2]
    result = serialize.merge(list1, list2)
    assert result == [1, 2]


@pytest.mark.parametrize(
    "invalid_input",
    [
        None,
        42,
        "string",
        True,
    ],
)
def test_merge_invalid_input(invalid_input: Any) -> None:
    with pytest.raises(TypeError):
        serialize.merge(invalid_input, {})


if __name__ == "__main__":
    pytest.main([__file__])
