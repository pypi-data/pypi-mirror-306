from __future__ import print_function

import pytest
from _pytest.fixtures import TopRequest

from keyboard import Key, Keyboard
from keyboard.cli import main

# -------------------------------------------------------------------------------


def test_a() -> None:
    with pytest.raises(SystemExit) as err:
        main(["a"])
    assert err.value.code == 0


def test_ctrl_a() -> None:
    with pytest.raises(SystemExit) as err:
        main(["ctrl+a"])
    assert err.value.code == 0


def test_shift_a() -> None:
    with pytest.raises(SystemExit) as err:
        main(["shift+a"])
    assert err.value.code == 0


def test_keymods_disagree() -> None:
    with pytest.raises(ValueError, match=r"keymods disagree"):
        Key("ctrl+A", Key.MOD_SHIFT)


def test_eq_type_mismatch() -> None:
    key = Key("A")
    assert key != "wrong type"


def test_pseudo_keymod_key() -> None:
    k = Keyboard()
    key = k.key(None, Key.MOD_CTRL)
    assert str(key) == "Ctrl"
    assert key.basename == ""
    assert key.keymod == Key.MOD_CTRL


# -------------------------------------------------------------------------------


def _print_key(request: TopRequest, key: Key) -> None:
    # 26 = len('ctrl+alt+shift+right arrow')
    # print(str.format('{} {!s:>26} {!r}', request.node.name, key, key))
    print(str.format("{} {!s:>26} {!s}", request.node.name, key, key))


# -------------------------------------------------------------------------------


def _print_assigned_keys(request: TopRequest, k: Keyboard) -> None:
    print(f'{"assigned keys":=^80}')
    for key in k.assigned_keys:
        _print_key(request, key)


# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#  keyname      keymod    description
# --------    --------    -----------------------------------
#     none        none    a) invalid, raises ValueError.
#     none    not none    b) a keymod permutation.
# not-none        none    c) parse keyname to yield b) or d).
# not-none    not none    d) a logical key.


def test_Key_a() -> None:
    with pytest.raises(ValueError):  # noqa: ignore[PT011]
        Key()
    with pytest.raises(ValueError):  # noqa: ignore[PT011]
        Key(None)
    with pytest.raises(ValueError):  # noqa: ignore[PT011]
        Key(None, None)
    with pytest.raises(ValueError):  # noqa: ignore[PT011]
        Key(keyname=None)
    with pytest.raises(ValueError):  # noqa: ignore[PT011]
        Key(keymod=None)
    with pytest.raises(ValueError):  # noqa: ignore[PT011]
        Key(keyname=None, keymod=None)


# -------------------------------------------------------------------------------
#     none    not none    b) a keymod permutation.


def test_Key_b() -> None:
    k = Key(None, Key.MOD_SHIFT)
    assert str(k) == "Shift"
    assert k.basename == ""
    assert k.keymod == Key.MOD_SHIFT

    k = Key(None, Key.MOD_CTRL | Key.MOD_ALT)
    assert str(k) == "Ctrl+Alt"
    assert k.basename == ""
    assert k.keymod == Key.MOD_CTRL | Key.MOD_ALT


# -------------------------------------------------------------------------------
# not-none        none    c) parse keyname to yield b) or d).


def test_Key_c() -> None:
    C = Key("cTrL+AlT+C")
    assert str(C) == "Ctrl+Alt+C"
    assert C.basename == "C"
    assert C.keymod == Key.MOD_CTRL | Key.MOD_ALT
    assert repr(C) == "Key(keyname='C', keymod=Key.MOD_CTRL | Key.MOD_ALT)"

    c = Key("aLt+CtRl+c")
    assert str(c) == "Ctrl+Alt+c"
    assert c.basename == "c"
    assert c.keymod == Key.MOD_CTRL | Key.MOD_ALT

    d = Key("aLt+CtRl+d")
    assert str(d) == "Ctrl+Alt+d"
    assert d.basename == "d"
    assert d.keymod == Key.MOD_CTRL | Key.MOD_ALT

    assert c == C
    assert d != C
    assert d != c

    a = Key("ctrl")
    assert str(a) == "Ctrl"
    assert a.basename == ""
    assert a.keymod == Key.MOD_CTRL

    a = Key("ctrl+")
    assert str(a) == "Ctrl"
    assert a.basename == ""
    assert a.keymod == Key.MOD_CTRL

    a = Key("shift+alt")
    assert str(a) == "Alt+Shift"
    assert a.basename == ""
    assert a.keymod == Key.MOD_ALT | Key.MOD_SHIFT

    a = Key("shift+alt+")
    assert str(a) == "Alt+Shift"
    assert a.basename == ""
    assert a.keymod == Key.MOD_ALT | Key.MOD_SHIFT

    a = Key("shift+ctrl+alt")
    assert str(a) == "Ctrl+Alt+Shift"
    assert a.basename == ""
    assert a.keymod == Key.MOD_CTRL | Key.MOD_ALT | Key.MOD_SHIFT

    a = Key("shift+ctrl+alt+")
    assert str(a) == "Ctrl+Alt+Shift"
    assert a.basename == ""
    assert a.keymod == Key.MOD_CTRL | Key.MOD_ALT | Key.MOD_SHIFT


# -------------------------------------------------------------------------------
# not-none    not none    d) a logical key.


def test_Key_d() -> None:
    A = Key("A", Key.MOD_NONE)
    assert str(A) == "A"
    assert A.basename == "A"
    assert A.keymod == Key.MOD_NONE

    a = Key("a", Key.MOD_NONE)
    assert str(a) == "a"
    assert a.basename == "a"
    assert a.keymod == Key.MOD_NONE

    x = Key("A", Key.MOD_SHIFT)
    assert str(x) == "Shift+A"
    assert x.basename == "A"
    assert x.keymod == Key.MOD_SHIFT

    y = Key("A", Key.MOD_CTRL | Key.MOD_ALT)
    assert str(y) == "Ctrl+Alt+A"
    assert y.basename == "A"
    assert y.keymod == Key.MOD_CTRL | Key.MOD_ALT

    #
    assert a == A
    assert a != x
    assert a != y
    assert x != y

    assert str(Key("NUMPAD0", Key.MOD_NONE)) == "NUMPAD0"
    assert str(Key("numpad0", Key.MOD_NONE)) == "numpad0"
    assert str(Key("NumPad0", Key.MOD_NONE)) == "NumPad0"

    assert str(Key("PAGE UP", Key.MOD_NONE)) == "PAGE UP"
    assert str(Key("page up", Key.MOD_NONE)) == "page up"
    assert str(Key("Page Up", Key.MOD_NONE)) == "Page Up"


# -------------------------------------------------------------------------------


def test_modnames() -> None:
    assert Key("A").modnames() == ("", "", "")
    assert Key("A").modnames("x") == ("x", "x", "x")

    assert Key("Shift+A").modnames() == ("", "", "Shift")
    assert Key("Shift+A").modnames("x") == ("x", "x", "Shift")

    assert Key("Alt+A").modnames() == ("", "Alt", "")
    assert Key("Alt+A").modnames("x") == ("x", "Alt", "x")

    assert Key("Alt+Shift+A").modnames() == ("", "Alt", "Shift")
    assert Key("Alt+Shift+A").modnames("x") == ("x", "Alt", "Shift")

    assert Key("Ctrl+A").modnames() == ("Ctrl", "", "")
    assert Key("Ctrl+A").modnames("x") == ("Ctrl", "x", "x")

    assert Key("Ctrl+Shift+A").modnames() == ("Ctrl", "", "Shift")
    assert Key("Ctrl+Shift+A").modnames("x") == ("Ctrl", "x", "Shift")

    assert Key("Ctrl+Alt+A").modnames() == ("Ctrl", "Alt", "")
    assert Key("Ctrl+Alt+A").modnames("x") == ("Ctrl", "Alt", "x")

    assert Key("Ctrl+Alt+Shift+A").modnames() == ("Ctrl", "Alt", "Shift")
    assert Key("Ctrl+Alt+Shift+A").modnames("x") == ("Ctrl", "Alt", "Shift")


# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------


def test_payload(request: TopRequest) -> None:

    k = Keyboard()
    k.key("ctrl+left arrow").payload = "WEST"
    k.key("alt+right arrow").payload = "EAST"
    k.key("shift+page up").payload = "NORTH"
    k.key("ctrl+shift+page down").payload = "SOUTH"

    print("before unassigning left and right")
    _print_assigned_keys(request, k)
    k.key("ctrl+left arrow").payload = None
    k.key("alt+right arrow").payload = None
    print("after unassigning left and right")
    _print_assigned_keys(request, k)


# -------------------------------------------------------------------------------


def test_aliases(request: TopRequest) -> None:
    k = Keyboard()

    k.key("!").payload = "BANG"
    assert k.key("!").payload == k.key("shift+1").payload
    k.key("@").payload = "AT"
    assert k.key("@").payload == k.key("shift+2").payload
    k.key("#").payload = "HASH"
    assert k.key("#").payload == k.key("shift+3").payload

    k.key("$").payload = "DOLLAR"
    assert k.key("$").payload == k.key("shift+4").payload
    k.key("%").payload = "PERCENT"
    assert k.key("%").payload == k.key("shift+5").payload
    k.key("^").payload = "CIRCUMFLEX"
    assert k.key("^").payload == k.key("shift+6").payload

    _print_assigned_keys(request, k)


# -------------------------------------------------------------------------------


def test_lookup_basename() -> None:
    k = Keyboard()
    with pytest.raises(KeyError):
        k.basekey("any")  # haha


def test_basekey_repr() -> None:
    k = Keyboard()
    b = k.basekey("A")
    assert repr(b) == "Basekey(basename='A', keygroup=Keygroup('Alpha')"


# -------------------------------------------------------------------------------


def test_lookup_keyname() -> None:
    k = Keyboard()
    with pytest.raises(KeyError):
        k.key("press any key to continue...")


# -------------------------------------------------------------------------------


def test_keygroups(request: TopRequest) -> None:
    k = Keyboard()
    for keygroup in k.keygroups:
        print(f"{keygroup.grpname:=^80}")
        for basekey in keygroup.basekeys:
            for key in basekey.keys:
                assert key
                assert key.grpname == keygroup.grpname
                _print_key(request, key)


def test_keygroup_keys() -> None:
    k = Keyboard()
    keygroup = k.keygroups[0]
    assert keygroup.grpname == "Alpha"
    assert len(list(keygroup.keys)) == 26 * 8


def test_keygroup_assigned_keys() -> None:
    k = Keyboard()
    keygroup = k.keygroups[0]
    assert keygroup.grpname == "Alpha"

    k.key("A").payload = "APPLES"
    k.key("Shift+A").payload = "ASPARAGUS"
    k.key("B").payload = "BANANAS"
    assert len(list(keygroup.assigned_keys)) == 3


# -------------------------------------------------------------------------------


def test_keyboard(request: TopRequest) -> None:

    k = Keyboard(
        keygroups=[
            {"letters": "abc"},
            {"digits": "123"},
            {"punct": "!@#"},
        ],
        aliases={
            "!": "1",
            "@": "2",
            "#": "3",
        },
    )

    print(f'{" custom keyboard ":=^80}')
    for key in k.keys:
        _print_key(request, key)
