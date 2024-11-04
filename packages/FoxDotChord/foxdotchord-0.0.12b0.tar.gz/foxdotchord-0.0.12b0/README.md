# FoxDotChord

[![Documentation](https://custom-icon-badges.demolab.com/badge/Docs-latest-%23b1f889.svg?logo=book&logoColor=%23b1f889)](https://foxdotchord.readthedocs.io)
[![License](https://custom-icon-badges.demolab.com/badge/License-GPLv3-%23b1f889.svg?logo=law&logoColor=%23b1f889)](https://spdx.org/licenses/)
[![Issue Tracker](https://custom-icon-badges.demolab.com/badge/Issue-Tracker-%23b1f889.svg?logo=issue-opened&logoColor=%23b1f889)](https://codeberg.org/taconi/FoxDotChord/issues)
[![Contributing](https://custom-icon-badges.demolab.com/badge/Contributor-Guide-%23b1f889.svg?logo=git-pull-request&logoColor=%23b1f889)](https://foxdotchord.readthedocs.io/contributing)
[![Source Code](https://custom-icon-badges.demolab.com/badge/Source-Code-%23b1f889.svg?logo=codeberg&logoColor=%23b1f889)](https://codeberg.org/taconi/FoxDotChord/)

[![PyPI version](https://img.shields.io/pypi/v/FoxDotChord.svg?logo=pypi&label=PyPI&color=%234e71b2&logoColor=%2389b1f8)](https://pypi.org/project/FoxDotChord/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/FoxDotChord.svg?logo=python&label=Python&color=%234e71b2&logoColor=%2389b1f8)](https://pypi.python.org/pypi/FoxDotChord/)
[![Downloads](https://img.shields.io/pypi/dm/FoxDotChord?logo=pypi&label=Downloads&color=%234e71b2&logoColor=%2389b1f8)](https://pypistats.org/packages/foxdotchord)

---

Chords to use in [renardo](https://renardo.org) or [FoxDot](https://foxdot.org).

## Installation

Use the package manager you prefer

```sh
pip install FoxDotChord
```

## Examples

```python
from FoxDotChord import PChord as c

c0 = c['C Am7 Dm Em']
t0 >> keys(
    c0.every(3, 'bubble'),
    dur=PDur(3, 8)
)

b0 >> sawbass(c0, amp=1, pan=[0, 1, -1, 0])

d0 >> play('x-o({-=}[--])')
```

```python
from FoxDotChord import PChord as c

Clock.bpm = 180

d1 >> play('(C(ES))   ')

c1 >> swell(
    c['F#6!4 Dm7/9!8 Bm5/7!4'],
    dur=PDur(5, 9)*2,
    oct=var([4, 5], 16),
    amp=1.5,
)

d2 >> play('pn u', amp=2)
```

```python
import FoxDotChord

k1 >> keys(c['Am7', c*('Bm7 E7')], dur=4)
g1 >> bassguitar(c[c*('Am7/2@'), c*(c*('Bm7@'), c*('E7@'))], dur=4)

b1 >> play('(xc)s')
```

```python
import FoxDotChord

Clock.bpm = 90

chords = c[
    'B7M D7 G7M Bb7!.7 Eb7M!2.3 Am7!.7 D7!1.3',
    'G7M B7 Eb7M F#7!.7 B7M!2.3 Fm7 Bb7!.7',
    'Eb7M!2.3 Am7 D7!.7 G7M!2.3 C#m7 F#7!.7',
    'B7M!2.3 Fm7 B7M!.7 Eb7M!2.3 C#m7!.7 F#7!1.3',
]
c1 >> play('o-x-')
s1 >> pianovel(chords, dur=chords.dur)
l1 >> sawbass(chords.values.i, dur=chords.dur)
```

## Contribute

See the [Contributor Guide](https://foxdotchord.readthedocs.io/contributing).
