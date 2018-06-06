import { Component, AfterViewInit, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { SearchInputComponent } from '../search/input.component';
import { NameListComponent } from '../cred/name-list.component';
import { NameResult } from '../data-types';
import { NameSearchClient } from '../search/name-search.client';
import { SearchResults } from '../search/results.model';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'app-home',
  templateUrl: '../../themes/_active/home/home.component.html',
  styleUrls: ['../../themes/_active/home/home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy, AfterViewInit {

  @ViewChild('searchInput') search: SearchInputComponent;
  @ViewChild('nameList') nameList: NameListComponent;
  protected _results: SearchResults<NameResult>;
  protected _searching = false;
  protected _sub: Subscription;
  public inited = true;
  public recordCounts = {orgs: 100, certs: 900};

  constructor(
    private _searchClient: NameSearchClient,
  ) {}

  ngOnInit() {
    this._searchClient.init();
    this._sub = this._searchClient.subscribe(this._receiveStatus.bind(this));
  }

  ngAfterViewInit() {
    this.search.focus();
  }

  ngOnDestroy() {
    this._sub.unsubscribe();
  }

  get names(): NameResult[] {
    return this._results && this._results.rows;
  }

  get results(): SearchResults<NameResult> {
    return this._results;
  }

  get searching(): boolean {
    return this._searching;
  }

  protected _receiveStatus(loading: boolean) {
    this._results = this._searchClient.results;
    this._searching = loading;
  }

  updateQuery(value: string) {
    if(value !== null && value.length) {
      this._searchClient.updateParams({query: value});
      this._searchClient.performSearch();
    } else {
      this._searchClient.clearSearch();
    }
  }

}
