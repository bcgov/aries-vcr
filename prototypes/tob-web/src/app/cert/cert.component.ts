import { Component, OnInit, OnDestroy } from '@angular/core';
import { GeneralDataService } from 'app/general-data.service';
import { ActivatedRoute } from '@angular/router';
import { VerifiableClaim, VerifiableClaimType, blankClaimType, VerifiableOrg,
  IssuerService, blankIssuerService } from '../data-types';

@Component({
  selector: 'app-cert',
  templateUrl: './cert.component.html',
  styleUrls: ['./cert.component.scss']
})
export class CertComponent implements OnInit {
  recordId: string;
  loaded: boolean;
  record: VerifiableClaim;
  others: VerifiableClaim[];
  error: string;
  sub: any;
  verifyStatus: string;
  verifyResult: any;
  verifying: boolean = false;
  private preload;

  constructor(
    private dataService: GeneralDataService,
    private route: ActivatedRoute) { }

  ngOnInit() {
    let loaded = this.preload = this.dataService.preloadData(['inactiveclaimreasons', 'issuerservices', 'verifiableclaimtypes']);
    this.sub = this.route.params.subscribe(params => {
      this.recordId = params['certId'];
      loaded.then(status => {
        this.dataService.loadRecord('verifiableclaims', this.recordId).subscribe((record : VerifiableClaim) => {
          let claim = this.dataService.formatClaim(record);
          console.log('vo claim:', claim);
          if (! claim) this.error = 'Record not found';
          else {
            this.dataService.loadVerifiableOrg(claim.verifiableOrgId)
              .subscribe((org : VerifiableOrg) => {
                console.log('org', org);
                claim.org = org;
                this.record = claim;
                if (org.claims) {
                  let others = [];
                  for (let idx = 0; idx < org.claims.length; idx++) {
                    if (org.claims[idx].claimType === claim.claimType && org.claims[idx].id !== claim.id) {
                      others.push(org.claims[idx]);
                    }
                  }
                  this.others = this.dataService.sortClaims(others);
                }
                this.loaded = !!claim;
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

  verifyClaim(evt) {
    this.verifying = true;
    this.preload.then((_) => {
      this.dataService.verifyClaim(this.recordId).then((data : any) => {
        this.verifyStatus = data.success ? 'success' : 'failure';
        this.verifyResult = JSON.stringify(data, null, 2);
        this.verifying = false;
      }, (err) => {
        this.verifyStatus = 'error';
        if(err._body) {
          let body = JSON.parse(err._body);
          if(body && body.detail)
            err = body.detail;
        }
        this.verifyResult = err;
        this.verifying = false;
      });
    });
  }

}
