import { Component, OnInit, OnDestroy } from '@angular/core';
import { GeneralDataService } from 'app/general-data.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-cert',
  templateUrl: './cert.component.html',
  styleUrls: ['./cert.component.scss']
})
export class CertComponent implements OnInit {
  id: number;
  loaded: boolean;
  record: any;
  loc: any;
  certs: any[];
  error: string;
  sub: any;

  constructor(
    private dataService: GeneralDataService,
    private route: ActivatedRoute) { }

  ngOnInit() {
    let loaded = this.dataService.preloadData(['voclaimtypes', 'issuerservices']);
    this.sub = this.route.params.subscribe(params => {
      this.id = +params['recordId'];
      loaded.then(status => {
        this.dataService.loadRecord('voclaims', ''+this.id).subscribe(record => {
          record.color = ['green', 'orange', 'blue', 'purple'][record.voClaimType % 4];
          this.record = record;
          console.log('vo claim:', record);
          if(! record) this.error = 'Record not found';
          else {
            let claimType = this.dataService.findOrgData('voclaimtypes', record.voClaimType);
            this.record.type = claimType || {};
            if(claimType) {
              this.record.issuer = this.dataService.findOrgData('issuerservices', claimType.issuerOrgId);
            }
            this.dataService.loadVerifiedOrg(record.verifiedOrgId)
              .subscribe((res: any) => {
                console.log('org', res);
                this.record.org = res;
                this.loaded = !!record;
              });
          }
        }, err => {
          this.error = err;
        });
      });
    });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

  showVerify() {
    let div = document.getElementsByClassName('cert-verify');
    let time = 0;
    if(div.length) {
      let outer = <any>div[0];
      outer.style.display = 'block';
      let inner = outer.getElementsByClassName('verify-line');
      for(let i = 0; i < inner.length; i++) {
        let line = <any>inner[i];
        if(line.classList.contains('delay')) time += 500;
        setTimeout(() => line.classList.add('show'), time);
      }
    }
    let stat = document.getElementById('verify-status');
    if(stat) {
      setTimeout(() => (<any>stat).textContent = 'Verified', time);
    }
  }

}
