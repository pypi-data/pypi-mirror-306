import pytest

from postopus.datacontainers.util.convenience_dict import ConvenienceDict


class Example(ConvenienceDict):
    pass


class Example2(ConvenienceDict):
    __dict_name__ = "systems"


def test_accessing_data_through_shortcut():
    # Testing with class with default dictionary name 'data'
    e = Example()

    # set new values, needs to be done via the dictionary
    e.data["new1"] = "new1-value"
    e.data["new2"] = "new2-value"

    # retrieve values, either via the dictionary or the shortcut
    assert e.new1 == e.data["new1"]
    assert e.new1 == e.data["new1"]

    # Testing with class with custom dictionary name 'systems'
    e2 = Example2()

    # set new values, needs to be done via the dictionary
    e2.systems["new1"] = "new1-value"
    e2.systems["new2"] = "new2-value"

    # retrieve values, either via the dictionary or the shortcut
    assert e2.new1 == e2.systems["new1"]
    assert e2.new1 == e2.systems["new1"]


def test_modifying_existing_data_through_shortcut():
    # Testing with class with default dictionary name 'data'
    e = Example()

    # set new values, needs to be done via the dictionary
    e.data["new1"] = "new1-value"
    e.data["new2"] = "new2-value"

    e.new1 = "updated new1-value"
    assert e.new1 == "updated new1-value"
    assert e.data["new1"] == "updated new1-value"

    # Testing with class with custom dictionary name 'systems'
    e2 = Example2()

    # set new values, needs to be done via the dictionary
    e2.systems["new1"] = "new1-value"
    e2.systems["new2"] = "new2-value"

    e2.new1 = "updated new1-value"
    assert e2.new1 == "updated new1-value"
    assert e2.systems["new1"] == "updated new1-value"


def test_retrieve_non_existing_dictionary_entries():
    e = Example()

    # retrieve non-existing values raises Exception
    with pytest.raises(AttributeError):
        print(e.doesnotexist)


def test_setting_object_attributes():
    # Testing with class with default dictionary name 'data'
    e = Example()

    # setting values in the dictionary via the shortcut is not supported, this
    # should create a new attribute in the class
    e.new = "test"

    assert e.new == "test"
    assert "new" not in e.data

    # Testing with class with custom dictionary name (here 'systems')
    e2 = Example2()

    # setting values via the shortcut is not supported, this should create
    # a new attribute in the class
    e2.new = "test"

    assert e2.new == "test"
    assert "new" not in e2.systems


def test_setting_object_attributes_bug():
    """
    previsously, we checked if the `name` was in the `data` string
    rather than in the `data` dictionary.

    This worked okay, apart from my coincidental testcase where `name` was
    `d` (because `d in "data"` is true in Python).

    Should be fixed now. This test checks for this bug.
    """
    # Testing with class with default dictionary name 'data'
    e = Example()
    e.d = "test"
    assert e.d == "test"
    assert "d" not in e.data

    # Testing with class with custom dictionary name 'systems'
    e2 = Example2()
    e2.s = "test"
    assert e2.s == "test"
    assert "s" not in e2.systems


def test_dir_funtion_works():
    """If the `dir` function doesn't work, autocompletion in IPython/Jupyter fails."""

    e = Example()

    e.data["new1"] = "new1-value"
    e.data["new2"] = "new2-value"

    dir_output = dir(e)

    assert "new1" in dir_output
    assert "new2" in dir_output
