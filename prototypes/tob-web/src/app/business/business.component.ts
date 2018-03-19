import { Component, OnInit, OnDestroy } from '@angular/core';
import { GeneralDataService } from 'app/general-data.service';
import { ActivatedRoute } from '@angular/router';
import { Location, LocationType, VerifiableOrg, VerifiableOrgType, IssuerService, VerifiableClaim, VerifiableClaimType, DoingBusinessAs,
  blankLocation, blankOrgType, blankLocationType, blankIssuerService, blankClaimType } from '../data-types';

@Component({
  selector: 'app-business',
  templateUrl: '../../themes/_active/business/business.component.html',
  styleUrls: ['../../themes/_active/business/business.component.scss']
})
export class BusinessComponent implements OnInit, OnDestroy {
  id: number;
  loaded: boolean;
  record: VerifiableOrg;
  loc: any;
  dbas: DoingBusinessAs[];
  certs: any[];
  locations: Location[];
  error: string;
  sub: any;

  constructor(
    private dataService: GeneralDataService,
    private route: ActivatedRoute) { }

  ngOnInit() {
    let loaded = this.dataService.preloadData(['verifiableclaimtypes', 'verifiableorgtypes', 'locationtypes', 'issuerservices']);
    this.sub = this.route.params.subscribe(params => {
      this.id = +params['orgId'];
      loaded.then(status => {
        this.dataService.loadVerifiableOrg(this.id).subscribe((record : VerifiableOrg) => {
          if(! record) this.error = 'Record not found';
          else {
            let orgType = <VerifiableOrgType>this.dataService.findOrgData('verifiableorgtypes', record.orgTypeId);
            record.type = orgType || blankOrgType();
            record.typeName = orgType && orgType.description;

            let orgLocs = [];
            let claimLocs = {};
            if(record.locations) {
              for(var i = 0; i < record.locations.length; i++) {
                let loc = <Location>Object.assign({}, record.locations[i]);
                let locType = <LocationType>this.dataService.findOrgData('locationtypes', loc.locationTypeId);
                loc.type = locType || blankLocationType();
                loc.typeName = locType && locType.locType;
                if(loc.doingBusinessAsId) {
                  let cid = loc.doingBusinessAsId;
                  if(! claimLocs[cid]) claimLocs[cid] = [];
                  claimLocs[cid].push(loc);
                } else {
                  orgLocs.push(loc);
                }
              }
            }
            this.locations = orgLocs;
            console.log('locations', orgLocs);

            let dbas = [];
            if(Array.isArray(record.doingBusinessAs)) {
              for(var i = 0; i < record.doingBusinessAs.length; i++) {
                let dba = <DoingBusinessAs>Object.assign({}, record.doingBusinessAs[i]);
                dba.locations = claimLocs[dba.id] || [];
                dbas.push(dba);
              }
            }
            this.dbas = dbas;
            console.log('dbas', dbas);

            this.certs = this.dataService.formatClaims(record.claims);
            console.log('claims', this.certs);

            /*this.dataService.loadFromApi('verifiableorgs/' + this.id + '/voclaims')
              .subscribe((res: any) => {
                let certs = [];
                let seen = {};
                for(var i = 0; i < res.length; i++) {
                  let cert = res[i];
                  if(! seen[cert.voClaimType]) {
                    cert.type = this.dataService.findOrgData('verifiableclaimtypes', cert.voClaimType);
                    cert.color = ['green', 'orange', 'blue', 'purple'][cert.voClaimType % 4];
                    certs.push(cert);
                    seen[cert.voClaimType] = 1;
                  }
                }
                this.certs = certs;
                console.log('claims', res);
              });*/
          }

          console.log('verified org:', record);
          this.record = record;
          this.loaded = !!record;

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
