import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { GeneralDataService } from 'app/general-data.service';
import { HttpService } from 'app/core/services/http.service';
import { ICredentialTypeResult } from 'app/core/interfaces/icredential-type-results.interface';
import { Fetch, Model } from 'app/data-types';
import { ISelectOption } from 'app/shared/components/select/select.component';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface IAdvancedSearchOption {
  label: string;
  helper: string;
}

@Component({
  selector: 'app-advanced-search',
  templateUrl: '../../themes/_active/search/advanced-search.component.html',
  styleUrls: ['../../themes/_active/search/advanced-search.component.scss'],
})
export class AdvancedSearchComponent implements OnInit, OnDestroy {
  private _loader = new Fetch.ModelListLoader(Model.CredentialFacetSearchResult, {persist: true});

  title: string = 'Advanced Search';
  credentialTypeOptions$: Observable<ISelectOption[]>;
  credentials$ = this._loader.stream;
  credTypeSelected: ISelectOption;
  searchOptions: IAdvancedSearchOption[];
  yesNoSelected: ISelectOption;
  yesNoOptions: ISelectOption[];
  fg: FormGroup;

  constructor(
    private dataSvc: GeneralDataService,
    private httpSvc: HttpService,
    private router: Router,
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
    this.credTypeSelected = { value: null, description: 'Any credential type' };

    // TODO: Add a validator for at least one required
    this.fg = this.fb.group({
      type: null,
      text: null,
      archived: 'false'
    });
  }

  ngOnInit() {
    const query = this.route.snapshot.queryParamMap.get('query');

    this.fg.patchValue({
      text: query
    });

    this.credentialTypeOptions$ = this.httpSvc
      .httpGetRequest<ICredentialTypeResult>('credentialtype')
      .pipe(
        map(res => res.results.map(credType => ({ value: credType.id, description: credType.description }))),
      );

    this.performSearch();
  }

  ngOnDestroy() {
    this._loader.complete();
  }

  // TODO: This should populate the list of results
  submit(value: { text: string; type: string; archived: string }) {
    const { text: query, archived: inactive, type: topic_credential_type_id } = value;

    // TODO: This should not redirect
    this.router.navigate(['../search/name'], {
      relativeTo: this.route,
      queryParams: { query, inactive, topic_credential_type_id },
    });
  }

  private performSearch() {
    // let query = this._filters.values;
    this.dataSvc.loadList(this._loader);
  }
}
