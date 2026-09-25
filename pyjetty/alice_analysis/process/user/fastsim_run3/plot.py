#!/usr/bin/env python3
import ROOT

output_file="~/results.root"

ROOT.gStyle.SetStatH(0.0001)
ROOT.gStyle.SetStatW(0.0001)
ROOT.gStyle.SetOptFit(True)
ROOT.gStyle.SetOptStat(0)

c=ROOT.TCanvas("c","",1200,400)
c.Divide(3)

pTmins=  [20, 40, 60]

with ROOT.TFile(output_file,'read') as f:
    h_jet_det = f.Get("jet_pT_det")
    h_jet_gen = f.Get("jet_pT_gen")

    for i, pTmin in enumerate(pTmins):

        bin_num = i + 1

        njets_det = h_jet_det.GetBinContent(bin_num)
        njets_gen = h_jet_gen.GetBinContent(bin_num)

        print(f"\n{pTmin}-{pTmin+20} GeV")
        print(f"DET jets = {njets_det}")
        print(f"GEN jets = {njets_gen}")

        h_det = f.Get(
            f"EEC_det_{pTmin}_{pTmin+20}"
        ).Clone(f"h_det_{pTmin}")

        h_gen = f.Get(
            f"EEC_gen_{pTmin}_{pTmin+20}"
        ).Clone(f"h_gen_{pTmin}")

        #det per jet
        if njets_det > 0:
            h_det.Scale(1.0 / njets_det, "width")

        #gen per jet
        if njets_gen > 0:
            h_gen.Scale(1.0 / njets_gen, "width")

        #det / gen
        h_ratio = h_det.Clone(f"h_ratio_{pTmin}")
        h_ratio.Divide(h_gen)

        #graphing det
        c.cd(1)
        ROOT.gPad.SetLogx()

        h_det.SetTitle(
            f"DET EEC, {pTmin} < pT < {pTmin+20} GeV"
        )
        h_det.GetXaxis().SetTitle("EEC")
        h_det.GetYaxis().SetTitle(
            "#frac{1}{N_{jets}} #frac{dN}{dEEC}"
        )
        h_det.Draw("HIST")
        h_det.Draw("E1 SAME")
        
        #graphing gen
        c.cd(2)
        ROOT.gPad.SetLogx()

        h_gen.SetTitle(
            f"GEN EEC, {pTmin} < pT < {pTmin+20} GeV"
        )
        h_gen.GetXaxis().SetTitle("EEC")
        h_gen.GetYaxis().SetTitle(
            "#frac{1}{N_{jets}} #frac{dN}{dEEC}"
        )
        h_gen.Draw("HIST")
        h_gen.Draw("E1 SAME")

        #graphing det/gen
        c.cd(3)
        ROOT.gPad.SetLogx()

        h_ratio.SetTitle(
            f"DET / GEN, {pTmin} < pT < {pTmin+20} GeV"
        )
        h_ratio.GetXaxis().SetTitle("EEC")
        h_ratio.GetYaxis().SetTitle(
            "DET/GEN"
        )
        h_det.Draw("HIST")
        h_det.Draw("E1 SAME")

        line = ROOT.TLine(
            h_ratio.GetXaxis().GetXmin(), 1,
            h_ratio.GetXaxis().GetXmax(), 1
        )

        line.SetLineStyle(2)
        h_ratio.Draw("HIST")
        h_ratio.Draw("E1 SAME")

        # h_jet = f.Get("jet_pT_det")
        # njets = h_jet.GetBinContent(i+1)
        # print(njets)
        # c.cd(1)
        # h=f.Get(f"EEC_det_{pTmin}_{pTmin+20}")
        # h.Scale(1 / njets, "width")
        # ROOT.gPad.SetLogx()
        # h.Draw()

        # h_jet = f.Get("jet_pT_gen")
        # njets = h_jet.GetBinContent(i+1)
        # print(njets)
        # c.cd(2)
        # h=f.Get(f"EEC_gen_{pTmin}_{pTmin+20}")
        # h.Scale(1 / njets, "width")
        # ROOT.gPad.SetLogx()
        # h.Draw()

        # h_jet = f.Get("jet_pT_gen")
        # njets = h_jet.GetBinContent(i+1)
        # print(njets)
        # c.cd(2)
        # h=f.Get(f"EEC_gen_{pTmin}_{pTmin+20}")
        # h.Scale(1 / njets, "width")
        # ROOT.gPad.SetLogx()
        # h.Draw()

        c.SaveAs(f"plots_{pTmin}.pdf")