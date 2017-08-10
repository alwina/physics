import csv
import math

# this centralizes the code used to read the csv files produced by makeInvariantSpectra.py
# the outputs are dictionaries whose values can be directly used with pyplot
# although it's not a csv, it also includes the code needed to get the same kinds of dictionaries for parameterized meson tsallis functions

def _convert(filename, minPt, maxPt):
    def inRange(pt):
        return minPt < pt and maxPt > pt

    plotdata = {}
    with open(filename) as f:
        reader = csv.DictReader(f, dialect='excel-tab')
        for row in reader:
            if not inRange(float(row['pt'])):
                continue
            for header, value in row.items():
                try:
                    plotdata[header].append(float(value))
                except KeyError:
                    plotdata[header] = [float(value)]
    return plotdata

def mesondecays(filename, minPt, maxPt):
    return _convert(filename, minPt, maxPt)

def peter(filename, minPt, maxPt):
    plotdata = _convert(filename, minPt, maxPt)
    plotdata['dsigmaerr'] = [plotdata['scale+'], plotdata['scale-']]
    return plotdata

def vogelsang(filename, minPt, maxPt):
    plotdata = _convert(filename, minPt, maxPt)
    plotdata['totalerr'] = [plotdata['totalerrhigh'], plotdata['totalerrlow']]
    plotdata['directerr'] = [plotdata['directerrhigh'], plotdata['directerrlow']]
    # add keys to make it consistent with everything else
    plotdata['dsigma'] = plotdata['total']
    plotdata['dsigmaerr'] = plotdata['totalerr']
    return plotdata

def pwgga(filename, minPt, maxPt):
    return _convert(filename, minPt, maxPt)

def pythia(filename, minPt, maxPt):
    plotdata = _convert(filename, minPt, maxPt)
    plotdata['pterr'] = map(lambda x: x/2, plotdata['ptBinWidth'])
    return plotdata

def jetphox(filename, minPt, maxPt):
    plotdata = _convert(filename, minPt, maxPt)
    plotdata['pterr'] = map(lambda x: x/2, plotdata['ptBinWidth'])
    return plotdata

def mesonTsallis(ptValues, tsallisparams, sigmamb):
    def tsallis(pt):
        A = tsallisparams["A"]
        n = tsallisparams["n"]
        T = tsallisparams["T"]
        m = tsallisparams["m"]
        return sigmamb*A/(2*math.pi)*(n-1)*(n-2)/(n*T*(n*T+m*(n-2)))*math.pow(1+(math.sqrt(m**2+pt**2)-m)/(n*T), -n)

    plotdata = {}
    plotdata['pt'] = ptValues
    plotdata['dsigma'] = map(tsallis, ptValues)
    return plotdata