import matplotlib.pyplot as plt
from standardppbspectra import *

plt.figure()
# direct photon spectra
plt.errorbar(peternnnll['pt'], peternnnll['dsigma'], peternnnll['dsigmaerr'], fmt='ks--', label='PeTeR NNNLL', markerfacecolor='none', markeredgecolor='k')
plt.errorbar(wv['pt'], wv['total'], wv['totalerr'], fmt='bd--', label='W.Vogelsang calculation', markerfacecolor='none', markeredgecolor='b')
plt.plot(pwggamma['pt'], pwggamma['dsigma'], 'r+--', label='PWG-GA prompt photons')
plt.errorbar(jpnlo['pt'], jpnlo['dsigma'], jpnlo['dsigmaerr'], jpnlo['pterr'], fmt='g.', label='JETPHOX NLO (direct+frag)')
# decay photon spectra
plt.errorbar(sharkfin['pt'], sharkfin['dsigma'], sharkfin['dsigmaerr'], sharkfin['pterr'], fmt='mo:', label='Sharkfin decay photons (pi0 + eta)')
plt.errorbar(pygamma['pt'], pygamma['dsigma'], pygamma['dsigmaerr'], pygamma['pterr'], fmt='cx', label='PYTHIA decay photons (pi0)')
# meson spectra
plt.plot(piontsallis['pt'], piontsallis['dsigma'], 'y-', label='Measured pi0 (parameterized Tsallis)')
plt.plot(etatsallis['pt'], etatsallis['dsigma'], '-', color='orange', label='Measured eta (parameterized Tsallis)')
plt.errorbar(pypion['pt'], pypion['dsigma'], pypion['dsigmaerr'], pypion['pterr'], fmt='.', color='indigo', label='PYTHIA pi0')
plt.plot(pwgpion['pt'], pwgpion['dsigma'], 'r*-', label='PWG-GA pi0', markerfacecolor='none', markeredgecolor='r')

plt.yscale('log')
plt.title('Photon and meson invariant cross sections')
plt.xlabel('pT [GeV]')
plt.ylabel('Invariant cross section [pb/GeV^2]')
plt.legend(numpoints=1, fontsize='small')

plt.show()