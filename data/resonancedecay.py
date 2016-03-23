#!/usr/bin/python

import ROOT
from array import array

from observables import Observables


def four_momentum(m, p):
    energy = ROOT.TMath.Hypot(m, p.Mag())  # sqrt(p*p + m*m)
    return ROOT.TLorentzVector(p, energy)


class ResonanceDecay(object):
    def __init__(self, mom_distribution, mass_distribution):
        self.masses = array(
            'd', [
                1.87561297416687012,
                0.139569997787475586,
                0.139569997787475586
            ])

        self.generatemomentum = mom_distribution
        self.generatemass = lambda: mass_distribution(sum(self.masses))
        self.observables = None  # create one only before simulation

    def Simulate(self, nevents, caption=''):
        # from progressbar import  ProgressBar
        # pbar = ProgressBar(nevents).start()
        self.observables = Observables(
            ' #N_{events} =  %d,' % nevents + caption)
        for i in range(nevents):
            d, pip, pim = self.GetParticles()
            self.observables.PushBack(d, pip, pim)
            # pbar.update(i)
        # pbar.finish()
        # self.observables.Draw()

    def GenerateEffect(self):
        resonance = four_momentum(self.generatemass(), self.generatemomentum())

        event = ROOT.TGenPhaseSpace()
        event.SetDecay(resonance, len(self.masses), self.masses)
        event.Generate()

        # array of particle arrays. This is used later
        return [[event.GetDecay(i)] for i in range(len(self.masses))]

    def GetParticles(self):
        """Now this function does nothing but it's useful in derived classes"""
        return self.GenerateEffect()

    def TraceDependece(self, dataf, p=None, m=None, nevents=10000, caption=''):
        if p:
            self.generatemomentum = p
        if m:
            self.generatemass = m
        self.Simulate(nevents, caption)
        return dataf(self.observables)


class ResonanceBackgroundDecay(ResonanceDecay):
    def __init__(self, mom_distribution, mass_distribution, bkg_distribution):
        super(ResonanceBackgroundDecay, self).__init__(
            mom_distribution, mass_distribution)
        self.GetBkgrPiMomentum = bkg_distribution

    def GetParticles(self):
        """Now we use it"""
        d, p, n = self.GenerateEffect()
        # we have 5 positive/negative pions on average (ROOT way)
        pbkgr = [four_momentum(0.1395, self.GetBkgrPiMomentum())
                 for i in range(ROOT.gRandom.Poisson(5))]
        nbkgr = [four_momentum(0.1395, self.GetBkgrPiMomentum())
                 for i in range(ROOT.gRandom.Poisson(5))]
        p = p + pbkgr
        n = n + nbkgr
        return d, p, n


def GetPseudoRandomData(n=1):
    simple_decay = ResonanceDecay(
        lambda x: 2.4,
        lambda x: 2.370
    )

    return [
        simple_decay.TraceDependece(
            lambda x: x.phi,
            caption="p = " + str(0.5 * i),
            p=lambda: on_sphere(0.5 * i))
        for i in range(n)]


def on_sphere(radius=1.000):
    x, y, z = ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)
    ROOT.gRandom.Sphere(x, y, z, radius)
    return ROOT.TVector3(x, y, z)


def main():
    simple_decay = ResonanceDecay(
        lambda x: on_sphere(2.4),
        lambda x: ROOT.gRandom.Gaus(2.370, 0.01)
    )
    simple_decay.Simulate(20000)


if __name__ == '__main__':
    main()
