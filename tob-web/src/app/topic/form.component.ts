import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GeneralDataService } from '../general-data.service';
import { Fetch, Model } from '../data-types';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'topic-form',
  templateUrl: '../../themes/_active/topic/form.component.html',
  styleUrls: ['../../themes/_active/topic/form.component.scss']
})
export class TopicFormComponent implements OnInit, OnDestroy {
  source_type: string;
  source_id: string;
  loaded: boolean;
  loading: boolean;
  credsFormat: string = 'rows';
  _filterActive: boolean = true;
  showFilters: boolean = false;

  private _loader = new Fetch.ModelLoader(Model.TopicFormatted);

  private _creds = new Fetch.ModelListLoader(Model.CredentialSearchResult);

  private _idSub: Subscription;

  constructor(
    private _dataService: GeneralDataService,
    private _route: ActivatedRoute,
    private _router: Router) { }

  ngOnInit() {
    this._loader.ready.subscribe(result => {
      this._fetchCreds();
    });
    this._idSub = this._route.params.subscribe(params => {
      this.source_type = params['sourceType'];
      this.source_id = params['sourceId'];
      let ident = this.ident;
      this._dataService.loadRecord(this._loader, ident, {primary: true});
    });
  }

  ngOnDestroy() {
    this._idSub.unsubscribe();
    this._loader.complete();
    this._creds.complete();
  }

  get ident(): string {
    let source_type = this.source_type || this._dataService.defaultTopicType;
    if(source_type && this.source_id) {
      return this.source_type === '_' ? this.source_id : `ident/${source_type}/${this.source_id}`;
    }
  }

  get title(): string {
    let names = this.topic.names;
    if(names && names.length) {
      return names[0].text;
    }
  }

  get topic(): Model.TopicFormatted {
    return this._loader.result.data;
  }

  get names(): Model.Name[] {
    return this.loaded && this.topic.names;
  }

  get result$() {
    return this._loader.stream;
  }

  get creds$() {
    return this._creds.stream;
  }

  get filterActive(): string {
    return this._filterActive ? 'true' : 'false';
  }

  set filterActive(active: string) {
    this._filterActive = (active === 'true');
    this._fetchCreds();
  }

  protected _fetchCreds() {
    let credsFilter = {
      topic_id: ''+this.topic.id,
      revoked: this._filterActive ? 'false': '',
    };
    this._dataService.loadList(this._creds, {query: credsFilter});
  }

}
