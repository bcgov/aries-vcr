import { Component, OnInit, OnDestroy, AfterViewInit, ChangeDetectionStrategy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AppConfigService } from 'app/app-config.service';
import { GeneralDataService } from 'app/general-data.service';
import { Fetch, Model } from '../data-types';
import { Subscription } from 'rxjs';
import { TimelineFormatterService } from './timeline-formatter.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'cred-form',
  templateUrl: '../../themes/_active/cred/form.component.html',
  styleUrls: [
    '../../themes/_active/cred/cred.scss',
    '../../themes/_active/cred/form.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CredFormComponent implements OnInit, OnDestroy, AfterViewInit {
  id: number;
  claimsVisible: boolean = true;
  proofVisible: boolean = true;
  mode: string = 'view';
  _timelineRange: any;
  _timelineRows: any;
  _verifyLoading = true;

  private _loader = new Fetch.ModelLoader(Model.CredentialFormatted);
  private _verify = new Fetch.ModelLoader(Model.CredentialVerifyResult);
  private _idSub: Subscription;

  constructor(
    private _config: AppConfigService,
    private _dataService: GeneralDataService,
    private _route: ActivatedRoute,
    private _formatter: TimelineFormatterService,
    private _httpClient: HttpClient,
  ) { }

  ngOnInit() {
    this._idSub = this._route.params.subscribe(params => {
      this.id = +params['credId'];
      this.mode = this._route.snapshot.data.verify ? 'verify' : 'view';
      this._dataService.loadRecord(this._loader, this.id, {primary: true});
    });
  }

  ngAfterViewInit() {
    this._loader.ready.subscribe(result => {
        this.updateRows();
        // auto-verify unless button is present
        let verify = this._config.getConfig().AUTO_VERIFY_CRED;
        if(verify === undefined || (verify && verify !== "false"))
          this.verifyCred();
    });
  }

  ngOnDestroy() {
    this._idSub.unsubscribe();
    this._loader.complete();
    this._verify.complete();
  }

  get result() {
    return this._loader.result;
  }

  get result$() {
    return this._loader.stream;
  }

  get verify$() {
    return this._verify.stream;
  }

  get verifyLoading() {
    return this._verifyLoading;
  }

  toggleShowClaims(evt?) {
    this.claimsVisible = !this.claimsVisible;
    if(evt) evt.preventDefault();
  }

  toggleShowProof(evt?) {
    this.proofVisible = !this.proofVisible;
    if(evt) evt.preventDefault();
  }

  delay(ms: number) {
      return new Promise( resolve => setTimeout(resolve, ms) );
  }

  async verifyCred(evt?) {
    if(this.result.data.revoked) {
      this._verify.reset();
    } else {
      // this is now 2 steps (in v3 api) - first to initiate the proof request
      let verify_req_url = "/api/v3/credential/" + this.id + "/verify";
      let verify_proof_req = await this._httpClient.get(verify_req_url).toPromise();

      let proof_exch_id;
      if ("presentation_exchange" in verify_proof_req) {
        let proof_exch = verify_proof_req["presentation_exchange" as keyof typeof verify_proof_req];
        if ("presentation_exchange_id" in proof_exch) {
          proof_exch_id = proof_exch["presentation_exchange_id" as keyof typeof proof_exch];
        }
      }

      // ... and then in a loop, check for proof request result
      let initial_delay = 1000;
      let delay_factor = 2;
      let max_delay = 8000;
      let delay = initial_delay;
      let waiting_for_proof = true;
      while (waiting_for_proof) {
        await this.delay(delay);
        let verify_url = verify_req_url + "/" + proof_exch_id;
        let verify_proof = await this._httpClient.get(verify_url).toPromise();

        if ("state" in verify_proof) {
          let verify_proof_state = verify_proof["state" as keyof typeof verify_proof];
          if (verify_proof_state === "verified") {
            waiting_for_proof = false;
          }
        }

        // backoff on the delay interval each loop
        delay = Math.min(max_delay, delay * delay_factor);
      }

      // finally call our data load service on the verification result
      this._dataService.loadRecord(this._verify, this.id, {"extPath": "verify/" + proof_exch_id});
      this._verifyLoading = false;
    }
  }

  updateRows() {
    let rows = [];
    let cred = <Model.Credential>this.result.data;
    let credset: Model.CredentialSet = cred.credential_set;
    let start = new Date();
    start.setFullYear(start.getFullYear() - 1);
    let end = new Date();
    end.setFullYear(end.getFullYear() + 1);
    let range = {start: start.toISOString(), end: end.toISOString()};
    if(credset) {
      if(credset.first_effective_date && credset.first_effective_date < range.start) {
        if (credset.first_effective_date < '0100-01-01') {
          //range.start = '';
        } else {
          range.start = credset.first_effective_date;
        }
      }
      if(credset.last_effective_date && credset.last_effective_date > range.end) {
        range.end = credset.last_effective_date;
      }
      let row = {
        id: `set-${credset.id}`,
        slots: []
      };
      for(let cred of credset.credentials) {
        if(!cred.effective_date || cred.effective_date < "0100-01-01") {
          // skip for timeline
        } else {
          if(cred.effective_date && cred.effective_date < range.start) {
            range.start = cred.effective_date;
          }
          row.slots.push(this._formatter.getCredentialSlot(cred));
        }
      }
      rows.push(row);
      this._timelineRange = range;
      this._timelineRows = rows;
    }
  }

  get timelineRange() {
    return this._timelineRange;
  }

  get timelineRows() {
    return this._timelineRows;
  }

}
