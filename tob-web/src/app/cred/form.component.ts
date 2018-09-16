import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { GeneralDataService } from 'app/general-data.service';
import { Fetch, Model } from '../data-types';
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
  error: string;
  verifyStatus: string;
  verifying: boolean = false;

  private _loader = new Fetch.ModelLoader(Model.CredentialFormatted);
  private _verify = new Fetch.JsonLoader();
  private _idSub: Subscription;

  constructor(
    private _dataService: GeneralDataService,
    private _route: ActivatedRoute) { }

  ngOnInit() {
    this._loader.stream.subscribe(result => {
      this.loaded = result.loaded;
    });
    this._verify.stream.subscribe(result => {
      this.verifying = result.loading;
      if(result.error)
        this.verifyStatus = 'error';
      else if(result.loaded)
        this.verifyStatus = result.data.success ? 'success' : 'failure';
      else
        this.verifyStatus = null;
    });
    this._idSub = this._route.params.subscribe(params => {
      this.id = +params['credId'];
      this._dataService.loadRecord(this._loader, this.id);
    });
  }

  ngOnDestroy() {
    this._idSub.unsubscribe();
    this._loader.complete();
  }

  get result(): Fetch.BaseResult<Model.CredentialFormatted> {
    return this._loader.result;
  }

  get record(): Model.CredentialFormatted {
    return this.result.data;
  }

  get people(): Model.Person[] {
    return this.record && this.record.people && this.record.people.length ? this.record.people : [];
  }

  get contacts(): Model.Contact[] {
    return this.record && this.record.contacts && this.record.contacts.length ? this.record.contacts : [];
  }

  get addresses(): Model.Address[] {
    return this.record && this.record.addresses && this.record.addresses.length ? this.record.addresses : [];
  }

  get categories(): Model.Category[] {
    return this.record && this.record.categories && this.record.categories.length ? this.record.categories : [];
  }

  get names(): Model.Name[] {
    return this.record && this.record.names && this.record.names.length ? this.record.names : [];
  }

  get issuer(): Model.Issuer {
    return this.record && this.record.issuer ? this.record.issuer : null;
  }

  get topic(): Model.Topic {
    return this.record && this.record.topic;
  }

  get verifyResult(): object {
    let result = this._verify.result;
    let ret = null;
    if(result.error) {
      ret = result.formatError();
    } else {
      ret = JSON.stringify(result.data, null, 2);
    }
    return ret;
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
    this._dataService.loadData(this._verify, `credential/${this.id}/verify`);
  }
}
