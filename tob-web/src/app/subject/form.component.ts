import { Component, OnInit, OnDestroy } from '@angular/core';
import { GeneralDataService } from 'app/general-data.service';
import { ActivatedRoute } from '@angular/router';
import { CredResult, SubjectResult } from '../data-types';
import { CredSearchClient } from '../search/cred-search.client';
import { SearchResults } from '../search/results.model';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'subject-form',
  templateUrl: '../../themes/_active/subject/form.component.html',
  styleUrls: ['../../themes/_active/subject/form.component.scss']
})
export class SubjectFormComponent implements OnInit, OnDestroy {
  id: number;
  loaded: boolean;
  record: SubjectResult;
  error: string;
  private _creds: SearchResults<CredResult>;
  private _credsLoaded: boolean;
  private _credsLoading: boolean;
  private _credSub: Subscription;
  private _idSub: Subscription;

  constructor(
    private _dataService: GeneralDataService,
    private _route: ActivatedRoute,
    private _credSearch: CredSearchClient) { }

  ngOnInit() {
    this._credSearch.init();
    this._credSub = this._credSearch.subscribe(this._credsUpdate.bind(this));
    this._idSub = this._route.params.subscribe(params => {
      this.id = +params['subjId'];
      this._dataService.loadJson('assets/testdata/subjects.json', {t: new Date().getTime()})
        .subscribe((result) => {
          this.record = (new SubjectResult()).load(result[0]);
          this.loaded = true;

          this._credSearch.updateParams({subjectId: this.id});
          this._credSearch.performSearch();
        });
    });
  }

  get creds(): CredResult[] {
    return this._creds && this._creds.rows;
  }

  get credsLoading(): boolean {
    return this._credsLoading;
  }

  protected _credsUpdate(loading: boolean) {
    this._credsLoading = loading;
    this._creds = this._credSearch.results;
  }

  ngOnDestroy() {
    this._credSub.unsubscribe();
    this._idSub.unsubscribe();
  }
}
