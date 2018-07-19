import { Component, OnInit, OnDestroy } from '@angular/core';
import { GeneralDataService } from 'app/general-data.service';
import { ActivatedRoute } from '@angular/router';
import { CredTypeResult, IssuerResult } from '../data-types';
import { IssuerClient } from '../search/issuer.client';
import { SearchResult } from '../search/results.model';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'issuer-form',
  templateUrl: '../../themes/_active/issuer/form.component.html',
  styleUrls: ['../../themes/_active/issuer/form.component.scss']
})
export class IssuerFormComponent implements OnInit, OnDestroy {
  id: number;
  loaded: boolean;
  record: IssuerResult;
  error: string;
  private _credTypes: SearchResult<CredTypeResult>;
  private _credTypesLoading: boolean = false;
  private _credTypeSub: Subscription;
  private _idSub: Subscription;
  private _issuerSub: Subscription;

  constructor(
    private _dataService: GeneralDataService,
    private _route: ActivatedRoute,
    private _issuerClient: IssuerClient) { }

  ngOnInit() {
    this._idSub = this._route.params.subscribe(params => {
      this.id = +params['issuerId'];
      this._issuerSub = this._issuerClient.subscribe(this._receiveIssuer.bind(this))
      this._issuerClient.getById(this.id);

      // this._dataService.loadJson('assets/testdata/issuers.json', {t: new Date().getTime()})
      //   .subscribe((result) => {
      //     this.record = (new IssuerResult()).load(result[0]);
      //     this.loaded = true;

      //     this._credTypeSearch.updateParams({issuerId: this.id});
      //     this._credTypeSearch.performSearch();
      //   });
    });
  }

  ngOnDestroy() {
    this._idSub.unsubscribe();
    this._issuerSub.unsubscribe();
  }

  get issuerLoading(): boolean {
    // return this._credTypesLoading;
    return true;
  }

  get credTypesLoading(): boolean {
    // return this._credTypesLoading;
    return true;
  }

  // protected _credTypesUpdate(loading: boolean) {
  //   this._credTypesLoading = loading;
  //   this._credTypes = this._credTypeSearch.results;
  // }

  protected _receiveIssuer(loading: boolean) {
    if (!this._issuerClient.result) return;
    console.log(this._issuerClient.result.data)
    this.record = this._issuerClient.result.data;
    this.loaded = true;
    
  }

}
