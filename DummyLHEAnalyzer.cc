#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "FWCore/Utilities/interface/EDMException.h"
#include <iomanip>
#include <iostream>
#include <TH1F.h>
#include <TFile.h>
#include <string>
#include <iostream>

using namespace std;
using namespace edm;
using namespace lhef;

class DummyLHEAnalyzer : public EDAnalyzer {
private: 
  bool dumpLHE_;
  bool checkPDG_;
  TFile * output;
  TH1F* h_pdf;
  TH1F* h_scale;
public:
  explicit DummyLHEAnalyzer( const ParameterSet & cfg ) : 
    src_( cfg.getParameter<InputTag>( "src" ) ),
    fileName_(cfg.getUntrackedParameter<std::string>("histoutputFile")),
    filterProduction_(cfg.getParameter<int>("filterProduction")),
    filterhh_(cfg.getParameter<bool>("filterhh")),
    nTotal_(0),
    nPass_(0)
  {
    switch(filterProduction_){
    case 0: 
      std::cout << "Filtering mode = keeping all process" << std::endl;
      break;
    case 1:
      std::cout << "Filtering mode = keeping only gluon fusion" << std::endl;
      break;
    case 2:
      std::cout << "Filtering mode = keeping only q-qbar annihilation " << std::endl;
      break;
    default:
      std::cout << "Filtering mode = keeping all process" << std::endl;
      break;
    }
    std::cout << "Filtering hh = " << filterhh_ << std::endl;
  }
  void beginJob(){
    output = new TFile(fileName_.data(), "RECREATE");
    h_pdf = new TH1F("h_pdf","",100,0.0001,0.000015);
    h_pdf->SetXTitle("Weight");
    h_scale = new TH1F("h_scale","",100,0.0001,0.000015);
    h_scale->SetXTitle("Weight");
  }
private:
  double maxNum = 0.0, scaleNum=0.0;
  int count=0;
  std::vector<double> pdfVec[101];
  std::vector<double> scaleVec[9];
  double total_pdf[101] = {0.0};
  double total_scale[9] = {0.0};
  void analyze( const Event & iEvent, const EventSetup & iSetup ) override {

    Handle<LHEEventProduct> evt;
    Handle<GenEventInfoProduct> genEvtInfo; 
    iEvent.getByLabel( src_, evt );
    // edm::Handle<LHEEventProduct> EvtHandle ;
    // iEvent.getByLabel( theSrc , EvtHandle ) ;

    const lhef::HEPEUP hepeup_ = evt->hepeup();

    const int nup_ = hepeup_.NUP; 
    const std::vector<int> idup_ = hepeup_.IDUP;
    const std::vector<lhef::HEPEUP::FiveVector> pup_ = hepeup_.PUP;

    std::cout << "Number of particles = " << nup_ << std::endl;

    for ( unsigned int icount = 0 ; icount < (unsigned int)nup_; icount++ ) {

      std::cout << "# " << std::setw(14) << std::fixed << icount 
                << std::setw(14) << std::fixed << idup_[icount] 
                << std::setw(14) << std::fixed << (pup_[icount])[0] 
                << std::setw(14) << std::fixed << (pup_[icount])[1] 
                << std::setw(14) << std::fixed << (pup_[icount])[2] 
                << std::setw(14) << std::fixed << (pup_[icount])[3] 
                << std::setw(14) << std::fixed << (pup_[icount])[4] 
                << std::endl;
    }
    if( evt->weights().size() ) {
      std::cout << "weights:" << std::endl;
      for ( size_t iwgt = 0; iwgt < evt->weights().size(); ++iwgt ) {
        // if (evt->weights()[iwgt].id == "111") std::cout<<"YYY"<<std::endl;

    const LHEEventProduct::WGT& wgt = evt->weights().at(iwgt);

    /********  scale uncertainty *******/
    if(std::stoi((wgt.id).c_str())>=1 && std::stoi((wgt.id).c_str())<=9){
      std::cout << "\t" << wgt.id << ' ' 
          << std::scientific << wgt.wgt << std::endl;
      for(int i=0;i<9;i++){
        if(std::stoi((wgt.id).c_str())==i+1){
            scaleVec[i].push_back(wgt.wgt);
        }
      }
    }
    /******** pdf uncertainty ********/
    if(std::stoi((wgt.id).c_str())>=111 && std::stoi((wgt.id).c_str())<=211){
      // h_pdf->Fill(wgt.wgt);
      std::cout << "\t" << wgt.id << ' ' 
          << std::scientific << wgt.wgt << std::endl;
      for(int i=0;i<101;i++){
        if(std::stoi((wgt.id).c_str())==i+111){
            pdfVec[i].push_back(wgt.wgt);
        }
      }
    }

      }//iwgt
    }//event.size()

    for(int id=0; id<9; id++){
      for(size_t event=0; event< scaleVec[0].size(); event++){
        total_scale[id] += scaleVec[id][event];
      }
    }
    count++;

    for(int id=0; id<101; id++){
      for(size_t event=0; event< pdfVec[0].size(); event++){
        total_pdf[id] += pdfVec[id][event];
      }
    }
    if(count==1000){
    for(int _id=0; _id<101;_id++){
      h_pdf->Fill(total_pdf[_id]);
    }
    for(int _id=0; _id<9;_id++){
      h_scale->Fill(total_scale[_id]);
    } 
    } 
  }//analyze()
  
  void endJob(){
    output->cd();
    h_scale->Write();
    h_pdf->Write();
    output->Write();
    output->Close();
  }

  InputTag src_;
  std::string fileName_;
  int filterProduction_; // 0: all, 1: gluon only, 2: DY only
  bool filterhh_;
  long int nTotal_;
  long int nPass_;
};

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE( DummyLHEAnalyzer );


