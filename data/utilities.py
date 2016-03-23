import ROOT

def draw_and_save(name, draw=True, save=True):
	canvas = ROOT.gROOT.FindObject('c1')
	if not canvas: return
	canvas.Update()
	if save: canvas.SaveAs(name + '.png')
	if draw: raw_input('Press any key ...')

def save_histogram(histogram, filename = 'default', option = 'UPDATE'):
	# if you want rewrite use RECREATE option
	ofile = ROOT.TFile(filename + '.root', option)
	histogram.Write()
	ofile.Write()
	# It's up to you 
	# ofile.Close()
