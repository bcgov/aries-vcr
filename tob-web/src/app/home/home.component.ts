import { Component, AfterViewInit, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SearchInputComponent } from '../search/input.component';
import { GeneralDataService } from 'app/general-data.service';
import { TopicListComponent } from '../cred/topic-list.component';
import { TopicResult } from '../data-types';
import { TopicSearchClient } from '../search/topic-search.client';
import { SearchResults } from '../search/results.model';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'app-home',
  templateUrl: '../../themes/_active/home/home.component.html',
  styleUrls: ['../../themes/_active/home/home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy, AfterViewInit {

  @ViewChild('searchInput') _searchInput: SearchInputComponent;
  @ViewChild('topicList') nameList: TopicListComponent;
  protected _results: SearchResults<TopicResult>;
  protected _searching = false;
  protected _sub: Subscription;
  public inited = false;
  public loadError = null;
  public recordCounts = {orgs: 0, certs: 0};
  public filterType = 'name';

  constructor(
    private _searchClient: TopicSearchClient,
    private _dataService: GeneralDataService,
    private _route: ActivatedRoute,
    private _router: Router,
  ) {}

  ngOnInit() {
    this._searchClient.init();
    this._sub = this._searchClient.subscribe(this._receiveStatus.bind(this));
    this._dataService.quickLoad().catch(err => {
      console.log('?');
      this.loadError = err;
      this.inited = true;
    }).then((loaded) => {
      if(loaded) {
        this.recordCounts.orgs = this._dataService.getRecordCount('topic');
        this.recordCounts.certs = this._dataService.getRecordCount('credential');
      }
      this.inited = true;
      setTimeout(() => this.focus(), 50);
    });
  }

  ngAfterViewInit() {
    this.focus();
  }

  ngOnDestroy() {
    this._sub.unsubscribe();
  }

  focus() {
    if(this._searchInput) this._searchInput.focus();
  }

  get topics(): TopicResult[] {
    return this._results && this._results.rows;
  }

  get results(): SearchResults<TopicResult> {
    return this._results;
  }

  get searching(): boolean {
    return this._searching;
  }

  protected _receiveStatus(loading: boolean) {
    this._results = this._searchClient.results;
    this._searching = loading;
  }

  setFilterType(filter: string) {
    this.filterType = filter;
    this._searchClient.clearSearch();
    this._searchInput.value = '';
    return false;
  }

  updateQuery(value: string) {
    if(value !== null && value.length) {
      this._searchClient.updateParams({query: value, filter: this.filterType});
      this._searchClient.performSearch();
    } else {
      this._searchClient.clearSearch();
    }
  }

  performSearch(value: string) {
    value = this._searchInput.value;
    this._router.navigate(['../search/name'], {relativeTo: this._route, queryParams: {query: value}});
  }

}
