"""Manage keyboard shortcut assignments.

Manages the assignment of an opaque 'payload', such as a shortcut (hotkey,
command, action, etc.) to each of ~800 logical keys on a typical computer
keyboard having ~100 physical (base) keys and 3 key modifiers: Ctrl, Alt
and Shift.

Some keys are "shifted-aliases"; e.g., '!' is an alias to target "Shift+1".
Assigning a payload to an alias also assigns to its target; and vice-versa.

>>> import keyboard
>>> kbd = keyboard.Keyboard()

>>> kbd.key('!').payload = 'bang is shift+1'
>>> kbd.key('shift+1').payload
'bang is shift+1'

>>> kbd.key('shift+1').payload = 'shift+1 is bang'
>>> kbd.key('!').payload
'shift+1 is bang'

>>> str(kbd.key('!'))
'!'

>>> str(kbd.key('shift+1'))
'!'
"""

# -------------------------------------------------------------------------------

from __future__ import annotations

from typing import Any, Iterator, NamedTuple

# -------------------------------------------------------------------------------


class Keyid(NamedTuple):
    """Key identifier."""

    basename: str
    keymod: int


# -------------------------------------------------------------------------------


class Key:
    """A computer keyboard key.

    FIXME

    Key identifier built from basename/keymod components. Primarily used
    to uniquely identify logical keys; may also identify a keymod permutation.

    Three key modifiers (Ctrl, Alt, Shift), when pressed in combination
    with an ordinary key, provide 8 permutations to temporarily modify the
    action to be taken when that ordinary (base) key is pressed.
    """

    MOD_CTRL, MOD_ALT, MOD_SHIFT, MOD_NONE = 4, 2, 1, 0
    MOD_LIST = range(2**3)

    _mod_names = [None, "Shift", "Alt", None, "Ctrl"]
    _mod_strs = [
        "",
        "Shift",
        "Alt",
        "Alt+Shift",
        "Ctrl",
        "Ctrl+Shift",
        "Ctrl+Alt",
        "Ctrl+Alt+Shift",
    ]
    _mod_reprs = [
        "Key.MOD_NONE",
        "Key.MOD_SHIFT",
        "Key.MOD_ALT",
        "Key.MOD_ALT | Key.MOD_SHIFT",
        "Key.MOD_CTRL",
        "Key.MOD_CTRL | Key.MOD_SHIFT",
        "Key.MOD_CTRL | Key.MOD_ALT",
        "Key.MOD_CTRL | Key.MOD_ALT | Key.MOD_SHIFT",
    ]

    # -------------------------------------------------------------------------------

    def __init__(
        self,
        keyname: str | None = None,
        keymod: int | None = None,
        _basekey: Basekey | None = None,
    ) -> None:
        """Create a new logical key.

        Args:
            keyname: name of key, possibly with modifier names; default=''.
            keymod: modifier bits; default=Key.MOD_NONE.
            _basekey: for internal use.

        One of keyname and/or keymod must be given with a non-default value;
        they will be parsed into 'basename' and 'keymod' attributes.

        Single-argument constructor splits keyname into basename/keymod components:
            >>> Key('A')
            Key(keyname='A', keymod=Key.MOD_NONE)

        Modifier names may be embedded in the keyname by prepending and joining with a '+':
            >>> Key('Ctrl+Left Arrow')
            Key(keyname='Left Arrow', keymod=Key.MOD_CTRL)

        Modifier names are not case-sensitive.
            >>> Key('cTRL+aLT+Home')
            Key(keyname='Home', keymod=Key.MOD_CTRL | Key.MOD_ALT)

        Basename case is preserved...
            >>> Key('a')
            Key(keyname='a', keymod=Key.MOD_NONE)

        ...but comparisons are not case-sensitive.
            >>> Key('a') == Key('A')
            True

        When keyname is empty, object identifies one of the keymod
        permutations that have at least 1 modifier bit set (all except
        Key.MOD_NONE).

            >>> Key(keymod=Key.MOD_CTRL | Key.MOD_ALT)
            Key(keyname='', keymod=Key.MOD_CTRL | Key.MOD_ALT)

        Attributes:
            basename: name of key, case preserved (from keyname), default=''.
            keymod: key modifier bits, default=Key.MOD_NONE.
            payload: opaque user-data structure.
        """

        # public
        self._basename, self.keymod = self.parse_args(keyname, keymod)
        self._payload: Any = None

        # private
        self._basekey = _basekey  # parent Basekey(object).
        self._alias_key: Key | None = None  # set when this key is the target of an alias.
        self._target_key: Key | None = None  # set when this key is an alias to a target.

    # -------------------------------------------------------------------------------

    @classmethod
    def parse_args(cls, keyname: str | None = None, keymod: int | None = None) -> Keyid:
        """Return Keyid parsed from given args."""

        if keyname:
            keyname = keyname.strip()

        if keyname:
            keyid = cls._parse_keyname(keyname)

            if keymod is None:
                # 1-arg-signature: Key(keyname).
                return keyid

            # 2-arg-signature: Key(keyname, keymod). Expect keymods in
            # one arg or the other; no need to enforce, unless they disagree.
            if keyid.keymod not in (cls.MOD_NONE, keymod):
                raise ValueError("keymods disagree")

            return Keyid(keyid.basename, keymod)

        if keymod is None or keymod == cls.MOD_NONE:
            raise ValueError("keyname and/or keymod must be given")

        return Keyid("", keymod)

    # -------------------------------------------------------------------------------

    @classmethod
    def _parse_keyname(cls, keyname: str) -> Keyid:
        """Return Keyid parsed from given arg.

        >>> Key._parse_keyname(None)
        Keyid(basename='', keymod=0)

        >>> Key._parse_keyname('')
        Keyid(basename='', keymod=0)

        >>> Key._parse_keyname(' ')
        Keyid(basename='', keymod=0)

        >>> Key._parse_keyname(' A ')
        Keyid(basename='A', keymod=0)

        >>> Key._parse_keyname(' ctrl+shift+Page uP ')
        Keyid(basename='Page uP', keymod=5)

        >>> Key._parse_keyname('ctrl+alt')
        Keyid(basename='', keymod=6)

        """

        if keyname:
            keyname = keyname.strip()

        basename = keyname.lower() if keyname else ""
        keymod = cls.MOD_NONE

        if basename in ("ctrl", "alt", "shift") or basename.endswith(
            ("+ctrl", "+alt", "+shift")
        ):
            basename += "+"

        if basename.find("ctrl+") >= 0:
            basename = basename.replace("ctrl+", "")
            keymod |= cls.MOD_CTRL

        if basename.find("alt+") >= 0:
            basename = basename.replace("alt+", "")
            keymod |= cls.MOD_ALT

        if basename.find("shift+") >= 0:
            basename = basename.replace("shift+", "")
            keymod |= cls.MOD_SHIFT

        # preserve case.
        basename = keyname[-len(basename) :] if basename else ""

        return Keyid(basename, keymod)

    # -------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return printable name of key."""
        obj = self._alias_key or self
        if obj.keymod and obj._basename:
            return obj._mod_strs[obj.keymod] + "+" + obj._basename
        if obj.keymod:
            return obj._mod_strs[obj.keymod]
        return obj._basename

    # -------------------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return evaluable construct."""
        obj = self._target_key or self
        return str.format(
            "{}(keyname={!r}, keymod={})",
            obj.__class__.__name__,
            obj.basename,
            obj._mod_reprs[obj.keymod],
        )

    # -------------------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """Compare objects without being case-sensitive."""
        if not isinstance(other, self.__class__):
            return False
        return self.keymod == other.keymod and self.basename.lower() == other.basename.lower()

    # -------------------------------------------------------------------------------

    def __ne__(self, other: object) -> bool:
        """Compare objects without being case-sensitive."""
        return not self.__eq__(other)

    # -------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------

    @property
    def basename(self) -> str:
        """Return name of key with no keymods."""
        obj = self._target_key or self
        return obj._basename  # pylint: disable=protected-access

    # -------------------------------------------------------------------------------

    @property
    def payload(self) -> Any:
        """Return opaque user-data structure assigned to this key."""
        obj = self._target_key or self
        return obj._payload  # pylint: disable=protected-access

    # -------------------------------------------------------------------------------

    @payload.setter
    def payload(self, value: Any) -> None:
        """Assign opaque user-data structure to this key."""
        obj = self._target_key or self
        obj._payload = value  # pylint: disable=protected-access

    # -------------------------------------------------------------------------------

    @property
    def grpname(self) -> str:
        """Return name of key group."""
        return self._basekey.keygroup.grpname if self._basekey else ""

    # -------------------------------------------------------------------------------

    def modnames(self, fill: str = "") -> tuple[str, str, str]:
        """Return tuple of names of keymod bits if set else fill."""

        obj = self._target_key or self

        # pylint: disable=protected-access
        return (  # type: ignore
            obj._mod_names[obj.MOD_CTRL] if (obj.keymod & obj.MOD_CTRL) else fill,
            obj._mod_names[obj.MOD_ALT] if (obj.keymod & obj.MOD_ALT) else fill,
            obj._mod_names[obj.MOD_SHIFT] if (obj.keymod & obj.MOD_SHIFT) else fill,
        )


# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------


class Basekey:
    """A physical key, such as 'A', 'F1' and 'Home'.

    Each basekey contains 8 logical keys, one for each keymod permutation.
    """

    # -------------------------------------------------------------------------------

    def __init__(self, basename: str, keygroup: Keygroup):
        """Create physical (base) key as member of keygroup.

        Args:
            basename: name of base key.
            keygroup: parent Keygroup(object).

        Attributes:
            basename: name of base key.
            keygroup: parent Keygroup(object).
            keys: list of logical Key(object), indexed by keymod.
        """

        # name of base key.
        self.basename = basename

        # parent Keygroup(object).
        self.keygroup = keygroup

        # list of logical Key(object)'s, indexed by keymod.
        self.keys: list[Key | None] = [None] * len(Key.MOD_LIST)
        for keymod in Key.MOD_LIST:
            self.keys[keymod] = Key(self.basename, keymod, _basekey=self)

    # -------------------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return evaluable construction."""
        return str.format(
            "{}(basename={!r}, keygroup={!r}",
            self.__class__.__name__,
            self.basename,
            self.keygroup,
        )

    # -------------------------------------------------------------------------------

    # @property
    # def keys(self):
    #    """Returns list of this base key's logical keys."""
    #    return [x for x in self.keys]

    # -------------------------------------------------------------------------------

    @property
    def assigned_keys(self) -> list[Key]:
        """Return list of this base key's assigned logical keys."""
        # pylint: disable=protected-access
        return [x for x in self.keys if x and x.payload and not x._target_key]


# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------


class Keygroup:
    """Arbitrary group of base keys.

    Group of letters, group of digits, etc.
    """

    def __init__(self, grpname: str) -> None:
        """Create group of base keys.

        Args:
            grpname: name of key group.

        Attributes:
            grpname: name of key group.
            basekeys: list of member Basekey(object)'s.
        """

        self.grpname = grpname
        self.basekeys: list[Basekey] = []

    # -------------------------------------------------------------------------------

    def __repr__(self) -> str:
        """docstring."""
        return str.format("{}({!r})", self.__class__.__name__, self.grpname)

    # -------------------------------------------------------------------------------

    @property
    def assigned_basekeys(self) -> list[Basekey]:
        """Return list of this keygroup's assigned base keys.

        (those with at least one assigned logical key)
        """
        return [x for x in self.basekeys if x.assigned_keys]

    # -------------------------------------------------------------------------------

    @property
    def keys(self) -> Iterator[Key]:
        """Return list of this keygroup's logical keys."""
        for basekey in self.basekeys:
            yield from [x for x in basekey.keys if x]

    # -------------------------------------------------------------------------------

    @property
    def assigned_keys(self) -> Iterator[Key]:
        """Return list of this keygroup's assigned logical keys."""
        for basekey in self.basekeys:
            yield from basekey.assigned_keys


# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------


class Keyboard:
    """Collection of Keygroup(object)'s.

    which are collections of physical Basekey(object)'s,
    each of which contain 8 logical Key(object)'s.

    Some logical keys have a secondary name, alias, to refer to them. All are
    "shifted" keymod permutations; for example:

        alias, refers to:   target
        -----------------   ------
        !                   Shift+1
        @                   Shift+2
        #                   Shift+3
        :                   ...
        Alt+!               Alt+Shift+1
        Alt+@               Alt+Shift+2
        Alt+#               Alt+Shift+3
        :                   ...
        Ctrl+!              Ctrl+Shift+1
        Ctrl+@              Ctrl+Shift+2
        Ctrl+#              Ctrl+Shift+3
        :                   ...
        Ctrl+Alt+!          Ctrl+Alt+Shift+1
        Ctrl+Alt+@          Ctrl+Alt+Shift+2
        Ctrl+Alt+#          Ctrl+Alt+Shift+3
    """

    # -------------------------------------------------------------------------------
    # Description of the default keyboard.

    _default_keygroups: list[dict[str, str | list[str]]] = [
        {"Alpha": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"},
        {"Numeric": "1234567890"},
        {"Punct": "`~!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?"},
        {"Function": ["F" + str(_) for _ in range(1, 13)]},
        {"NumPad": ["NumPad" + str(_) for _ in "1234567890*+-./"]},
        {
            "Nav": [
                "Up Arrow",
                "Down Arrow",
                "Left Arrow",
                "Right Arrow",
                "Home",
                "End",
                "Page Up",
                "Page Down",
            ]
        },
        {"Other": ["Backspace", "Enter", "Space", "Tab", "Caps Lock", "Ins", "Del"]},
        {"Tape": ["Play Pause", "Stop", "Forward", "Rewind", "Record"]},
    ]

    # -------------------------------------------------------------------------------
    # Description of the default aliases for the default keyboard.

    _default_shifted_aliases = {
        "!": "1",
        "@": "2",
        "#": "3",
        "$": "4",
        "%": "5",
        "^": "6",
        "&": "7",
        "*": "8",
        "(": "9",
        ")": "0",
        "~": "`",
        "_": "-",
        "+": "=",
        "{": "[",
        "}": "]",
        "|": "\\",
        ":": ";",
        '"': "'",
        "<": ",",
        ">": ".",
        "?": "/",
    }

    # -------------------------------------------------------------------------------

    def __init__(
        self,
        keygroups: list[dict[str, str | list[str]]] | None = None,
        aliases: dict[str, str] | None = None,
    ):
        """Create a keyboard from given args or internal defaults.

        Args:
            keygroups: optional, list of keygroup descriptions; keynames by keygroup.
            aliases: optional, list of "shifted-alias" descriptions; targets by alias.

        Attributes:
            keygroups: ordered list of Keygroup(object)'s.

        """

        self.keygroups: list[Keygroup] = []
        self._basekeys_by_basename: dict[str, Basekey] = {}

        self._build_keyboard(self._default_keygroups if keygroups is None else keygroups)
        self._apply_aliases(self._default_shifted_aliases if aliases is None else aliases)

    # -------------------------------------------------------------------------------

    def _build_keyboard(
        self,
        keygroups: list[dict[str, str | list[str]]] | None = None,
    ) -> None:

        # Build a Keyboard...
        for grpname, basenames in [
            inner for outer in keygroups for inner in outer.items()  # type: ignore
        ]:

            # ...as a list of Keygroup's...
            keygroup = Keygroup(grpname)

            for basename in basenames or []:

                # ...containing a list of Basekey's.
                basekey = Basekey(basename, keygroup)
                keygroup.basekeys.append(basekey)

                # add to lookup table.
                self._basekeys_by_basename[basekey.basename.lower()] = basekey

            self.keygroups.append(keygroup)

    # -------------------------------------------------------------------------------

    def _apply_aliases(self, aliases: dict[str, str]) -> None:

        for alias, target in aliases.items():

            alias_basekey = self.basekey(alias)
            target_basekey = self.basekey(target)

            for keymod in [x for x in Key.MOD_LIST if not x & Key.MOD_SHIFT]:

                alias_key = alias_basekey.keys[keymod]
                target_key = target_basekey.keys[keymod | Key.MOD_SHIFT]

                assert alias_key
                assert target_key

                # pylint: disable=protected-access
                alias_key._target_key = target_key
                target_key._alias_key = alias_key

    # -------------------------------------------------------------------------------

    def basekey(self, basename: str) -> Basekey:
        """Return the matching Basekey(object)."""
        return self._basekeys_by_basename[basename.lower()]

    # -------------------------------------------------------------------------------

    _pseudo_keymod_key = Key(keymod=Key.MOD_SHIFT)

    def key(self, keyname: str | None = None, keymod: int | None = None) -> Key:
        """Return matching Key(object) or None."""
        basename, keymod = Key.parse_args(keyname, keymod)
        if not basename:
            self._pseudo_keymod_key.keymod = keymod
            return self._pseudo_keymod_key
        key = self._basekeys_by_basename[basename.lower()].keys[keymod]
        assert key
        return key

    # -------------------------------------------------------------------------------

    @property
    def basekeys(self) -> Iterator[Basekey]:
        """Return list of all physical keys."""
        for keygroup in self.keygroups:
            yield from keygroup.basekeys

    # -------------------------------------------------------------------------------

    @property
    def keys(self) -> Iterator[Key]:
        """Return list of all logical keys."""
        for basekey in self.basekeys:
            yield from [x for x in basekey.keys if x]

    # -------------------------------------------------------------------------------

    @property
    def assigned_basekeys(self) -> Iterator[Basekey]:
        """Return list of physical keys with at least one assigned logical key."""
        for keygroup in self.keygroups:
            yield from keygroup.assigned_basekeys

    # -------------------------------------------------------------------------------

    @property
    def assigned_keys(self) -> Iterator[Key]:
        """Return list of assigned logical keys."""
        for basekey in self.assigned_basekeys:
            yield from [x for x in basekey.keys if x]
