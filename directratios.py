import matplotlib.pyplot as plt
import numpy
from standardppbspectra import *

def getJetphoxRatio(jpdir, jpfrag):
    jptotal = [sum(x) for x in zip(jpdir['dsigma'], jpfrag['dsigma'])]
    return numpy.divide(jpdir['dsigma'], jptotal)

peterratio = numpy.divide(peterlo['dsigma'], peternnnll['dsigma'])
wvratio = numpy.divide(wv['direct'], wv['total'])
jpratio = getJetphoxRatio(jpdir, jpfrag)
jpiso1ratio = getJetphoxRatio(jpiso1dir, jpiso1frag)
jpiso2ratio = getJetphoxRatio(jpiso2dir, jpiso2frag)
jpiso4ratio = getJetphoxRatio(jpiso4dir, jpiso4frag)

# non-fragmentation ratio plots
plt.figure(1)
plt.plot(peterlo['pt'], peterratio, 'ko-', label='PeTeR LO/NNNLL')
plt.plot(wv['pt'], wvratio, 'bo-', label='W.Vogelsang calculations direct/total')
plt.plot(jpdir['pt'], jpratio, 'go-', label='JETPHOX (no iso) direct/direct+frag (LO+NLO)')
plt.plot(jpiso1dir['pt'], jpiso1ratio, 'co-', label='JETPHOX (iso R=0.1) direct/direct+frag (LO+NLO)')
plt.plot(jpiso2dir['pt'], jpiso2ratio, 'mo-', label='JETPHOX (iso R=0.2) direct/direct+frag (LO+NLO)')
plt.plot(jpiso4dir['pt'], jpiso4ratio, 'ro-', label='JETPHOX (iso R=0.4) direct/direct+frag (LO+NLO)')

plt.xlabel('pT [GeV]')
plt.xlim([minPt-1, maxPt+1])
# plt.ylim([0,1])
plt.legend(numpoints=1, loc=4)

# cross-check jetphox isolation cuts
plt.figure(2)
plt.plot(jpdir['pt'], jpdir['dsigma'], 'go', label="no iso, direct", markerfacecolor='none', markeredgecolor='g')
plt.plot(jpiso1dir['pt'], jpiso1dir['dsigma'], 'co', label="R=0.1, direct", markerfacecolor='none', markeredgecolor='c')
plt.plot(jpiso2dir['pt'], jpiso2dir['dsigma'], 'mo', label="R=0.2, direct", markerfacecolor='none', markeredgecolor='m')
plt.plot(jpiso4dir['pt'], jpiso4dir['dsigma'], 'ro', label="R=0.4, direct", markerfacecolor='none', markeredgecolor='r')
plt.plot(jpfrag['pt'], jpfrag['dsigma'], 'g+', label="no iso, frag")
plt.plot(jpiso1frag['pt'], jpiso1frag['dsigma'], 'c+', label="R=0.1, frag")
plt.plot(jpiso2frag['pt'], jpiso2frag['dsigma'], 'm+', label="R=0.2, frag")
plt.plot(jpiso4frag['pt'], jpiso4frag['dsigma'], 'r+', label="R=0.4, frag")

plt.yscale('log')
plt.xlabel('pT [GeV]')
plt.ylabel('Invariant cross section [pb/GeV^2]')
plt.legend(numpoints=1, fontsize='small')

plt.show()