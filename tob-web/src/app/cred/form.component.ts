import { Component, OnInit, OnDestroy } from '@angular/core';
import { GeneralDataService } from 'app/general-data.service';
import { ActivatedRoute } from '@angular/router';
import { CredResult, IssuerResult, NameResult, PersonResult, ContactResult, CategoryResult, AddressResult, TopicResult, CredentialResult } from '../data-types';
import { CredentialClient } from '../search/cred.client';
import { SearchResult } from '../search/results.model';
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
  // record: CredResult;
  error: string;
  verifyStatus: string;
  verifyResult: any;
  verifying: boolean = false;

  private _cred: SearchResult<CredentialResult>;

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


  get record(): CredentialResult {
    return this._cred && this._cred.data;
  }

  get people(): PersonResult[] {
    return this.record && this.record.people && this.record.people.length ? this.record.people : [];
  }

  get contacts(): ContactResult[] {
    return this.record && this.record.contacts && this.record.contacts.length ? this.record.contacts : [];
  }

  get addresses(): AddressResult[] {
    return this.record && this.record.addresses && this.record.addresses.length ? this.record.addresses : [];
  }
  get topics(): TopicResult[] {
    return this.record && this.record.topics && this.record.topics.length ? this.record.topics : [];
  }

  get categories(): CategoryResult[] {
    return this.record && this.record.categories && this.record.categories.length ? this.record.categories : [];
  }

  get names(): NameResult[] {
    return this.record && this.record.names && this.record.names.length ? this.record.names : [];
  }

  get issuer(): IssuerResult {
    return this.record && this.record.issuer ? this.record.issuer : null;
  }

  protected _receiveCred(loading: boolean) {
    console.log(this._credClient.result)
    this._cred = this._credClient.result;
    if (this._cred) this.loaded = true;
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
