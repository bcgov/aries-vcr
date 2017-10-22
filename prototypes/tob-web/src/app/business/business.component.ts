import { Component, OnInit, OnDestroy } from '@angular/core';
import { GeneralDataService } from 'app/general-data.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-business',
  templateUrl: './business.component.html',
  styleUrls: ['./business.component.scss']
})
export class BusinessComponent implements OnInit, OnDestroy {
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
    let loaded = this.dataService.preloadData(['voclaimtypes', 'voorgtypes', 'volocations']);
    this.sub = this.route.params.subscribe(params => {
      this.id = +params['recordId'];
      loaded.then(status => {
        this.dataService.loadVerifiedOrg(this.id).subscribe(record => {
          this.record = record;
          console.log('verified org:', record);
          this.loaded = !!record;
          if(! record) this.error = 'Record not found';
          else {
            let orgType = this.dataService.findOrgData('voorgtypes', record.orgTypeId);
            this.record.type = orgType || {};
            this.record.typeName = orgType && orgType.theType;
            this.dataService.loadFromApi('verifiedorgs/' + this.id + '/voclaims')
              .subscribe((res: any) => {
                let certs = [];
                let seen = {};
                for(var i = 0; i < res.length; i++) {
                  let cert = res[i];
                  if(! seen[cert.voClaimType]) {
                    cert.type = this.dataService.findOrgData('voclaimtypes', cert.voClaimType);
                    cert.color = ['green', 'orange', 'blue', 'purple'][cert.voClaimType % 4];
                    certs.push(cert);
                    seen[cert.voClaimType] = 1;
                  }
                }
                this.certs = certs;
                console.log('claims', res);
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
}
