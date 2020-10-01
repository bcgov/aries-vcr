import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { GeneralDataService } from 'app/general-data.service';
import { Fetch, Filter, Model } from 'app/data-types';
import { ISelectOption } from 'app/shared/components/select/select.component';
import { Observable } from 'rxjs';
import { map, tap } from 'rxjs/operators';

export interface IAdvancedSearchOption {
  label: string;
  helper: string;
}

const FilterSpec = [
  {
    name: "name",
    hidden: true
  },
  {
    name: "issuer_id",
    label: "cred.issuer"
  },
  {
    name: "topic_credential_type_id",
    label: "cred.cred-type"
  },
  {
    name: "category:entity_type",
    label: "attribute.entity_type"
  }
];

@Component({
  selector: 'app-advanced-search',
  templateUrl: '../../themes/_active/search/advanced-search.component.html',
  styleUrls: ['../../themes/_active/search/advanced-search.component.scss'],
})
export class AdvancedSearchComponent implements OnInit, OnDestroy {
  private _filters = new Filter.FieldSet(FilterSpec);
  private _cLoader = new Fetch.ModelListLoader(Model.CredentialFacetSearchResult, { persist: true });
  private _ctLoader = new Fetch.ModelListLoader(Model.CredentialType, { persist: true });

  title: string = 'Advanced Search';
  credentials$: Observable<Fetch.ListResult<Model.CredentialFacetSearchResult>>;
  credentialTypeOptions$: Observable<ISelectOption[]>;
  credentialTypeSelected: ISelectOption;
  searchOptions: IAdvancedSearchOption[];
  yesNoSelected: ISelectOption;
  yesNoOptions: ISelectOption[];
  fg: FormGroup;

  constructor(
    private dataSvc: GeneralDataService,
    private route: ActivatedRoute,
    private fb: FormBuilder
  ) {
    this.yesNoOptions = [
      { value: 'true', description: 'Yes' }
    ];

    /* TODO: Parameterize these to include a method of defining the input option */
    this.searchOptions = [
      { label: 'name', helper: 'Search by the name of the organization.' },
      { label: 'credential type', helper: 'Search by a specific type of credential.' },
      { label: 'historical credentials', helper: 'Include results that have expired or are no longer active.' },
    ];

    this.yesNoSelected = { value: 'false', description: 'No' }
    this.credentialTypeSelected = { value: null, description: 'Any credential type' };

    this.credentialTypeOptions$ = this._ctLoader.ready
      .pipe(
        map(res => res.data.map(credType => ({ value: credType.id, description: credType.description }))),
      );

    this.credentials$ = this._cLoader.ready
      .pipe(
        tap(data => this.loadFacets(data))
      );

    // TODO: Add a validator for at least one required
    this.fg = this.fb.group({
      type: null,
      text: null,
      archived: 'false'
    }, []);
  }

  ngOnInit() {
    const query = this.route.snapshot.queryParamMap.get('query');

    this.fg.patchValue({
      text: query
    });

    this.dataSvc.loadList(this._ctLoader);
  }

  ngOnDestroy() {
    this._filters.complete();
    this._cLoader.complete();
    this._ctLoader.complete();
  }

  get filters() {
    return this._filters;
  }

  submit(value: { text: string; type: string; archived: string }) {
    const { text: name, archived: inactive, type: topic_credential_type_id } = value;
    this._filters.update({ name, inactive, topic_credential_type_id });
    this.dataSvc.loadList(this._cLoader, { query: this._filters.values });
  }

  private loadFacets(data: Fetch.ListResult<Model.CredentialFacetSearchResult>): void {
    let facets = this.dataSvc.loadFacetOptions(data);
    for (const field in facets) {
      if (Object.prototype.hasOwnProperty.call(facets, field)) {
        this._filters.setOptions(field, facets[field]);
      }
    }
  }
}
