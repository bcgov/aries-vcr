import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TopicResult, NameResult, CredentialResult } from '../data-types';
import { TopicClient } from '../search/topic.client';
import { TopicCredClient } from '../search/topic-cred.client';
import { SearchResult, SearchResults } from '../search/results.model';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'topic-form',
  templateUrl: '../../themes/_active/topic/form.component.html',
  styleUrls: ['../../themes/_active/topic/form.component.scss']
})
export class TopicFormComponent implements OnInit, OnDestroy {
  id: number;
  loaded: boolean;
  loading: boolean;
  credsFormat: string = 'rows';
  filterActive: string = 'true';
  showFilters: boolean = false;

  private _topic: SearchResult<TopicResult>;
  private _topicError: any;
  private _topicLoading: boolean;

  private _creds: SearchResults<CredentialResult>;
  private _credsError: any;
  private _credsLoading: boolean;

  private _idSub: Subscription;
  private _topicSub: Subscription;
  private _topicCredsSub: Subscription;

  constructor(
    private _route: ActivatedRoute,
    private _router: Router,
    private _topicClient: TopicClient,
    private _topicCredClient: TopicCredClient) { }

  ngOnInit() {
    this._topicSub = this._topicClient.subscribe(this._receiveTopic.bind(this))
    this._topicCredsSub = this._topicCredClient.subscribe(this._receiveCreds.bind(this))
    this._idSub = this._route.params.subscribe(params => {
      this.loading = true;
      this.id = +params['topicId'];
      this._topicClient.getRelatedById(this.id);
      this._topicCredClient.getRelatedById(this.id);
    });
  }

  get title(): string {
    if(this._topic && this._topic.data.names && this._topic.data.names.length) {
      return this._topic.data.names[0].text;
    }
  }

  get names(): NameResult[] {
    return this._topic && this._topic.data.names;
  }

  get topic(): TopicResult {
    return this._topic && this._topic.data;
  }

  get error(): string {
    if(this._topicError && ! this.notFound) {
      return this._topicError.display;
    }
  }

  get notFound(): boolean {
    return (this._topicError && this._topicError.obj.status === 404);
  }

  get creds(): CredentialResult[] {
    return this._creds && this._creds.rows;
  }

  protected _receiveTopic(loading: boolean) {
    this._topic = this._topicClient.result;
    this._topicError = this._topicClient.error;
    this._topicLoading = loading;
    this.loaded = !! this._topic;
    this.loading = false;
  }

  protected _receiveCreds(loading: boolean) {
    this._creds = this._topicCredClient.results;
    this._credsError = this._topicCredClient.error;
    this._credsLoading = loading;
  }

  ngOnDestroy() {
    this._topicSub.unsubscribe();
    this._idSub.unsubscribe();
    this._topicCredsSub.unsubscribe();
  }
}
