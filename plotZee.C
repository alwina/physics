void plotZee()
{
	// set up branches
	TBranch *zPtBranch, *zEtaBranch, *zYBranch, *zPhiBranch, *zEnergyBranch;
	TBranch *emPtBranch, *emEtaBranch, *emYBranch, *emPhiBranch, *emEnergyBranch;
	TBranch *epPtBranch, *epEtaBranch, *epYBranch, *epPhiBranch, *epEnergyBranch;

	Float_t zPt, zEta, zY, zPhi, zEnergy;
	Float_t emPt, emEta, emY, emPhi, emEnergy;
	Float_t epPt, epEta, epY, epPhi, epEnergy;

	TFile *f = TFile::Open("~/root/z2eetree.root");
	if (f == 0) {
		printf("Error: cannot open file\n");
		return;
	}

	TTree *tree = (TTree *)f->Get("Z2eeTree");

	tree->SetMakeClass(1);

	tree->SetBranchAddress("zPt", &zPt, &zPtBranch);
	tree->SetBranchAddress("zEta", &zEta, &zEtaBranch);
	tree->SetBranchAddress("zY", &zY, &zYBranch);
	tree->SetBranchAddress("zPhi", &zPhi, &zPhiBranch);
	tree->SetBranchAddress("zEnergy", &zEnergy, &zEnergyBranch);
	tree->SetBranchAddress("emPt", &emPt, &emPtBranch);
	tree->SetBranchAddress("emEta", &emEta, &emEtaBranch);
	tree->SetBranchAddress("emY", &emY, &emYBranch);
	tree->SetBranchAddress("emPhi", &emPhi, &emPhiBranch);
	tree->SetBranchAddress("emEnergy", &emEnergy, &emEnergyBranch);
	tree->SetBranchAddress("epPt", &epPt, &epPtBranch);
	tree->SetBranchAddress("epEta", &epEta, &epEtaBranch);
	tree->SetBranchAddress("epY", &epY, &epYBranch);
	tree->SetBranchAddress("epPhi", &epPhi, &epPhiBranch);
	tree->SetBranchAddress("epEnergy", &epEnergy, &epEnergyBranch);

	// create Z histograms
	TH1F* incZPtH = new TH1F("incZPtH", "p_{t} of Z", 25, 0., 50.);
	TH1F* incZYH = new TH1F("incZYH", "y of Z", 25, -8., 8.);
	TH1F* incZPhiH = new TH1F("incZPhiH", "#phi of Z", 25, -3.1416, 3.1416);
	TH1F* cutZPtH = new TH1F("cutZPtH", "p_{t} of Z", 25, 0., 50.);
	TH1F* cutZYH = new TH1F("cutZYH", "y of Z", 25, -8., 8.);
	TH1F* cutZPhiH = new TH1F("cutZPhiH", "#phi of Z", 25, -3.1416, 3.1416);
	TH1F* accZPtH = new TH1F("accZPtH", "p_{t} of Z", 25, 0., 50.);
	TH1F* accZYH = new TH1F("accZYH", "y of Z", 25, -8., 8.);
	TH1F* accZPhiH = new TH1F("accZPhiH", "#phi of Z", 25, -3.1416, 3.1416);

	// create e histograms
	TH1F* incePtH = new TH1F("incePtH", "p_{t} of e", 25, 0., 50.);
	TH1F* inceEtaH = new TH1F("inceEtaH", "#eta of e", 25, -8., 8.);
	TH1F* incePhiH = new TH1F("incePhiH", "#phi of e", 25, -3.1416, 3.1416);
	TH1F* cutePtH = new TH1F("cutePtH", "p_{t} of e", 25, 0., 50.);
	TH1F* cuteEtaH = new TH1F("cuteEtaH", "#eta of e", 25, -8., 8.);
	TH1F* cutePhiH = new TH1F("cutePhiH", "#phi of e", 25, -3.1416, 3.1416);
	TH1F* accePtH = new TH1F("accePtH", "p_{t} of e", 25, 0., 50.);
	TH1F* acceEtaH = new TH1F("acceEtaH", "#eta of e", 25, -8., 8.);
	TH1F* accePhiH = new TH1F("accePhiH", "#phi of e", 25, -3.1416, 3.1416);

	// make cuts and fill histograms
	Long64_t nev = tree->GetEntries();
	for (Int_t i = 0; i < nev; i++) {
		// load data for each entry
		zPtBranch->GetEntry(i);
		// zEtaBranch->GetEntry(i);
		zYBranch->GetEntry(i);
		zPhiBranch->GetEntry(i);
		// zEnergyBranch->GetEntry(i);
		emPtBranch->GetEntry(i);
		emEtaBranch->GetEntry(i);
		// emYBranch->GetEntry(i);
		emPhiBranch->GetEntry(i);
		emEnergyBranch->GetEntry(i);
		epPtBranch->GetEntry(i);
		epEtaBranch->GetEntry(i);
		// epYBranch->GetEntry(i);
		epPhiBranch->GetEntry(i);
		epEnergyBranch->GetEntry(i);

		// fill histograms that always get filled
		incZPtH->Fill(zPt);
		incZYH->Fill(zY);
		incZPhiH->Fill(zPhi);

		incePtH->Fill(emPt);
		incePtH->Fill(epPt);
		inceEtaH->Fill(emEta);
		inceEtaH->Fill(epEta);
		incePhiH->Fill(emPhi);
		incePhiH->Fill(epPhi);

		// fill histograms only if, for both electrons, energy > 5 and |eta| < 0.9
		if (emEnergy > 5. && epEnergy > 5.) {
			if (-0.9 < emEta && emEta < 0.9) {
				if (-0.9 < epEta && epEta < 0.9) {
					cutZPtH->Fill(zPt);
					cutZYH->Fill(zY);
					cutZPhiH->Fill(zPhi);

					cutePtH->Fill(emPt);
					cutePtH->Fill(epPt);
					cuteEtaH->Fill(emEta);
					cuteEtaH->Fill(epEta);
					cutePhiH->Fill(emPhi);
					cutePhiH->Fill(epPhi);
				}
			}
		}
	}

	// take ratios
	accZPtH->Divide(cutZPtH, incZPtH);
	accZYH->Divide(cutZYH, incZYH);
	accZPhiH->Divide(cutZPhiH, incZPhiH);
	accePtH->Divide(cutePtH, incePtH);
	acceEtaH->Divide(cuteEtaH, inceEtaH);
	accePhiH->Divide(cutePhiH, incePhiH);

	// this cross section came from 250,000 events
	// the luminosity used is 4 pb^-1
	// perhaps one day I'll figure out how to save this to the tree as well
	Float_t scale = 48500*4./nev;
	incZPtH->Scale(scale);
	incZYH->Scale(scale);
	incZPhiH->Scale(scale);
	incePtH->Scale(scale);
	inceEtaH->Scale(scale);
	incePhiH->Scale(scale);
	cutZPtH->Scale(scale);
	cutZYH->Scale(scale);
	cutZPhiH->Scale(scale);
	cutePtH->Scale(scale);
	cuteEtaH->Scale(scale);
	cutePhiH->Scale(scale);

	// ********************************************************
	// Everything below this line is just to make various plots
	// ********************************************************

	// save plots as pngs
	TImage *img = TImage::Create();

	// plotplotplotplotplot
	TCanvas* zStats = new TCanvas("zStats", "Z statistics", 800, 800);
	zStats->Divide(3,3);

	zStats->cd(1);
	gPad->SetLogy();
	incZPtH->Draw();
	incZPtH->SetXTitle("Z p_{T} [GeV/c]");
	incZPtH->SetYTitle("dN/dp_{T}");

	zStats->cd(2);
	gPad->SetLogy();
	cutZPtH->Draw();
	cutZPtH->SetXTitle("Z p_{T} [GeV/c]");
	cutZPtH->SetYTitle("dN/dp_{T}");

	zStats->cd(3);
	gPad->SetLogy();
	accZPtH->Draw();
	accZPtH->SetXTitle("Z p_{T} [GeV/c]");
	accZPtH->SetYTitle("dN/dp_{T}");

	zStats->cd(4);
	gPad->SetLogy();
	incZYH->Draw();
	incZYH->SetXTitle("Z y");
	incZYH->SetYTitle("dN/dy");

	zStats->cd(5);
	gPad->SetLogy();
	cutZYH->Draw();
	cutZYH->SetXTitle("Z y");
	cutZYH->SetYTitle("dN/dy");

	zStats->cd(6);
	gPad->SetLogy();
	accZYH->Draw();
	accZYH->SetXTitle("Z y");
	accZYH->SetYTitle("dN/dy");

	zStats->cd(7);
	incZPhiH->Draw();
	incZPhiH->SetXTitle("Z_#phi");
	incZPhiH->SetYTitle("dN/d#phi");
	incZPhiH->SetMinimum(0);

	zStats->cd(8);
	cutZPhiH->Draw();
	cutZPhiH->SetXTitle("Z_#phi");
	cutZPhiH->SetYTitle("dN/d#phi");
	cutZPhiH->SetMinimum(0);

	zStats->cd(9);
	accZPhiH->Draw();
	accZPhiH->SetXTitle("Z_#phi");
	accZPhiH->SetYTitle("dN/d#phi");
	accZPhiH->SetMinimum(0);

	// plotplotplotplotplot
	TCanvas* eStats = new TCanvas("eStats", "e statistics", 800, 800);
	eStats->Divide(3,3);

	eStats->cd(1);
	gPad->SetLogy();
	incePtH->Draw();
	incePtH->SetXTitle("e p_{T} [GeV/c]");
	incePtH->SetYTitle("dN/dp_{T}");

	eStats->cd(2);
	gPad->SetLogy();
	cutePtH->Draw();
	cutePtH->SetXTitle("e p_{T} [GeV/c]");
	cutePtH->SetYTitle("dN/dp_{T}");

	eStats->cd(3);
	gPad->SetLogy();
	accePtH->Draw();
	accePtH->SetXTitle("e p_{T} [GeV/c]");
	accePtH->SetYTitle("dN/dp_{T}");

	eStats->cd(4);
	gPad->SetLogy();
	inceEtaH->Draw();
	inceEtaH->SetXTitle("e_#eta");
	inceEtaH->SetYTitle("dN/d#eta");

	eStats->cd(5);
	gPad->SetLogy();
	cuteEtaH->Draw();
	cuteEtaH->SetXTitle("e_#eta");
	cuteEtaH->SetYTitle("dN/d#eta");

	eStats->cd(6);
	gPad->SetLogy();
	acceEtaH->Draw();
	acceEtaH->SetXTitle("e_#eta");
	acceEtaH->SetYTitle("dN/d#eta");

	eStats->cd(7);
	incePhiH->Draw();
	incePhiH->SetXTitle("e_#phi");
	incePhiH->SetYTitle("dN/d#phi");
	incePhiH->SetMinimum(0);

	eStats->cd(8);
	cutePhiH->Draw();
	cutePhiH->SetXTitle("e_#phi");
	cutePhiH->SetYTitle("dN/d#phi");
	cutePhiH->SetMinimum(0);

	eStats->cd(9);
	accePhiH->Draw();
	accePhiH->SetXTitle("e_#phi");
	accePhiH->SetYTitle("dN/d#phi");
	accePhiH->SetMinimum(0);

	// smaller plotplotplotplotplot
	TCanvas *zPtPlots = new TCanvas("zPtPlots", "Z pT plots", 1500, 600);
	zPtPlots->Divide(3,1);

	zPtPlots->cd(1);
	gPad->SetLogy();
	incZPtH->Draw();
	zPtPlots->cd(2);
	gPad->SetLogy();
	cutZPtH->Draw();
	zPtPlots->cd(3);
	gPad->SetLogy();
	accZPtH->Draw();

	img->FromPad(zPtPlots);
	img->WriteImage("zPtPlots.png");

	TCanvas *zYPlots = new TCanvas("zYPlots", "Z y plots", 1500, 600);
	zYPlots->Divide(3,1);

	zYPlots->cd(1);
	gPad->SetLogy();
	incZYH->Draw();
	zYPlots->cd(2);
	gPad->SetLogy();
	cutZYH->Draw();
	zYPlots->cd(3);
	gPad->SetLogy();
	accZYH->Draw();

	img->FromPad(zYPlots);
	img->WriteImage("zYPlots.png");

	TCanvas *zPhiPlots = new TCanvas("zPhiPlots", "Z Phi plots", 1500, 600);
	zPhiPlots->Divide(3,1);

	zPhiPlots->cd(1);
	incZPhiH->Draw();
	zPhiPlots->cd(2);
	cutZPhiH->Draw();
	zPhiPlots->cd(3);
	accZPhiH->Draw();

	img->FromPad(zPhiPlots);
	img->WriteImage("zPhiPlots.png");

	// smaller plotplotplotplotplot
	TCanvas *ePtPlots = new TCanvas("ePtPlots", "e pT plots", 1500, 600);
	ePtPlots->Divide(3,1);

	ePtPlots->cd(1);
	gPad->SetLogy();
	incePtH->Draw();
	ePtPlots->cd(2);
	gPad->SetLogy();
	cutePtH->Draw();
	ePtPlots->cd(3);
	gPad->SetLogy();
	accePtH->Draw();

	img->FromPad(ePtPlots);
	img->WriteImage("ePtPlots.png");

	TCanvas *eEtaPlots = new TCanvas("eEtaPlots", "e Eta plots", 1500, 600);
	eEtaPlots->Divide(3,1);

	eEtaPlots->cd(1);
	gPad->SetLogy();
	inceEtaH->Draw();
	eEtaPlots->cd(2);
	gPad->SetLogy();
	cuteEtaH->Draw();
	eEtaPlots->cd(3);
	gPad->SetLogy();
	acceEtaH->Draw();

	img->FromPad(eEtaPlots);
	img->WriteImage("eEtaPlots.png");

	TCanvas *ePhiPlots = new TCanvas("ePhiPlots", "e Phi plots", 1500, 600);
	ePhiPlots->Divide(3,1);

	ePhiPlots->cd(1);
	incePhiH->Draw();
	ePhiPlots->cd(2);
	cutePhiH->Draw();
	ePhiPlots->cd(3);
	accePhiH->Draw();

	img->FromPad(ePhiPlots);
	img->WriteImage("ePhiPlots.png");
}