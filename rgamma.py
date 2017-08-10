import math
import matplotlib.pyplot as plt
import numpy
import rootpy.ROOT as ROOT
from array import array
from standardppbspectra import *

fitplotx = numpy.linspace(minPt, maxPt, 200)

# quick switches for plotting
doplotspectra = True
# doplotspectra = False
doplotresiduals = True
# doplotresiduals = False
doplotrgamma = True
# doplotrgamma = False

def getArray(l):
    arr = array('d')
    arr.fromlist(l)
    return arr

def buildGraph(plotdata):
    pt = getArray(plotdata['pt'])
    dsigma = getArray(plotdata['dsigma'])
    n = len(pt)

    pterr = plotdata.get('pterr')
    dsigmaerr = plotdata.get('dsigmaerr')

    # ROOT needs an array for the x-error, even if one doesn't exist
    if not pterr:
        pterr = [0.0 for i in range(n)]
    pterr = getArray(pterr)

    # include a very small fake y-error for points that don't have one;
    # apparently, this is standard when fitting
    if not dsigmaerr:
        dsigmaerr = [0.001 for i in range(n)]

    # unpack asymmetric errors if necessary
    if isinstance(dsigmaerr[0], list):
        dsigmaerr = [getArray(err) for err in dsigmaerr]
        graph = ROOT.TGraphAsymmErrors(n, pt, dsigma, pterr, pterr, dsigmaerr[0], dsigmaerr[1])
    else:
        dsigmaerr = getArray(dsigmaerr)
        graph = ROOT.TGraphErrors(n, pt, dsigma, pterr, dsigmaerr)

    return graph

def fitToTsallis(m, graph, approxNorm):
    tsallisstring = "10**12*[0]/(2*pi)*([1]-1)*([1]-2)/([1]*[2]*([1]*[2]+"+str(m)+"*([1]-2)))*pow(1+(sqrt("+str(m)+"**2+x**2)-"+str(m)+")/([1]*[2]), -[1])"
    tsallis = ROOT.TF1("tsallis", tsallisstring, minPt, maxPt)
    tsallis.SetParNames("A", "n", "T")
    tsallis.SetParameters(approxNorm*2/(10**7), 5, 0.2)

    graph.Fit(tsallis, "R")
    fit = graph.GetFunction("tsallis")
    fitparams = {}
    for i, parameter in enumerate(["A", "n", "T"]):
        fitparams[parameter] = fit.GetParameter(parameter)
        fitparams[parameter+"err"] = fit.GetParError(i)
    fitparams["Chi2"] = fit.GetChisquare()
    fitparams["NDF"] = fit.GetNDF()

    return fitparams

def getTsallis(ptRange, m, fitparams):
    def tsallis(pt):
        A = fitparams["A"]
        n = fitparams["n"]
        T = fitparams["T"]
        return 10**12*A/(2*math.pi)*(n-1)*(n-2)/(n*T*(n*T+m*(n-2)))*math.pow(1+(math.sqrt(m**2+pt**2))/(n*T),-n)
    
    return map(tsallis, ptRange)

def getFitResults(plotdata, decayResults=None):
    graph = buildGraph(plotdata)
    fitparams = fitToTsallis(0, graph, plotdata['dsigma'][0])
    tsallis = getTsallis(fitplotx, 0, fitparams)
    
    results = {}
    results['chi2ndf'] = fitparams['Chi2']/fitparams['NDF']
    results['residuals'] = numpy.divide(numpy.subtract(plotdata['dsigma'], getTsallis(plotdata['pt'], 0, fitparams)), plotdata['dsigma'])
    results['graph'] = graph
    results['fitparams'] = fitparams 
    results['tsallis'] = tsallis
    
    if decayResults:
        results['rgamma'] = numpy.add(1, numpy.divide(tsallis, decayResults['tsallis']))

    return results

decayResults = getFitResults(sharkfin)
peterResults = getFitResults(peternnnll, decayResults)
wvResults = getFitResults(wv, decayResults)
jpResults = getFitResults(jpnlo, decayResults)
pwgResults = getFitResults(pwggamma, decayResults)

# plot spectra and fits
if doplotspectra:
    def plotDataAndFit(plotdata, fitResults, color, label):
        data = plt.errorbar(plotdata['pt'], plotdata['dsigma'], plotdata.get('dsigmaerr'), plotdata.get('pterr'), fmt=color+'o', label=label)
        fit, = plt.plot(fitplotx, fitResults['tsallis'], color+':', label='$\chi^2$/NDF='+str(fitResults['chi2ndf']))
        return data, fit

    plt.figure(1)
    decaydata, decayfit = plotDataAndFit(sharkfin, decayResults, 'm', 'Decay photons from pi0 and eta')
    peterdata, peterfit = plotDataAndFit(peternnnll, peterResults, 'k', 'PeTeR NNNLL')
    wvdata, wvfit = plotDataAndFit(wv, wvResults, 'b', 'W.Vogelsang calculations')
    jpdata, jpfit = plotDataAndFit(jpnlo, jpResults, 'g', 'JETPHOX NLO (direct + frag)')
    pwgdata, pwgfit = plotDataAndFit(pwggamma, pwgResults, 'r', 'PWG-GA prompt photons')

    plt.yscale('log')
    plt.xlabel('pT [GeV]')
    plt.ylabel('Invariant cross section [pb/GeV^2]')
    orderedHandles = [decaydata, peterdata, wvdata, jpdata, pwgdata]
    # orderedHandles = [decaydata, decayfit, peterdata, peterfit, wvdata, wvfit, jpdata, jpfit, pwgdata, pwgfit]
    plt.legend(handles=orderedHandles, numpoints=1)

# plot residuals
if doplotresiduals:
    def plotResiduals(i, plotdata, fitResults, color, label):
        plt.subplot(3, 2, i)
        res, = plt.plot(plotdata['pt'], fitResults['residuals'], color+'.', label=label)
        plt.plot(fitplotx, [0 for x in fitplotx], 'y:')
        plt.ylim([-0.05, 0.05])
        return res

    plt.figure(2)
    dRes = plotResiduals(1, sharkfin, decayResults, 'm', 'Decay photons')
    pRes = plotResiduals(2, peternnnll, peterResults, 'k', 'PeTeR')
    wRes = plotResiduals(3, wv, wvResults, 'b', 'W.Vogelsang')
    jRes = plotResiduals(4, jpnlo, jpResults, 'g', 'JETPHOX')
    aRes = plotResiduals(5, pwggamma, pwgResults, 'r', 'PWG-GA')
    plt.subplot(326)
    plt.axis('off')
    plt.legend(handles=[dRes, pRes, wRes, jRes, aRes], numpoints=1, loc=2)

# plot rgamma
if doplotrgamma:
    plt.figure(3)
    plt.subplot(121)
    plt.plot(fitplotx, peterResults['rgamma'], 'k-', label='PeTeR')
    plt.plot(fitplotx, wvResults['rgamma'], 'b-', label='W.Vogelsang')
    plt.plot(fitplotx, jpResults['rgamma'], 'g-', label='JETPHOX')
    plt.plot(fitplotx, pwgResults['rgamma'], 'r-', label='PWG-GA')
    plt.xlabel('pT [GeV]')
    plt.ylabel('$R_\gamma$')
    plt.ylim([0.9, 1.35])
    plt.legend(loc=2)

    plt.subplot(122)
    allRgamma = [peterResults['rgamma'], wvResults['rgamma'], jpResults['rgamma'], pwgResults['rgamma']]
    rgammaCenter = numpy.average(allRgamma, 0)
    rgammaMin = numpy.amin(allRgamma, 0)
    rgammaMax = numpy.amax(allRgamma, 0)
    rgammaDecErrMin = numpy.multiply(rgammaCenter, 0.9)
    rgammaDecErrMax = numpy.multiply(rgammaCenter, 1.1)

    plt.plot(fitplotx, rgammaCenter, 'w-')
    plt.fill_between(fitplotx, rgammaDecErrMin, rgammaDecErrMax, color='darkgrey', label='Approx decay photon uncertainty (10%)')
    plt.fill_between(fitplotx, rgammaMin, rgammaMax, color='maroon', label='Theory uncertainty')

    plt.xlabel('pT [GeV]')
    plt.ylabel('$R_\gamma$')
    plt.ylim([0.9, 1.35])
    plt.legend(loc=2)

plt.show()