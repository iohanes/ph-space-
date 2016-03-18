#!/usr/bin/python

import ROOT
from ResonanceDecay import GetPseudoRandomData
from Utilities import draw_and_save, save_histogram

def main():
	phi = GetPseudoRandomData()
	phi.Draw()
	draw_and_save('simple_random_hist', True, True)
	save_histogram(phi)



if __name__ == '__main__':
	main()
