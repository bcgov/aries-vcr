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
  id: number;
  loaded: boolean;
  loading: boolean;
  credsFormat: string = 'rows';
  _filterActive: boolean = true;
  showFilters: boolean = false;

  private _focus = new Fetch.ModelLoader(Model.TopicFormatted);

  private _creds = new Fetch.ModelListLoader(Model.CredentialSearchResult);
  private _credsLoading: boolean;
  private _credsLoaded: boolean;

  private _idSub: Subscription;

  constructor(
    private _dataService: GeneralDataService,
    private _route: ActivatedRoute,
    private _router: Router) { }

  ngOnInit() {
    this._focus.stream.subscribe(result => {
      this.loaded = result.loaded;
      this.loading = result.loading;
      if(this.loaded) {
        this._fetchCreds();
      }
    });
    this._creds.stream.subscribe(result => {
      this._credsLoaded = result.loaded;
      this._credsLoading = result.loading;
    });
    this._idSub = this._route.params.subscribe(params => {
      this.id = +params['topicId'];
      this._dataService.loadRecord(this._focus, this.id);
    });
  }

  ngOnDestroy() {
    this._idSub.unsubscribe();
    this._focus.complete();
    this._creds.complete();
  }

  get title(): string {
    let names = this.names;
    if(names && names.length) {
      return names[0].text;
    }
  }

  get names(): Model.Name[] {
    return this.loaded && this.topic.names;
  }

  get result(): Fetch.BaseResult<Model.TopicFormatted> {
    return this._focus.result;
  }

  get topic(): Model.TopicFormatted {
    return this.result.data;
  }

  get error(): string {
    if(this.result.error && ! this.result.notFound) {
      return this.result.error.display;
    }
  }

  get notFound(): boolean {
    return this.result.notFound;
  }

  get creds(): Model.CredentialSearchResult[] {
    return this._creds.result.data;
  }

  get credsLoading() {
    return this._credsLoading;
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
      topic_id: ''+this.id,
      revoked: this._filterActive ? 'false': '',
    };
    this._dataService.loadList(this._creds, {query: credsFilter});
  }

}
