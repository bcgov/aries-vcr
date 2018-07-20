import { Component, OnInit, OnDestroy } from '@angular/core';
import { GeneralDataService } from 'app/general-data.service';
import { ActivatedRoute } from '@angular/router';
import { CredResult, IssuerResult, NameResult } from '../data-types';
import { CredentialClient } from '../search/cred.client';
import { SearchResults } from '../search/results.model';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'cred-form',
  templateUrl: '../../themes/_active/cred/form.component.html',
  styleUrls: [
    '../../themes/_active/cred/cred.scss',
    '../../themes/_active/cred/form.component.scss']
})
export class CredFormComponent implements OnInit, OnDestroy {
  id: number;
  loaded: boolean;
  record: CredResult;
  error: string;
  verifyStatus: string;
  verifyResult: any;
  verifying: boolean = false;

  private _idSub: Subscription;
  private _credSub: Subscription;

  constructor(
    private _dataService: GeneralDataService,
    private _route: ActivatedRoute,
    private _credClient: CredentialClient) { }

  ngOnInit() {
    this._idSub = this._route.params.subscribe(params => {
      this.id = +params['credId'];

      this._credSub = this._credClient.subscribe(this._receiveCred.bind(this))
      this._credClient.getRelatedById(this.id);
    });
  }

  ngOnDestroy() {
    this._idSub.unsubscribe();
    this._credSub.unsubscribe();
  }

  // get issuer(): IssuerResult {
  //   return this.record && this.record.credentialType && this.record.credentialType.issuer;
  // }

  protected _receiveCred(loading: boolean) {
    console.log(this._credClient.result)
  }

  showVerify() {
    let div = document.getElementsByClassName('cred-verify');
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

  verifyCred(evt) {
    this.verifying = true;
    this._dataService.verifyCred(''+this.id).then((data : any) => {
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
  }
}
