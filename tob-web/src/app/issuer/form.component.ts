import { Component, OnInit, OnDestroy } from '@angular/core';
import { GeneralDataService } from 'app/general-data.service';
import { ActivatedRoute } from '@angular/router';
import { CredTypeResult, IssuerResult } from '../data-types';
import { CredTypeSearchClient } from '../search/cred-type-search.client';
import { SearchResults } from '../search/results.model';
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
  private _credTypes: SearchResults<CredTypeResult>;
  private _credTypesLoading: boolean = false;
  private _credTypeSub: Subscription;
  private _idSub: Subscription;

  constructor(
    private _dataService: GeneralDataService,
    private _route: ActivatedRoute,
    private _credTypeSearch: CredTypeSearchClient) { }

  ngOnInit() {
    this._credTypeSearch.init();
    this._credTypeSub = this._credTypeSearch.subscribe(this._credTypesUpdate.bind(this));
    this._idSub = this._route.params.subscribe(params => {
      this.id = +params['issuerId'];
      this._dataService.loadJson('assets/testdata/issuers.json', {t: new Date().getTime()})
        .subscribe((result) => {
          this.record = (new IssuerResult()).load(result[0]);
          this.loaded = true;

          this._credTypeSearch.updateParams({issuerId: this.id});
          this._credTypeSearch.performSearch();
        });
    });
  }

  ngOnDestroy() {
    this._idSub.unsubscribe();
  }

  get credTypes(): CredTypeResult[] {
    return this._credTypes && this._credTypes.rows;
  }

  get credTypesLoading(): boolean {
    return this._credTypesLoading;
  }

  protected _credTypesUpdate(loading: boolean) {
    this._credTypesLoading = loading;
    this._credTypes = this._credTypeSearch.results;
  }

}
