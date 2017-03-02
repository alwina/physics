// main92.cc is a part of the PYTHIA event generator.
// Copyright (C) 2017 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// This is a simple test program.
// Modified by Rene Brun and Axel Naumann to put the Pythia::event
// into a TTree.

// Header file to access Pythia 8 program elements.
#include "Pythia8/Pythia.h"

// ROOT, for saving Pythia events as trees in a file.
#include "TTree.h"
#include "TFile.h"

using namespace Pythia8;

int main(int argc, char* argv[]) {
  // make the number of events a command line argument or 100 by default
  int nev = 100;
  if (argc == 2) {
    nev = atoi(argv[1]);
  }

  Pythia pythia;
  pythia.readString("WeakSingleBoson:ffbar2gmZ = on");
  pythia.readString("23:oneChannel = 1 1.0 0 11 -11");
  pythia.readString("Beams:eCM = 13000.");
  pythia.init();

  Event& event = pythia.event;

  // set up the ROOT TFile and TTree.
  TFile *file = TFile::Open("~/root/z2eetree.root","recreate");
  auto tout = new TTree("Z2eeTree","Z2ee tree");

  // set up variables and branches
  Float_t zPt, zEta, zY, zPhi, zEnergy;
  Float_t emPt, emEta, emY, emPhi, emEnergy;
  Float_t epPt, epEta, epY, epPhi, epEnergy;

  tout->Branch("zPt", &zPt, "zPt/F");
  tout->Branch("zEta", &zEta, "zEta/F");
  tout->Branch("zY", &zY, "zY/F");
  tout->Branch("zPhi", &zPhi, "zPhi/F");
  tout->Branch("zEnergy", &zEnergy, "zEnergy/F");
  tout->Branch("emPt", &emPt, "emPt/F");
  tout->Branch("emEta", &emEta, "emEta/F");
  tout->Branch("emY", &emY, "emY/F");
  tout->Branch("emPhi", &emPhi, "emPhi/F");
  tout->Branch("emEnergy", &emEnergy, "emEnergy/F");
  tout->Branch("epPt", &epPt, "epPt/F");
  tout->Branch("epEta", &epEta, "epEta/F");
  tout->Branch("epY", &epY, "epY/F");
  tout->Branch("epPhi", &epPhi, "epPhi/F");
  tout->Branch("epEnergy", &epEnergy, "epEnergy/F");

 // Begin event loop. Generate event; skip if generation aborted.
  for (int iEvent = 0; iEvent < nev; ++iEvent) {
    if (!pythia.next()) continue;

    // find the first Z boson in the event
    int iFirstZ = -1;
    int np = event.size();
    for (int ip = 0; ip < np; ++ip) {
      if (event[ip].id() == 23) {
        iFirstZ = ip;
        break;
      }
    }

    // go through the daughters of the Zs until the e+/e- pair is found
    bool doSearch = true;
    int iCurrentZ = iFirstZ;
    int iLoopBreaker = 0;
    while (doSearch && iLoopBreaker < np) {
      // get the indices of the daughters at the current z index
      int i1 = event[iCurrentZ].daughter1();
      int i2 = event[iCurrentZ].daughter2();

      if (i1 == i2) {
        // the Z scattered and we need to look at the next one
        iCurrentZ = i1;
        // also, make sure this doesn't accidentally run infinitely
        iLoopBreaker++;
      } else {
        // the Z decayed and we found the e+/e-
        doSearch = false;

        // fill the Z kinematic data
        zPt = event[iCurrentZ].pT();
        zY = event[iCurrentZ].y();
        zEta = event[iCurrentZ].eta();
        zPhi = event[iCurrentZ].phi();
        zEnergy = event[iCurrentZ].e();

        // fill the e+/e- kinematic data after figuring out which is which
        if (event[i1].id() == 11) {
          emPt = event[i1].pT();
          emY = event[i1].y();
          emEta = event[i1].eta();
          emPhi = event[i1].phi();
          emEnergy = event[i1].e();

          epPt = event[i2].pT();
          epY = event[i2].y();
          epEta = event[i2].eta();
          epPhi = event[i2].phi();
          epEnergy = event[i2].e();
        } else {
          epPt = event[i1].pT();
          epY = event[i1].y();
          epEta = event[i1].eta();
          epPhi = event[i1].phi();
          epEnergy = event[i1].e();

          emPt = event[i2].pT();
          emY = event[i2].y();
          emEta = event[i2].eta();
          emPhi = event[i2].phi();
          emEnergy = event[i2].e();
        }

        tout->Fill();
      }
    }
    
  // End event loop.
  }

  // Statistics on event generation.
  pythia.stat();

  //  Write tree.
  tout->Write();
  file->Close();
  delete file;

  // Done.
  return 0;
}