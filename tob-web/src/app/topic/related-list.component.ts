import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TopicResult } from '../data-types';
import { TopicRelatedClient } from '../search/topic-related.client';
import { TopicRelatedFromClient } from '../search/topic-related-from.client';
import { SearchResults } from '../search/results.model';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'related-topics',
  templateUrl: '../../themes/_active/topic/related-list.component.html',
})
export class TopicRelatedListComponent implements OnInit, OnDestroy {
  protected _topicId: number;
  protected _defaultFormat = 'cards';
  @Input() title: string;
  @Input('related-from') relatedFrom: boolean;
  loaded: boolean;
  loading: boolean;
  filterActive: string = 'true';

  private _results: SearchResults<TopicResult>;
  private _resultError: any;
  private _resultLoading: boolean;
  private _resultSub: Subscription;
  private _topicClient;

  constructor(
    private _route: ActivatedRoute,
    private _router: Router,
    private _topicToClient: TopicRelatedClient,
    private _topicFromClient: TopicRelatedFromClient) { }

  ngOnInit() {
  }

  @Input() set defaultFormat(fmt: string) {
    this._defaultFormat = fmt;
  }

  get defaultFormat(): string {
    return this._defaultFormat;
  }

  get format(): string {
    // switch to list for many records
    return this._defaultFormat;
  }

  get topicId(): number {
    return this._topicId;
  }

  @Input() set topicId(newId: number) {
    this._topicId = newId;
    this.performSearch();
  }

  get topics(): TopicResult[] {
    return this._results && this._results.rows;
  }

  get error(): string {
    if(this._resultError && ! this.notFound) {
      return this._resultError.display;
    }
  }

  get notFound(): boolean {
    return (this._resultError && this._resultError.obj.status === 404);
  }

  performSearch() {
    if(! this._topicClient) {
      this._topicClient = this.relatedFrom ? this._topicFromClient : this._topicToClient;
      this._resultSub = this._topicClient.subscribe(this._receiveTopics.bind(this));
    }
    if(this._topicId) {
      this._topicClient.getRelatedById(this._topicId);
    }
  }

  protected _receiveTopics(loading: boolean) {
    this._results = this._topicClient.results;
    this._resultError = this._topicClient.error;
    this._resultLoading = loading;
    this.loaded = !! this._results;
    this.loading = false;
  }

  ngOnDestroy() {
    this._resultSub.unsubscribe();
  }
}
