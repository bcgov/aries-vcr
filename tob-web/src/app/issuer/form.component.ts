import { Component, OnInit, OnDestroy } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { Fetch, Model } from '../data-types';
import { GeneralDataService } from '../general-data.service';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'issuer-form',
  templateUrl: '../../themes/_active/issuer/form.component.html',
  styleUrls: ['../../themes/_active/issuer/form.component.scss']
})
export class IssuerFormComponent implements OnInit, OnDestroy {
  id: number;
  loaded: boolean;
  loading: boolean;
  credentialTypesLoaded: boolean;

  private _loader = new Fetch.ModelLoader(Model.Issuer);
  private _credTypes = new Fetch.ModelListLoader(Model.IssuerCredentialType);
  private _idSub: Subscription;

  constructor(
    private _dataService: GeneralDataService,
    private _route: ActivatedRoute,
    private _sanitizer: DomSanitizer,
  ) { }

  ngOnInit() {
    this._loader.stream.subscribe(result => {
      this.loaded = result.loaded;
      this.loading = result.loading;
      if(this.loaded) {
        this._dataService.loadList(this._credTypes, {parentId: this.id});
      }
    });
    this._credTypes.stream.subscribe(result => {
      this.credentialTypesLoaded = result.loaded;
    });
    this._idSub = this._route.params.subscribe(params => {
      this.id = +params['issuerId'];
      this._dataService.loadRecord(this._loader, this.id);
    });
  }

  ngOnDestroy() {
    this._idSub.unsubscribe();
    this._loader.complete();
    this._credTypes.complete();
  }

  get result() {
    return this._loader.result;
  }

  get record(): Model.Issuer {
    return this.result.data;
  }

  get error(): string {
    if(this.result.error && ! this.result.notFound) {
      return this.result.error.display;
    }
  }

  get credentialTypeRecords(): Model.IssuerCredentialType[] {
    return this._credTypes.result.data;
  }

  get safeImg() {
    if(this.record.logo_b64) {
      let src = 'data:image/*;base64,' + this.record.logo_b64;
      return this._sanitizer.bypassSecurityTrustUrl(src);
    }
  }

}
