#!/usr/bin/python

from data.ResonanceDecay import GetPseudoRandomData


def test_simple():
    phi = GetPseudoRandomData()
    assert phi.GetEntries() > 0
