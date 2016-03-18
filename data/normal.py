#!/usr/bin/python

import ROOT
from ResonanceDecay import GetPseudoRandomData
from Utilities import draw_and_save

def draw_multiple(histograms):
	colors = [2 * i + 0 for i, h in enumerate(histograms)]
	titles = ['P = ' + p.GetName().split('_')[-1] for p in histograms]
	# first one should not contain any option if you need to erase canvas
	drawoptions = [''] + ['same'] *  (len(histograms) - 1 ) 
	map(lambda h: h.Scale(1. / h.Integral() ), histograms) # Normalize
	map(lambda h, c: h.SetLineColor(c), histograms, colors)
	map(lambda h, o: h.Draw('same'), histograms, drawoptions)
	legend = ROOT.TLegend(0.6, 0.6, 0.8, 0.8)
	map(lambda h, t: legend.AddEntry(h, t), histograms, titles)
	legend.Draw()

	draw_and_save('simple_random_hists', True, True)


def main():
	phis = GetPseudoRandomData(4)
	for p in phis: 
		p.Draw()
		draw_and_save('simple_random_hist', True, True)

	# map(lambda x : x.Draw('same'), phis)
	# draw_and_save('simple_random_hists', True, True)

	draw_multiple(phis)



if __name__ == '__main__':
	main()
