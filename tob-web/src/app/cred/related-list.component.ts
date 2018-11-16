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
  _credTypeId: string = '';
  _credTypeOptions: Model.CredentialType[] = [];
  _filterActive: boolean = true;
  _issuerOptions: Model.Issuer[] = [];
  _issuerId: string = '';
  _optionsLoaded: boolean = false;
  _showFilters: boolean = false;

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
    if(this._filterActive && ! this._optionsLoaded) {
      this._loadOptions();
    }
  }

  get showFilters(): boolean {
    return this._showFilters;
  }

  set showFilters(show: boolean) {
    this._showFilters = show;
    this.load();
    if(this._showFilters && ! this._optionsLoaded) {
      this._loadOptions();
    }
  }

  get credTypeOptions(): Model.CredentialType[] {
    return this._credTypeOptions;
  }

  get issuerOptions(): Model.Issuer[] {
    return this._issuerOptions;
  }

  @Input() set defaultFormat(fmt: string) {
    this._defaultFormat = fmt;
  }

  get defaultFormat(): string {
    return this._defaultFormat;
  }

  get credTypeId(): string {
    return this._credTypeId;
  }

  set credTypeId(val: string) {
    if(! val) val = '';
    if(this._credTypeId !== val) {
      this._credTypeId = val;
      this.load();
    }
  }

  get format(): string {
    // switch to list for many records
    return this._format || this._defaultFormat;
  }

  set format(val) {
    this._format = val;
    this.load();
  }

  get issuerId(): string {
    return this._issuerId;
  }

  set issuerId(val: string) {
    if(! val) val = '';
    if(this._issuerId !== val) {
      this._issuerId = val;
      this.load();
    }
  }

  get topicId(): number {
    return this._topicId;
  }

  @Input() set topicId(newId: number) {
    this._topicId = newId;
    this.load();
  }

  _loadOptions() {
    let credTypes = this._dataService.loadAll(Model.CredentialType);
    credTypes.then(data => {
      data.sort((a,b) => a.description.localeCompare(b.description));
      this._credTypeOptions = data;
    });
    let issuers = this._dataService.loadAll(Model.Issuer);
    issuers.then(data => {
      data.sort((a,b) => a.name.localeCompare(b.name));
      this._issuerOptions = data;
    });
    this._optionsLoaded = true;
  }

  load() {
    if(this._loader && this.format === 'timeline') {
      this._loader.reset();
    }
    else if(this._loader && this._topicId) {
      let credsFilter = {
        credential_type_id: this._credTypeId,
        issuer_id: this._issuerId,
        topic_id: ''+this._topicId,
        inactive: this._filterActive ? 'false': '',
      };
      this._dataService.loadList(this._loader, {query: credsFilter});
    }
  }
}
