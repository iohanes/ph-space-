
import ROOT
from math import sqrt
from Utilities import draw_and_save


class Observables(object):
    def __init__(self, caption='', use_acceptance=False):
        self.use_acceptance = use_acceptance
        unique_identifier = '_' + caption.split('=')[-1].strip()
        self.rapidity = ROOT.TH1F(

            'hEta%s' % unique_identifier, '#eta', 1000, -2, 2)
        self.phi = ROOT.TH1F(
            'hPhi%s' % unique_identifier,
            'Angle #phi between d and (#pi^{+}, #pi^{-}); #phi ',
            1000, 0, 2 * ROOT.TMath.Pi())

        self.mass = ROOT.TH1F(
            'hMass%s' % unique_identifier,
            'Effective mass ' + caption, 1000, 0.1, 2.7)

        self.momtot = ROOT.TH1F(
            'hMomt%s' % unique_identifier,
            'Momentum of the system (d, #pi^{-}, #pi^{+})', 5000, 0, 10)

        self.sdalitz = ROOT.TH2F(
            'Msdalitz%s' % unique_identifier,
            'x vs y; #sqrt{3} (T_{#pi^{+}} - T_{#pi^{-}})/q;" \
            " (2T_{d} - T_{#pi^{+}} - T_{#pi^{-} })/q ',
            2000, -6, 6, 2000, 0, 12.)

        self.dalitz = ROOT.TH2F(
            'M_dalitz%s' % unique_identifier,
            'M(d, #pi^{+})^{2} vs M(#pi^{+}, #pi^{-})^{2}',
            2000, 0.05, 0.25, 2000, 4., 5.)

        self.my = ROOT.TH2F(
            'M_vs %s' % unique_identifier,
            'M(d, #pi^{-}, #pi^{+})^{2} vs M(#pi^{-}, #pi^{+})^{2}',
            2000, 0.05, 0.45, 2000, 0.3, 7.,)

        # Hardcoded for now
        mass_of_interest = 2.370

        def fT(x):
            return x.E() - x.M()     # kinetic energy

        def fq(x, y, z): return mass_of_interest - \
            x.M() - y.M() - z.M()  # defect mass

        self.fX = lambda x, y, z: sqrt(3) * (fT(y) - fT(z)) / fq(x, y, z)
        self.fY = lambda x, y, z: (2 * fT(x) - fT(y) - fT(z)) / fq(x, y, z)

    def InDetector(self, particle, deuteron=False):
        if not self.use_acceptance:
            return True

        # acceptance cuts
        if abs(particle.Eta()) > 0.8:
            return False
        if particle.Pt() < 0.15:
            return False
        if deuteron and particle.P() > 1.3:
            return False
        if particle.Pt() > 2.:
            return False

        return True

    def PushBack(self, deuterons, positive, negative):
        # Cut all
        deuterons = [i for i in deuterons if self.InDetector(i, True)]
        positive = [i for i in positive if self.InDetector(i)]
        negative = [i for i in negative if self.InDetector(i)]

        # if all lists are not empty
        if deuterons and positive and negative:
            self.FillHistograms(deuterons, positive, negative)

    def FillHistograms(self, deuterons, positive, negative):
        for d in deuterons:
            for pos in positive:
                for neg in negative:
                    self.FillCombination(d, pos, neg)

    def FillCombination(self, d, p, n):

        self.mass.Fill((d + p + n).M())
        self.momtot.Fill((d + p + n).P())

        self.phi.Fill((p + n).Angle(n.Vect()))

        self.my.Fill((p + n).M() ** 2, (d + p + n).M() ** 2)
        self.dalitz.Fill((p + n).M() ** 2, (p + d).M() ** 2)

        self.sdalitz.Fill(self.fX(d, p, n), self.fY(d, p, n))

    def Draw(self):
        self.momtot.Draw()
        draw_and_save('mom_tot', True, True)

        self.mass.Draw()
        draw_and_save('mass', True, True)

        self.sdalitz.Draw('colz')
        draw_and_save('sdalitz', True, True)

        self.dalitz.Draw('colz')
        draw_and_save('dalitz', True, True)

        self.my.Draw('colz')
        draw_and_save('my', True, True)

        self.phi.Draw()
        draw_and_save('test', True, False)

    def GetAngularWindow(self):
        mean = self.phi.GetMean()
        sigma = self.phi.GetRMS()
        return mean - sigma / 4., mean + sigma / 4.
