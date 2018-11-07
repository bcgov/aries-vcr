import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { GeneralDataService } from '../general-data.service';
import { Fetch, Model } from '../data-types';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'related-creds',
  templateUrl: '../../themes/_active/cred/related-list.component.html',
  styleUrls: ['../../themes/_active/cred/related-list.component.scss']
})
export class RelatedCredsComponent implements OnInit, OnDestroy {
  protected _topicId: number;
  protected _defaultFormat = 'timeline';
  protected _format = '';
  @Input() title: string;
  _filterActive: boolean = true;
  showFilters: boolean = false;

  private _loader: Fetch.ModelListLoader<Model.CredentialSearchResult>;

  constructor(
    private _dataService: GeneralDataService,
  ) { }

  ngOnInit() {
    this._loader = new Fetch.ModelListLoader(Model.CredentialSearchResult);
    this.load();
  }

  ngOnDestroy() {
    this._loader.complete();
  }

  get result$() {
    return this._loader.stream;
  }

  get filterActive(): string {
    return this._filterActive ? 'true' : 'false';
  }

  set filterActive(active: string) {
    this._filterActive = (active === 'true');
    this.load();
  }

  @Input() set defaultFormat(fmt: string) {
    this._defaultFormat = fmt;
  }

  get defaultFormat(): string {
    return this._defaultFormat;
  }

  get format(): string {
    // switch to list for many records
    return this._format || this._defaultFormat;
  }

  set format(val) {
    this._format = val;
    this.load();
  }

  get topicId(): number {
    return this._topicId;
  }

  @Input() set topicId(newId: number) {
    this._topicId = newId;
    this.load();
  }

  load() {
    if(this._loader && this.format === 'timeline') {
      this._loader.reset();
    }
    else if(this._loader && this._topicId) {
      let credsFilter = {
        topic_id: ''+this._topicId,
        inactive: this._filterActive ? 'false': '',
      };
      this._dataService.loadList(this._loader, {query: credsFilter});
    }
  }
}
