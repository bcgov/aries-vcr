import { Component, AfterViewInit, Input, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SearchInputComponent } from './input.component';
import { SearchResults, SearchInfo } from './results.model';
import { Subscription } from 'rxjs/Subscription';
import { CredListComponent } from '../cred/list.component';
import { CredentialResult } from '../data-types';
import { CredSearchClient } from './cred-search.client';

@Component({
  selector: 'app-search',
  templateUrl: '../../themes/_active/search/form.component.html',
  styleUrls: ['../../themes/_active/search/form.component.scss']
})
export class SearchComponent implements OnInit, OnDestroy, AfterViewInit {

  @ViewChild('searchInput') _searchInput: SearchInputComponent;
  @ViewChild('credList') _nameList: CredListComponent;
  protected _curQuery: string;
  protected _filterType: string;
  protected _results: SearchResults<CredentialResult>;
  protected _searching = false;
  protected _searchSub: Subscription;
  protected _typeSub: Subscription;
  public inited = true;

  constructor(
    private _searchClient: CredSearchClient,
    private _route: ActivatedRoute,
    private _router: Router,
  ) {}

  ngOnInit() {
    this._searchClient.init();
    this._searchSub = this._searchClient.subscribe(this._receiveStatus.bind(this));
    this._typeSub = this._route.params.subscribe(params => {
      this.filterType = params['filterType'];
    });
  }

  ngAfterViewInit() {
    this._route.queryParams.subscribe(params => {
      this._searchInput.value = params['query'];
      this._curQuery = this._searchInput.value;
      if(! this._curQuery.length) {
        this._searchInput.focus();
      }
      setTimeout(this.updateQuery.bind(this), 50);
    });
  }

  ngOnDestroy() {
    this._searchSub.unsubscribe();
    this._typeSub.unsubscribe();
  }


  get error(): string {
    return this._searchClient && this._searchClient.error;
  }

  get filterType(): string {
    return this._filterType;
  }

  @Input() set filterType(filter: string) {
    this._filterType = filter;
    //this._searchInput.value = '';
    this.updateQuery();
  }

  get creds(): CredentialResult[] {
    return this._results && this._results.rows;
  }

  get results(): SearchResults<CredentialResult> {
    return this._results;
  }

  get resultInfo(): SearchInfo {
    return this._results && this._results.info;
  }

  get searching(): boolean {
    return this._searching;
  }

  protected _receiveStatus(loading: boolean) {
    this._results = this._searchClient.results;
    this._searching = loading;
  }

  /*setFilterType(filter: string) {
    this._router.navigate(['../', filter]);
  }*/

  public handleNav(nav: string) {
    this._searchClient.clearSearch();
    if (nav === 'previous') {
      this._searchClient.previousPage();
    } else if (nav == 'next') {
      this._searchClient.nextPage();
    } else {
      console.warn(`Invalid nav '${nav}' received`);
      this._searchClient.clearSearch();
    }
    this._searchClient.performSearch();
  }

  public updateQuery() {
    if(! this._searchInput) return;
    this._searchClient.pageNum = 1;
    let value = this._searchInput.value;
    if(this._curQuery !== value) {
      this._router.navigate([], { relativeTo: this._route, queryParams: {query: value }, queryParamsHandling: 'merge' });
      return;
    }
    if(value !== null && value.length) {
      this._searchClient.updateParams({query: value, filter: this.filterType});
      this._searchClient.performSearch();
    } else {
      this._searchClient.clearSearch();
    }
  }

}
