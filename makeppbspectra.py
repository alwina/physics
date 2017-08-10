import csv
import numpy
from math import pi, sqrt
from rootpy.io import root_open

# this takes the raw files and converts them to a standard (tab-separated) csv format
# it also makes any and all modifications needed to get pPb invariant cross sections (e.g. dividing by 2*pi*pt, multiplying by 208, etc)

outputDirectory = 'ppbspectra/'
pbscale = 208
doRunMain = True
doRunExtra = True

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def processMesonSharkfin(etaFilename, pionFilename, outputFilename):
    with open(etaFilename, 'r') as etaFile, open(pionFilename, 'r') as pionFile, open(outputDirectory + outputFilename, 'w') as outputFile:
        fieldnames = ['pt', 'pterr', 'dsigma', 'dsigmaerr']
        writer = csv.DictWriter(outputFile, fieldnames, dialect='excel-tab')
        writer.writeheader()

        etareader = csv.DictReader(etaFile, dialect='excel-tab')
        pionreader = csv.DictReader(pionFile, dialect='excel-tab')

        for eta, pion in zip(etareader, pionreader):
            row = {}
            row['pt'] = eta['pt']
            row['pterr'] = eta['pterr']
            row['dsigma'] = float(eta['dsigma']) + float(pion['dsigma'])
            row['dsigmaerr'] = sqrt(float(eta['dsigmaerr'])**2 + float(pion['dsigmaerr'])**2)
            writer.writerow(row)

def processPeTeR(inputFilename, outputFilename):
    with open(inputFilename, 'r') as inputFile, open(outputDirectory + outputFilename, 'w') as outputFile:
        # set up the output as a tab-separated file
        fieldnames = ['pt', 'dsigma', 'scale+', 'scale-']
        writer = csv.DictWriter(outputFile, fieldnames, dialect='excel-tab')
        writer.writeheader()

        for line in inputFile:
            # read the rapidity ranges from the output of PeTeR directly
            if line.startswith('min-rapidity'):
                minEta = float(line[13:])
                continue
            elif line.startswith('max-rapidity'):
                maxEta = float(line[13:])
                continue

            data = line.split()
            if not data or not isNumber(data[0]):
                continue
            pt = float(data[0])
            invscale = pbscale/(2*pi*pt*(maxEta-minEta))
            dsigma = invscale*float(data[1])
            errhigh = invscale*float(data[5])
            errlow = -invscale*float(data[6])

            writer.writerow({'pt': pt, 'dsigma': dsigma, 'scale+': errhigh, 'scale-': errlow})

def processVogelsang(inputFilename, outputFilename):
    with open(inputFilename, 'r') as inputFile, open(outputDirectory + outputFilename, 'w') as outputFile:
        # set up the output as a tab-separated file
        fieldnames = ['pt', 'total', 'totalerrhigh', 'totalerrlow', 'direct', 'directerrhigh', 'directerrlow']
        writer = csv.DictWriter(outputFile, fieldnames, dialect='excel-tab')
        writer.writeheader()

        totaldata, directdata = [], []
        alllines = inputFile.readlines()
        for lines in zip(alllines[3:60], alllines[63:120], alllines[123:180]):
            # this will give the values grouped by column, i.e. a tuple of pT, a tuple of 3 direct values, etc
            data = zip(*map(lambda l: l.split(), lines))
            pt = float(data[2][0])
            totaldata = map(lambda x: pbscale*float(x), data[5])
            directdata = map(lambda x: pbscale*float(x), data[3])

            total = numpy.median(totaldata)
            totalerrlow = numpy.median(totaldata) - numpy.min(totaldata)
            totalerrhigh = numpy.max(totaldata) - numpy.median(totaldata)
            direct = numpy.median(directdata)
            directerrlow = numpy.median(directdata) - numpy.min(directdata)
            directerrhigh = numpy.max(directdata) - numpy.median(directdata)

            writer.writerow({'pt': pt, 'total': total, 'totalerrlow': totalerrlow, 'totalerrhigh': totalerrhigh, 'direct': direct, 'directerrlow': directerrlow, 'directerrhigh': directerrhigh})

def processPwgga(inputFilename, outputFilename):
    with open(inputFilename, 'r') as inputFile, open(outputDirectory + outputFilename, 'w') as outputFile:
        fieldnames = ['pt', 'dsigma']
        writer = csv.DictWriter(outputFile, fieldnames, dialect='excel-tab')
        writer.writeheader()

        for line in inputFile:
            data = line.split()
            pt = float(data[0])
            dsigma = 10**3*pbscale*float(data[1])/(2*pi*pt)

            writer.writerow({'pt': pt, 'dsigma': dsigma})

def processPythia(nBins, ptRange, deltay, rootFilename, sigmaFilename, gammaOutputFilename, pionOutputFilename):
    with open(sigmaFilename) as f:
        sigma = float(f.readline())*10**9 # pb
        nEvents = int(f.readline())
    tosigma = sigma/nEvents

    with root_open(rootFilename) as rootFile:
        pionPt, gammaPt = [], []
        for event in rootFile.Pi0GammaTree:
            pionPt.append(event.pionPt)
            gammaPt.append(event.gamma1Pt)
            gammaPt.append(event.gamma2Pt)

    def writeFile((hist, binEdges), outputFilename):
        with open(outputDirectory + outputFilename, 'w') as outputFile:
            fieldnames = ['pt', 'ptBinWidth', 'dsigma', 'dsigmaerr']
            writer = csv.DictWriter(outputFile, fieldnames, dialect='excel-tab')
            writer.writeheader()

            for value, ptlow, pthigh in zip(hist, binEdges[:-1], binEdges[1:]):
                pt = 0.5*(ptlow+pthigh)
                ptBinWidth = pthigh-ptlow
                invscale = pbscale*tosigma/(2*pi*pt*deltay*ptBinWidth)
                dsigma = value*invscale
                dsigmaerr = sqrt(value)*invscale

                writer.writerow({'pt': pt, 'ptBinWidth': ptBinWidth, 'dsigma': dsigma, 'dsigmaerr': dsigmaerr})

    writeFile(numpy.histogram(gammaPt, nBins, ptRange), gammaOutputFilename)
    writeFile(numpy.histogram(pionPt, nBins, ptRange),pionOutputFilename)


def processJetphox(inputFilename, outputFilename, eta):
    with open(inputFilename, 'r') as inputFile, open(outputDirectory + outputFilename, 'w') as outputFile:
        fieldnames = ['pt', 'ptBinWidth', 'dsigma', 'dsigmaerr']
        writer = csv.DictWriter(outputFile, fieldnames, dialect='excel-tab')
        writer.writeheader()

        # skip the header
        inputFile.readline()
        for line in inputFile:
            data = line.split()
            pt = float(data[1])
            invscale = pbscale/(2*pi*pt*2*eta)
            ptBinWidth = float(data[2]) - float(data[0])
            dsigma = invscale*float(data[3])
            dsigmaerr = invscale*float(data[4])

            writer.writerow({'pt': pt, 'ptBinWidth': ptBinWidth, 'dsigma': dsigma, 'dsigmaerr': dsigmaerr})

def runMain():
    processMesonSharkfin('tsallis/etadecayphotons.dat', 'tsallis/piondecayphotons.dat', 'decay-sharkfin.dat')
    processPeTeR('peter/ct10nlo/peterout3.txt', 'peter-nnnll.dat')
    processPeTeR('peter/ct10nlo/peterout0.txt', 'peter-lo.dat')
    processVogelsang('wvogelsang/alice_5023.dat', 'vogelsang.dat')
    processPwgga('alicetheory/datTOTALgamma5-1TeV.out', 'pwgga-gamma.dat')
    processPwgga('alicetheory/datTOTALpi0pp5-1TeV.out', 'pwgga-pion.dat')
    processPythia(56, (2,30), 1.6, 'pythia/decayphotons.root', 'pythia/sigma.txt', 'pythia-gamma.dat', 'pythia-pion.dat')

    processJetphox('jetphox/ppbins/nlo.dat', 'jetphox-nlo.dat', 0.27)
    processJetphox('jetphox/ppbins/dir.dat', 'jetphox-dir.dat', 0.27)
    processJetphox('jetphox/ppbins/frag.dat', 'jetphox-frag.dat', 0.27)
    processJetphox('jetphox/ppiso4bins/dir.dat', 'jetphox-iso4-dir.dat', 0.27)
    processJetphox('jetphox/ppiso4bins/frag.dat', 'jetphox-iso4-frag.dat', 0.27)
    processJetphox('jetphox/ppiso2bins/dir.dat', 'jetphox-iso2-dir.dat', 0.47)
    processJetphox('jetphox/ppiso2bins/frag.dat', 'jetphox-iso2-frag.dat', 0.47)
    processJetphox('jetphox/ppiso1bins/dir.dat', 'jetphox-iso1-dir.dat', 0.57)
    processJetphox('jetphox/ppiso1bins/frag.dat', 'jetphox-iso1-frag.dat', 0.57)

def runExtra():
    print 'Nothing extra defined'

if doRunMain:
    runMain()
if doRunExtra:
    runExtra()