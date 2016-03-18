#!/usr/bin/python

import ROOT
from array import array #use this if you need to pass your data by reference 'd' -- means double.

from Observables import * # import our class

def four_momentum(m, p):
	energy = ROOT.TMath.Hypot(m, p.Mag()) # sqrt(p*p + m*m)
	return ROOT.TLorentzVector(p, energy)



class ResonanceDecay(object):
	def __init__(self, mom_distribution, mass_distribution):
		self.masses = array('d',[1.87561297416687012, 0.139569997787475586, 0.139569997787475586] )

		self.GenerateMomentum = mom_distribution
		self.GenerateMass     = lambda : mass_distribution( sum(self.masses) )
		self.observables = None # create one only before simulation


	def Simulate(self, nevents, caption = ''):
		# from progressbar import  ProgressBar
		# pbar = ProgressBar(nevents).start()
		self.observables      = Observables(' #N_{events} =  %d,' % nevents + caption )
		for i in range(nevents): 
			d, pip, pim = self.GetParticles()	
			self.observables.PushBack(d, pip, pim)
			# pbar.update(i)
		# pbar.finish()
		# self.observables.Draw()


	def GenerateEffect(self):
		resonance = four_momentum(self.GenerateMass(), self.GenerateMomentum() )

		event = ROOT.TGenPhaseSpace()
		event.SetDecay(resonance, len(self.masses),  self.masses)
		event.Generate()

		return  [ [event.GetDecay(i)] for i in range(len(self.masses)) ] # array of particle arrays. This is used later


	def GetParticles(self):
		"""Now this function does nothing but it's useful in derived classes"""
		return self.GenerateEffect()


	def TraceDependece(self, dataf, p = None, m = None, nevents = 10000, caption = ''):
		if p: self.GenerateMomentum = p
		if m: self.GenerateMass = m
		self.Simulate(nevents, caption)
		return dataf(self.observables)



class ResonanceBackgroundDecay(ResonanceDecay):
	def __init__(self, mom_distribution, mass_distribution, bkg_distribution):
		super(ResonanceBackgroundDecay, self).__init__(mom_distribution, mass_distribution)
		self.GetBkgrPiMomentum = bkg_distribution


	def GetParticles(self):
		"""Now we use it"""
		d, p, n = self.GenerateEffect()
		# we have 5 positive/negative pions on average (ROOT way)
		pbkgr = [four_momentum(0.1395, self.GetBkgrPiMomentum()) for i in range(ROOT.gRandom.Poisson(5)) ]
		nbkgr = [four_momentum(0.1395, self.GetBkgrPiMomentum()) for i in range(ROOT.gRandom.Poisson(5)) ]
		p = p + pbkgr
		n = n + nbkgr
		return d, p, n



def GetPseudoRandomData(n = 0):
	p = lambda : on_sphere(2.4)
	m = lambda x: 2.370
	simple_decay = ResonanceDecay(p, m)

	fdata = lambda x : x.phi # phi is the histogram from object x in observables class
	mcaption = ' m = 0.2370, p = '
	if n == 0:
		return simple_decay.TraceDependece(fdata, caption=mcaption + str(1.4))
	return [simple_decay.TraceDependece(fdata, caption=mcaption + str(0.5 * i), p=lambda: on_sphere(0.5 * i)) for i in range(n)]



def on_sphere(radius = 1.000):
	x, y, z = ROOT.Double(0), ROOT.Double(0), ROOT.Double(0)
	ROOT.gRandom.Sphere(x, y, z, radius)
	return  ROOT.TVector3(x, y, z)

def main():
	# p = lambda : ROOT.TVector3(0, 0, 2.4) 
	p = lambda : on_sphere(2.4)
	# Here x should be greater than mass drawn from a distribution
	# m = lambda x: 2.370
	m = lambda x: ROOT.gRandom.Gaus(2.370, 0.01) 
	simple_decay = ResonanceDecay(p, m)
	simple_decay.Simulate(20000)

	# background_decay = ResonanceBackgroundDecay(p, m, on_sphere)
	# background_decay.Simulate(20000)



if __name__ == '__main__':
	main()

