import csvToPlot

spectraDirectory = "ppbspectra/"
minPt, maxPt = 8, 20

# parameters from 5TeV pPb pi0/eta paper
pi0tsallisparams = {"A": 8.82, "Aerr": 0.47, "n": 7.14, "nerr": 0.09, "T": 0.163, "Terr": 0.0005, "m": 0.135}
etatsallisparams = {"A": 0.88, "Aerr": 0.12, "n": 7.47, "nerr": 0.37, "T": 0.27, "Terr": 0.02, "m": 0.548}
sigmamb = 2.1*10**12 #pb


# decay photon spectra
pygamma = csvToPlot.pythia(spectraDirectory + "pythia-gamma.dat", minPt, maxPt)
sharkfin = csvToPlot.mesondecays(spectraDirectory + "decay-sharkfin.dat", minPt, maxPt)

# direct photon spectra
jpnlo = csvToPlot.jetphox(spectraDirectory + "jetphox-nlo.dat", minPt, maxPt)
peternnnll = csvToPlot.peter(spectraDirectory + "peter-nnnll.dat", minPt, maxPt)
pwggamma = csvToPlot.pwgga(spectraDirectory + "pwgga-gamma.dat", minPt, maxPt)
wv = csvToPlot.vogelsang(spectraDirectory + "vogelsang.dat", minPt, maxPt)

# lower order photon spectra
jpdir = csvToPlot.jetphox(spectraDirectory + "jetphox-dir.dat", minPt, maxPt)
jpfrag = csvToPlot.jetphox(spectraDirectory + "jetphox-frag.dat", minPt, maxPt)
peterlo = csvToPlot.peter(spectraDirectory + "peter-lo.dat", minPt, maxPt)

# jetphox isolation cuts
jpiso1dir = csvToPlot.jetphox(spectraDirectory + "jetphox-iso1-dir.dat", minPt, maxPt)
jpiso1frag = csvToPlot.jetphox(spectraDirectory + "jetphox-iso1-frag.dat", minPt, maxPt)
jpiso2dir = csvToPlot.jetphox(spectraDirectory + "jetphox-iso2-dir.dat", minPt, maxPt)
jpiso2frag = csvToPlot.jetphox(spectraDirectory + "jetphox-iso2-frag.dat", minPt, maxPt)
jpiso4dir = csvToPlot.jetphox(spectraDirectory + "jetphox-iso4-dir.dat", minPt, maxPt)
jpiso4frag = csvToPlot.jetphox(spectraDirectory + "jetphox-iso4-frag.dat", minPt, maxPt)

# meson spectra
etatsallis = csvToPlot.mesonTsallis(sharkfin['pt'], etatsallisparams, sigmamb)
piontsallis = csvToPlot.mesonTsallis(sharkfin['pt'], pi0tsallisparams, sigmamb)
pwgpion = csvToPlot.pwgga(spectraDirectory + "pwgga-pion.dat", minPt, maxPt)
pypion = csvToPlot.pythia(spectraDirectory + "pythia-pion.dat", minPt, maxPt)