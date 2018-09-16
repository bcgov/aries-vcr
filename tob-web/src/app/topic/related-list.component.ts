import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GeneralDataService } from '../general-data.service';
import { Fetch, Model } from '../data-types';
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
  @Input('records') inputRecords: Model.Topic[];
  loaded: boolean;
  loading: boolean;
  filterActive: string = 'true';

  private _loader: Fetch.ModelListLoader<Model.Topic>;

  constructor(
    private _dataService: GeneralDataService,
    private _route: ActivatedRoute,
    private _router: Router,
  ) {}

  ngOnInit() {
    this._loader = new Fetch.ModelListLoader(
      this.relatedFrom ? Model.TopicRelatedFrom : Model.TopicRelatedTo);
    this._loader.stream.subscribe(result => {
      this.loading = result.loading;
      this.loaded = result.loaded;
    });
    this.load();
  }

  ngOnDestroy() {
    this._loader.complete();
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
    this.load();
  }

  load() {
    if(this._loader && this._topicId && ! this.inputRecords)
      this._dataService.loadList(this._loader, {parentId: this._topicId});
  }

  get topics(): Model.Topic[] {
    return this.inputRecords || this._loader.result.data;
  }

  get error(): string {
    return this._loader.result.formatError();
  }

  get notFound(): boolean {
    return this._loader.result.notFound;
  }
}
