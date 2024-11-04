"""Chord for foxdot."""

from ._chord import Chord
from ._pattern import ChordPattern, PChord, c
from ._require import require

__all__ = ['Chord', 'ChordPattern', 'PChord', 'c']

FoxDotCode = require('Code').FoxDotCode

FoxDotCode.namespace['c'] = c
FoxDotCode.namespace['PChord'] = PChord
