#!/usr/bin/python

from data.resonancedecay import GetPseudoRandomData


def test_simple():
    phi = GetPseudoRandomData()[0]
    assert phi.GetEntries() > 0
