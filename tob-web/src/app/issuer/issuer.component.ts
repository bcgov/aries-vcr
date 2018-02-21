import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router} from '@angular/router';
import { GeneralDataService } from 'app/general-data.service';
import { IssuerService, VerifiableClaim, VerifiableClaimType } from '../data-types';

@Component({
  selector: 'app-issuer',
  templateUrl: './issuer.component.html',
  styleUrls: ['./issuer.component.scss']
})
export class IssuerComponent implements OnInit {

  public certId : string = '';
  public recordId : string = '';
  public record;
  public inited = false;
  public loading = false;
  public loaded = false;
  public claimTypes : VerifiableClaimType[] = [];
  public error;
  private preload;
  private sub;

  constructor(
    private dataService: GeneralDataService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit() {
    this.preload = this.dataService.preloadData();
    this.sub = this.route.params.subscribe(params => {
      this.certId = params['certId'];
      this.recordId = params['issuerId'];
      let fetch = this.preload;
      if(this.certId) {
        // get issuer ID from cert
        fetch = fetch.then(status => {
          return new Promise(resolve => {
            this.dataService.loadRecord('verifiableclaims', this.certId).subscribe((cert : VerifiableClaim) => {
              console.log('cert:', cert);
              let type = <VerifiableClaimType>this.dataService.findOrgData('verifiableclaimtypes', cert.claimType);
              console.log(type);
              if(type) {
                this.recordId = ''+type.issuerServiceId;
                resolve(status);
              }
            }, err => {
              this.error = err;
            });
          });
        });
      }
      fetch.then(status => {console.log('?');
        this.dataService.loadRecord('issuerservices', this.recordId).subscribe((record : IssuerService) => {
          console.log('issuer:', record);

          if(! record) this.error = 'Record not found';
          else {

            // scanning all claim types for this issuer at the moment
            let alltypes = this.dataService.getOrgData('verifiableclaimtypes') || [];
            let ctypes = [];
            alltypes.forEach((ctype : VerifiableClaimType) => {
              if(''+ctype.issuerServiceId === this.recordId)
                ctypes.push(ctype);
            });
            console.log(ctypes);
            this.claimTypes = ctypes;
          }

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
