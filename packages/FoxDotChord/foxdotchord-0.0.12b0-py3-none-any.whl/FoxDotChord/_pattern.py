import re
from collections.abc import Collection, Iterable, Sequence
from copy import deepcopy
from functools import reduce, singledispatch
from itertools import chain
from operator import iconcat
from typing import Union

from ._chord import Chord
from ._require import require

Pattern = require('Patterns').Pattern
TimeVar = require('TimeVar').TimeVar
PRand = require('Patterns.Generators').PRand
PGroupStar = require('Patterns.PGroups').PGroupStar
__pattern__ = require('Patterns.Sequences').__pattern__


def flat(anything):
    if isinstance(anything, Iterable):
        yield from (f for a in anything for f in flat(a))
    else:
        yield anything


def split(chords):
    replace_comma = re.sub(r'\s?,\s?', ' ', chords.strip())
    filter_ = filter(bool, replace_comma.split(' '))
    yield from map(str.strip, filter_)


REPEAT_PATTERN = r'!(?P<repet>(\d{1,})?\.?(\d{1,})?)'


def decomp_str(chords, *, only_repets=False):
    harmony = []
    repets = []
    for chord in split(chords):
        repet = 1
        if not isinstance(chord, str):
            harmony.append(chord)
            repets.append(repet)
            continue

        if matcher := re.search(r'[A-Z].*' + REPEAT_PATTERN, chord):
            chord = re.sub(REPEAT_PATTERN, '', chord)
            repet = float(matcher.group('repet'))
        repets.append(repet)

        if chord.endswith('@'):
            harmony.extend(notes := Chord(chord.removesuffix('@')).notes)
            for _ in range(len(notes) - 1):
                repets.append(repet)
        else:
            harmony.append(Chord(chord))

    return repets if only_repets else harmony


@singledispatch
def decomp_repets(chords):  # pylint: disable=unused-argument
    return 1


@decomp_repets.register(str)
def _(chords: str):
    return decomp_str(chords, only_repets=True)


@decomp_repets.register(Sequence)
def _(chords):
    sequence = []
    for chord in chords:
        reps = decomp_repets(chord)
        if isinstance(chord, str):
            sequence.extend(reps)
        else:
            sequence.append(reps)
    return sequence


@singledispatch
def decomp_chords(chords):
    return chords


@decomp_chords.register(str)
def _(chords: str):
    return decomp_str(chords)


@decomp_chords.register(list)
def _(chords):
    sequence = []
    for chord in chords:
        chrs = decomp_chords(chord)
        if isinstance(chord, str):
            sequence.extend(chrs)
        else:
            sequence.append(chrs)
    return sequence


@decomp_chords.register(tuple)
def _(chords):
    sequence = []
    for chord in chords:
        chrs = decomp_chords(chord)
        if isinstance(chord, str):
            sequence.extend(chrs)
        else:
            sequence.append(chrs)
    return tuple(sequence)


def decomp(*pattern):
    harmony, repets = [], []

    for p in pattern:
        for chord, repet in zip(decomp_chords(p), decomp_repets(p)):
            harmony.append(chord)
            repets.append(repet)

    return harmony, repets


def comp(*args) -> Union[Pattern, TimeVar]:
    harmony, repets = decomp(*args)
    pattern = ChordPattern(harmony)
    if any(filter(lambda r: r > 1, flat(repets))):
        return TimeVar(pattern, repets)
    return pattern


class __chord__(__pattern__):  # noqa: N801, pylint: disable=invalid-name
    """
    Composing chords and progressions.

    **_`Progression`_**

    - `c[...]` or `c(...)`:
      creates a new progression.

    **_`Random/Stutters`_**

    - `c*[...]`:
      set random values.

    - `c*(...)`:
      distribute the values by the current "dur".

    **_`Shuffles`_**

    - `c**[...]` or `c**(...)`:
      shuffles the values.

    **_`Delays`_**

    - `c^[..., dur]` or `c^(..., dur)`:
       creates a PGroup that delays each value in dur * n.

    **_`Stutters`_**

    - `c+[...]` or `c+(...)`:
      stutters the values over the length of and event's 'sus'.

    - `c/[...]` or `c/(...)`:
      stutter every other request.
    """

    def __getitem__(self, *args) -> Union[Pattern, TimeVar]:
        """
        Creates a harmonic progression based on a list of chords.
        e.g. `c[...]`

        Parameters
        ----------
        args : Any
            Many chords or others patterns.

        Examples
        --------
        **_`Progression:`_**

        You can create a chord pattern in a few ways.

        One of them is using a list of strings:

        >>> c['Am7', 'C(7/9)', 'F7Maj', 'G(4/9/13)']
        P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]

        Or passing a string of chords separated by `space`:

        >>> c['Am7 C(7/9) F7Maj G(4/9/13)']
        P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]

        **_`Repetition:`_**

        You can also set how many times the chord will be repeated

        >>> c['C!4 Dm!2'].json_value()
        ['TimeVar', [Chord('C'), Chord('Dm')], [4.0, 2.0]]

        Or repeat the number of times the arpeggio will be made

        >>> c['C!4 Dm!2 G7!2@'].json_value()
        ['TimeVar', [Chord('C'), Chord('Dm'), 4, 6, 8, 10], [4.0, 2.0, 2.0, 2.0, 2.0, 2.0]]

        Repetition of a group can be done by multiplying it,
        either as a `string` or `list`:

        >>> c['Dm7/11!8 Bb7M!7 Bb7M/5 ' * 2 + 'Dm7M/9!4 Bb7M!2 G7/9!2 ' * 2].json_value()
        ['TimeVar', [Chord('Dm7/11'), Chord('Bb7M'), Chord('Bb7M/5'), Chord('Dm7/11'), Chord('Bb7M'), Chord('Bb7M/5'), Chord('Dm7M/9'), Chord('Bb7M'), Chord('G7/9'), Chord('Dm7M/9'), Chord('Bb7M'), Chord('G7/9')], [8.0, 7.0, 1, 8.0, 7.0, 1, 4.0, 2.0, 2.0, 4.0, 2.0, 2.0]]

        >>> c[['Dm7/11!8 Bb7M!7 Bb7M/5'] * 2 + ['Dm7M/9!4 Bb7M!2 G7/9!2'] * 2].json_value()
        ['TimeVar', [Chord('Dm7/11'), Chord('Bb7M'), Chord('Bb7M/5'), Chord('Dm7/11'), Chord('Bb7M'), Chord('Bb7M/5'), Chord('Dm7M/9'), Chord('Bb7M'), Chord('G7/9'), Chord('Dm7M/9'), Chord('Bb7M'), Chord('G7/9')], [8.0, 7.0, 1, 8.0, 7.0, 1, 4.0, 2.0, 2.0, 4.0, 2.0, 2.0]]

        It must also accept repetition values that are not integers:

        >>> c['B7M D7 G7M Bb7!.75 Eb7M!2.75 Am7!.75 D7'].json_value()
        ['TimeVar', [Chord('B7M'), Chord('D7'), Chord('G7M'), Chord('Bb7'), Chord('Eb7M'), Chord('Am7'), Chord('D7')], [1, 1, 1, 0.75, 2.75, 0.75, 1]]

        **_`Mixing inputs:`_**

        >>> c['C  D ', [1, 4], 'Dm E#', (2, 3), 1]
        P[Chord('C'), Chord('D'), P[1, 4], Chord('Dm'), Chord('E#'), P(2, 3), 1]

        >>> c[1, 'C D', [1, 4], 'Dm E#@', (2, 3)]
        P[1, Chord('C'), Chord('D'), P[1, 4], Chord('Dm'), 3, 5, 7, P(2, 3)]

        >>> c[(2, 3), 'C!4 D', [1, 4], 'Dm!3@', 1].json_value()
        ['TimeVar', [P(2, 3), Chord('C'), Chord('D'), 1, 1, 3, 5, 1, P(2, 3), Chord('C'), Chord('D'), 4, 1, 3, 5, 1], [1, 4.0, 1, 1, 3.0, 3.0, 3.0, 1, 1, 4.0, 1, 1, 3.0, 3.0, 3.0, 1]]

        >>> c[1, c['C D'].arp(), [1, 4], c['Dm E#@'], (2, 3)]
        P[1, P[0, 2, 4, 1, 3.5, 5], P[1, 4], P[Chord('Dm'), 3, 5, 7], P(2, 3)]

        **_`Composition:`_**

        You can put chords in a list to alternate between them.
        In the example below, the first three chords (`#!python 'E7M G⁰ G#m7'`)
        will be played once in the sequence while the list
        (`#!python ['C#7/13 B7/13']` ) will alternatively be:

        - E7M G⁰ G#m7 `C#7/13`
        - E7M G⁰ G#m7 `B7/13`

        >>> c['E7M G⁰ G#m7', ['C#7/13 B7/13']]
        P[Chord('E7M'), Chord('G⁰'), Chord('G#m7'), P[Chord('C#7/13'), Chord('B7/13')]]

        >>> c['E7M!4 G⁰!4 G#m7!4', ['C#7/13!4 B7/13!4']].json_value()
        ['TimeVar', [Chord('E7M'), Chord('G⁰'), Chord('G#m7'), Chord('C#7/13'), Chord('E7M'), Chord('G⁰'), Chord('G#m7'), Chord('B7/13')], [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]]

        To play a group together at the same time, use a `tuple` to form the
        chords:

        >>> c['E7M G⁰ G#m7', ('C#7/13', 'B7/13')]
        P[Chord('E7M'), Chord('G⁰'), Chord('G#m7'), P(Chord('C#7/13'), Chord('B7/13'))]

        >>> c['E7M!4 G⁰!4 G#m7!4', ('C#7/13!4', 'B7/13!4')].json_value()
        ['TimeVar', [Chord('E7M'), Chord('G⁰'), Chord('G#m7'), P(Chord('C#7/13'), Chord('B7/13'))], [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]]

        Returns
        -------
        Pattern
            Chord progression.
        TimeVar
            If any repetition is defined other than 1
        """  # noqa: E501
        harmony, repets = decomp(*args)
        pattern = ChordPattern(harmony)
        if any(filter(lambda r: r > 1, flat(repets))):
            return TimeVar(pattern, repets)
        return pattern

    def __call__(self, *args):
        """
        Creates a harmonic progression based on a list of chords.
        e.g. `c(...)`

        Parameters
        ----------
        args : Any
            Many chords or others patterns.

        Examples
        --------
        You can create a chord pattern in a few ways.

        One of them is using `[]` or `()` with a list of strings
        or passing a string of chords separated by `space`:

        >>> c('Am7', 'C(7/9)', 'F7Maj', 'G(4/9/13)')
        P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]
        >>> c('Am7 C(7/9) F7Maj G(4/9/13)')
        P[Chord('Am7'), Chord('C(7/9)'), Chord('F7Maj'), Chord('G(4/9/13)')]

        Returns
        -------
        Pattern
            Chord progression.
        TimeVar
            If any repetition is defined other than 1
        """
        return self.__getitem__(*args)

    def __mul__(self, other):
        """
        Random  `[]` or spreads `()`.
        e.g. `c*[...]` or `c*(...)`

        Parameters
        ----------
        other : Any
            Another object.

        Examples
        --------
        **_`Random:`_**

        Use `[]` to set random values:

        >>> c*['A C']
        PRand(P[Chord('A'), Chord('C')])

        **_`Stutters`_**

        You can spreads the values across the current “dur”.

        If the dur is 4 beats then it will play each value 2/4 beats apart:

        >>> c['Am7', c*('Bm7 E7')]
        P[Chord('Am7'), P*(Chord('Bm7'), Chord('E7'))]

        In the example above, `Am7` will be played for a full beat while `Bm7`
        and `E7` will be played before the end of the beat.

        This can be interesting in arpeggios.

        >>> c[c*('Am7/2@'), c*(c*('Bm7@'), c*('E7@'))]
        P[P*(5, 6, 7, 9, 11), P*(P*(6, 8, 10.5, 12), P*(2, 4.5, 6, 8))]

        For example:

        ```python
        p1 >> keys(c['Am7', c*('Bm7 E7')], dur=4)
        b1 >> bassguitar(c[c*('Am7/2@'), c*(c*('Bm7@'), c*('E7@'))], dur=4)
        ```

        Returns
        -------
        PRand
            If a list or a Pattern is a step, the returned value will be PRand.
        PGroupStar
            Stutters the values over the length of and event's "dur".
        """
        if isinstance(other, (list, Pattern)):
            return PRand(list(self(other)))
        return PGroupStar(self(other))

    def __pow__(self, other):
        """
        Returns scrambled version.
        e.g. `c**[...]`

        Parameters
        ----------
        other : Any
            Another object.

        Examples
        --------
        >>> c**('A C')
        P**(Chord('A'), Chord('C'))
        >>> c**['A C']
        P**(Chord('A'), Chord('C'))

        Returns
        -------
        PGroupPow
            Shuffled values.
        """
        return super().__pow__(self(other))

    def __xor__(self, other):
        """
        Returns a PGroup that delays each value by dur * n.
        e.g. `c^[..., dur]`

        Parameters
        ----------
        other : Any
            Another object.

        Examples
        --------
        >>> c^('A C', 4)
        P^(Chord('A'), Chord('C'))

        Returns
        -------
        PGroupXor
            Pattern with delay.
        """
        return super().__xor__(self(other))

    def __add__(self, other):
        """
        Stutters the values over the length of and event's 'sus'.
        e.g. `c+[...]`

        Parameters
        ----------
        other : Any
            Another object.

        Examples
        --------
        >>> c+('A C')
        P+(Chord('A'), Chord('C'))
        >>> ('A C')+c
        P+(Chord('A'), Chord('C'))

        Returns
        -------
        PGroupPlus
            Stuttered values.
        """
        return super().__add__(self(other))

    def __truediv__(self, other):
        """
        Stutter every other request.
        e.g. `c/[...]`

        Parameters
        ----------
        other : Any
            Another object.

        Examples
        --------
        >>> c/('A C')
        P/(Chord('A'), Chord('C'))

        Returns
        -------
        PGroupDiv
            Stuttered values.
        """
        return super().__truediv__(self(other))


c = __chord__()
PChord = c  # TODO: Remove this


class ChordPattern(Pattern):
    """
    Class used by `c` to manipulate chords/notes/Patterns.

    You probably shouldn't invoke this class manually, when calling
    c[...] this class will be returned, so it may be worth knowing
    its methods.
    """

    _degrees = {
        'I': 'tonic',
        'II': 'supertonic',
        'III': 'third',
        'IV': 'subdominant',
        'V': 'dominant',
        'VI': 'submediant',
        'VII': 'maj',
        'IX': 'ninth',
        'XI': 'eleventh',
        'XIII': 'thirteenth',
    }

    def degrees(self, grades: Union[str, list[str]], *args: str) -> Pattern:
        """
        Take certain degrees from all chords in the pattern.

        Parameters
        ----------
        grades : str | list[str]
            Degrees to be selected.
        *args : str
            Degrees to be selected.

        Examples
        --------
        Use the function to pick certain chord degrees:

        >>> c['F Am G C'].degrees('i')
        P[3, 5, 4, 0]

        Or use your shorthand function:

        >>> c['F Am G C'].deg('i')
        P[3, 5, 4, 0]

        An interesting example is taking the bass of the chords:

        >>> c['F Am G C'].deg('i')
        P[3, 5, 4, 0]

        It is also possible to take more than one degree of the chords:

        >>> c['F Am G C'].deg('i', 'iii')
        P[3, 5, 5, 7, 4, 6, 0, 2]
        >>> c['F Am G C'].deg(['i', 'iii'])
        P[3, 5, 5, 7, 4, 6, 0, 2]

        Only the degrees that are present in the chord will be returned.

        >>> c['C Dm7'].deg('i', 'vii')
        P[0, 1, 7]
        >>> c['C'].deg('vi')
        P[]

        Anything that is not a chord will be disregarded.

        >>> c['C', 2, (2, 2), [2, 2]].deg('i')
        P[0]

        Returns
        -------
        Pattern
            Note pattern.
        """
        if isinstance(grades, str):
            grades = grades.split(',')

        notes = (
            getattr(c, self._degrees.get(a.strip(), '_'), None)
            for c in self.data
            for a in map(str.upper, chain(grades, args))
        )

        return Pattern(list(filter(lambda n: n is not None, notes)))

    deg = degrees

    @property
    def i(self) -> Pattern:
        """
        Get the degree `I` (tonic) of the chords.

        Examples
        --------
        >>> c['C G'].i
        P[0, 4]

        >>> c['C G'].tonic
        P[0, 4]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('I')

    @property
    def ii(self) -> Pattern:
        """
        Get the degree `II` (supertonic) of the chords.

        Examples
        --------
        >>> c['C2 G2'].ii
        P[1, 5]

        >>> c['C2 G2'].supertonic
        P[1, 5]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('II')

    @property
    def iii(self) -> Pattern:
        """
        Get the degree `III` (third) of the chords.

        Examples
        --------
        >>> c['C G'].iii
        P[2, 6]

        >>> c['C G'].third
        P[2, 6]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('III')

    @property
    def iv(self) -> Pattern:
        """
        Get the degree `IV` (subdominant) of the chords.

        Examples
        --------
        >>> c['C4 G4'].iv
        P[3, 7]

        >>> c['C4 G4'].subdominant
        P[3, 7]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('IV')

    @property
    def v(self) -> Pattern:
        """
        Get the degree `V` (dominant) of the chords.

        Examples
        --------
        >>> c['C G'].v
        P[4, 8]

        >>> c['C G'].dominant
        P[4, 8]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('V')

    @property
    def vi(self) -> Pattern:
        """
        Get the degree `VI` (submediant) of the chords.

        Examples
        --------
        >>> c['C6 G6'].vi
        P[5, 9]

        >>> c['C6 G6'].submediant
        P[5, 9]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('VI')

    @property
    def vii(self) -> Pattern:
        """
        Get the degree `VII` (seven) of the chords.

        Examples
        --------
        >>> c['C7 G7M'].vii
        P[5.5, 10.5]

        >>> c['C7 G7M'].seven
        P[5.5, 10.5]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('VII')

    @property
    def ix(self) -> Pattern:
        """
        Get the degree `IX` (ninth) of the chords.

        Examples
        --------
        >>> c['C9 G9'].ix
        P[8, 12]

        >>> c['C9 G9'].ninth
        P[8, 12]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('IX')

    @property
    def xi(self) -> Pattern:
        """
        Get the degree `XI` (eleventh) of the chords.

        Examples
        --------
        >>> c['C11 G11'].xi
        P[10, 14]

        >>> c['C11 G11'].eleventh
        P[10, 14]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('XI')

    @property
    def xiii(self) -> Pattern:
        """
        Get the degree `XIII` (thirteenth) of the chords.

        Examples
        --------
        >>> c['C13 G13'].xiii
        P[12, 16]

        >>> c['C13 G13'].thirteenth
        P[12, 16]

        Returns
        -------
        Pattern
            Note pattern.
        """
        return self.degrees('XIII')

    tonic = i
    supertonic = ii
    third = iii
    subdominant = iv
    dominant = v
    submediant = vi
    seven = vii
    ninth = ix
    eleventh = xi
    thirteenth = xiii

    def arp(self, arp_pattern: Union[Collection, None] = None):
        """
        Create a arpeggio pattern.

        Parameters
        ----------
        arp_pattern : Collection, optional
            Arpeggio pattern.

        Examples
        --------
        You can create arpeggios with all chords.

        >>> c['C G'].arp()
        P[0, 2, 4, 4, 6, 8]

        Or create  a new Pattern with each item repeated len(arp_pattern) times
        and incremented by arp_pattern.

        >>> c['C G'].arp([0, 3])
        P[0, 3, 2, 5, 4, 7, 4, 7, 6, 9, 8, 11]

        You can also create the arpeggio of a single chord when defining it.

        >>> c['C@ G']
        P[0, 2, 4, Chord('G')]

        Returns
        -------
        Pattern[int]
            Arpeggio pattern.
        """
        notes = [a.notes if hasattr(a, 'notes') else [a] for a in self]
        pattern = Pattern(reduce(iconcat, notes))

        if arp_pattern:
            return pattern.stutter(len(arp_pattern)) + arp_pattern
        return pattern

    def __mul__(self, other):
        """
        Multiple pattern.

        Parameters
        ----------
        other : int
            Times the pattern should be repeated.

        Examples
        --------
        Multiplying the chord sequence

        >>> c['C G'] * 3
        P[Chord('C'), Chord('G'), Chord('C'), Chord('G'), Chord('C'), Chord('G')]

        Multiplying the chord sequence with notes

        >>> c['C G', 1] * 3
        P[Chord('C'), Chord('G'), 1, Chord('C'), Chord('G'), 1, Chord('C'), Chord('G'), 1]

        Multiplying the chord sequence with notes and microtonal notes

        >>> c['C G', 1, 1.5] * 3
        P[Chord('C'), Chord('G'), 1, 1.5, Chord('C'), Chord('G'), 1, 1.5, Chord('C'), Chord('G'), 1, 1.5]

        Multiplying the chord sequence with notes, microtonal notes and note sequence

        >>> c['C G', 1, 1.5, [1, 2]] * 3
        P[Chord('C'), Chord('G'), 1, 1.5, P[1, 2], Chord('C'), Chord('G'), 1, 1.5, P[1, 2], Chord('C'), Chord('G'), 1, 1.5, P[1, 2]]

        Multiplying the sequence of chords with notes, microtonal notes and sequence of notes playing separately and together

        >>> c['C G', 1, 1.5, [1, 2], (2, 1)] * 3
        P[Chord('C'), Chord('G'), 1, 1.5, P[1, 2], P(2, 1), Chord('C'), Chord('G'), 1, 1.5, P[1, 2], P(2, 1), Chord('C'), Chord('G'), 1, 1.5, P[1, 2], P(2, 1)]

        Only interiors can be used, if another type is passed an error will be
        raised

        >>> c['C'] * True
        Traceback (most recent call last):
          ...
        NotImplementedError: Cannot multiplate 'True' -> <class 'bool'>

        >>> c['C'] * False
        Traceback (most recent call last):
          ...
        NotImplementedError: Cannot multiplate 'False' -> <class 'bool'>

        >>> c['C'] * 'string'
        Traceback (most recent call last):
          ...
        NotImplementedError: Cannot multiplate 'string' -> <class 'str'>

        >>> c['C'] * 1.0
        Traceback (most recent call last):
          ...
        NotImplementedError: Cannot multiplate '1.0' -> <class 'float'>

        """  # noqa: E501
        if not isinstance(other, int) or isinstance(other, bool):
            raise NotImplementedError(
                f"Cannot multiplate '{other}' -> {type(other)}"
            )

        copy = self.true_copy()
        copy.data.extend(
            [
                deepcopy(data)
                for _ in range(other - 1)
                for data in self.true_copy().data
            ]
        )
        return copy

    def __add__(self, other):
        """
        Added in pattern.

        Parameters
        ----------
        other : Any
            Element to be added.

        Examples
        --------
        You can use `+` to add an element or another sequence to the chord/note
        pattern.

        >>> c['C'] + Chord('D')
        P[Chord('C'), Chord('D')]

        >>> c['C'] + 'D'
        P[Chord('C'), Chord('D')]

        >>> c['C'] + ['D']
        P[Chord('C'), Chord('D')]

        >>> c['C'] + Pattern('D')
        P[Chord('C'), Chord('D')]

        >>> c['C'] + 1
        P[Chord('C'), 1]

        >>> c['C'] + 2.0
        P[Chord('C'), 2.0]

        >>> c['C'] + c['D']
        P[Chord('C'), Chord('D')]
        """  # noqa: E501
        copy = self.true_copy()
        if isinstance(other, Chord):
            copy.data.append(other)
        elif isinstance(other, str):
            copy.data.append(Chord(other))
        elif isinstance(other, (list, Pattern)):
            copy.data.extend(
                [
                    Chord(data) if isinstance(data, str) else deepcopy(data)
                    for data in list(other)
                ]
            )
        else:
            copy.data.append(other)

        return copy
