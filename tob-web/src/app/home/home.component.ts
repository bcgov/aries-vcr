import { Component, AfterViewInit, OnInit, OnDestroy, ViewChild } from '@angular/core';
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

  @ViewChild('searchInput') search: SearchInputComponent;
  @ViewChild('topicList') nameList: TopicListComponent;
  protected _results: SearchResults<TopicResult>;
  protected _searching = false;
  protected _sub: Subscription;
  public inited = true;
  public recordCounts = {orgs: 0, certs: 0};
  public filterType = 'name';

  constructor(
    private _searchClient: TopicSearchClient,
    private _dataService: GeneralDataService
  ) {}

  ngOnInit() {
    this._searchClient.init();
    this._sub = this._searchClient.subscribe(this._receiveStatus.bind(this));
    this._dataService.quickLoad().then(() => {
      this.recordCounts.orgs = this._dataService.getRecordCount('topic')
      this.recordCounts.certs = this._dataService.getRecordCount('credential')
    })
  }

  ngAfterViewInit() {
    this.search.focus();
  }

  ngOnDestroy() {
    this._sub.unsubscribe();
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
    this.search.value = '';
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

}
