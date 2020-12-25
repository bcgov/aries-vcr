import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormGroup, FormControl, ValidatorFn, ValidationErrors } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { GeneralDataService } from 'app/general-data.service';
import { Fetch, Filter, Model } from 'app/data-types';
import { ISelectOption } from 'app/shared/components/select/select.component';
import { BehaviorSubject, combineLatest, Observable } from 'rxjs';
import { distinctUntilChanged, map, tap } from 'rxjs/operators';

export interface IAdvancedSearchOption {
  label: string;
  helper: string;
}

const FilterSpec = [
  {
    name: "q",
    alias: "query",
    hidden: true
  },
  {
    name: "page",
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
  },
  {
    name: "inactive",
    label: "general.period-historical"
  },
  {
    name: "inactive",
    label: "attribute.entity_status",
    options: [
      {
        tlabel: "general.show-inactive",
        value: "any"
      }
    ],
    defval: "false",
    blank: true
  }
];

export const blankQueryValidator: ValidatorFn = (fg: FormGroup): ValidationErrors | null => {
  const text = fg.get('text');
  const type = fg.get('type');
  return !(text.value || type.value) ? { 'blankQuery': true } : null;
};

@Component({
  selector: 'app-advanced-search',
  templateUrl: '../../themes/_active/search/advanced-search.component.html',
  styleUrls: ['../../themes/_active/search/advanced-search.component.scss'],
})
export class AdvancedSearchComponent implements OnInit, OnDestroy {
  title: string = 'Advanced Search';

  private _refreshSubject = new BehaviorSubject<boolean>(false);
  private _filters = new Filter.FieldSet(FilterSpec);
  private _cLoader = new Fetch.ModelListLoader(Model.TopicFacetSearchResult, { persist: false });
  private _ctLoader = new Fetch.ModelListLoader(Model.CredentialType, { persist: false });
  private _queryParams$: Observable<any> = this.route.queryParams;
  private _refresh$: Observable<boolean> = this._refreshSubject.asObservable();
  private _searchTriggered: boolean = false;

  credentials$: Observable<Fetch.ListResult<Model.TopicFacetSearchResult>>;
  credentialTypeOptions$: Observable<ISelectOption[]>;

  yesNoOptions: ISelectOption[] = [
    { value: 'any', description: 'Yes' }
  ];

  /* TODO: Parameterize these to include a method of defining the input option */
  searchOptions: IAdvancedSearchOption[] = [
    { label: 'name', helper: 'Search by the name of the organization.' },
    { label: 'credential type', helper: 'Search by a specific type of credential.' },
    { label: 'historical credentials', helper: 'Include results that have expired or are no longer active.' },
  ];

  yesNoSelected: ISelectOption = { value: 'false', description: 'No' }
  credentialTypeSelected: ISelectOption = { value: '', description: 'any' };

  fg: FormGroup = new FormGroup({
    text: new FormControl(''),
    type: new FormControl(''),
    archived: new FormControl('false')
  }, { validators: blankQueryValidator });

  constructor(
    private dataService: GeneralDataService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.setupSubscriptions();
    this.loadCategories();
    this.patchForm();
    this.updateFilters();
  }

  ngOnDestroy(): void {
    this.teardownSubscriptions();
  }

  private get _currentPage(): string {
    return this._filters.getFieldValue('page') || '1';
  }

  private get _currentPageNum(): number {
    return parseInt(this._currentPage, 10);
  }

  get filters(): Filter.FieldSet {
    return this._filters;
  }

  get blankQuery(): boolean {
    return this.fg.hasError('blankQuery');
  }

  private loadCategories(): void {
    this.dataService.loadList(this._ctLoader);
  }

  private setupSubscriptions(): void {
    this.credentialTypeOptions$ = this._ctLoader.ready
      .pipe(
        map(res => res.data.map(type => ({
          value: type.id,
          description: type.description
        })))
      );

    this.credentials$ = this._cLoader.stream
      .pipe(
        tap(stream => stream.data && this.loadFacets(stream))
      );

    this._filters.stream
      .pipe(distinctUntilChanged())
      .subscribe(_ => {
        this.updateUrl();
      });

    combineLatest([
      this._refresh$,
      this._queryParams$
        .pipe(
          tap(() => this.patchForm())
        )
    ])
      .subscribe(([refresh]) => {
        if (!refresh) {
          return;
        }
        this.dataService.loadList(this._cLoader, { query: this._filters.values });
      });
  }

  private teardownSubscriptions(): void {
    this._refreshSubject.complete();
    this._filters.complete();
    this._cLoader.complete();
    this._ctLoader.complete();
  }

  private patchForm(): void {
    const queryParamMap: any = this.route.snapshot.queryParamMap;
    this.fg.patchValue({
      text: queryParamMap.get('q') || queryParamMap.get('query') || '',
      type: queryParamMap.get('topic_credential_type_id') || '',
      archived: queryParamMap.get('inactive') || 'false'
    });
  }

  private updateFilters(): void {
    const { text: q, archived: inactive, type: topic_credential_type_id } = this.fg.value;
    this._filters.update({ q, inactive, topic_credential_type_id, page: this._currentPage });
  }

  private updateUrl() {
    const queryParams = this._filters.queryParams;
    this.router.navigate([], { replaceUrl: true, relativeTo: this.route, queryParams, queryParamsHandling: 'merge' });
  }

  private previousPage(pageNum: number): void {
    this._filters.setFieldValue('page', Math.max(pageNum - 1, 1));
  }

  private nextPage(pageNum: number): void {
    this._filters.setFieldValue('page', pageNum + 1);
  }

  private loadFacets(data: Fetch.ListResult<Model.TopicFacetSearchResult>): void {
    let facets = this.dataService.loadFacetOptions(data);
    for (const field in facets) {
      if (Object.prototype.hasOwnProperty.call(facets, field)) {
        this._filters.setOptions(field, facets[field]);
      }
    }
  }

  onNav(nav: string): void {
    if (nav === 'previous') {
      this.previousPage(this._currentPageNum);
    } else if (nav == 'next') {
      this.nextPage(this._currentPageNum);
    } else {
      console.warn(`Invalid nav '${nav}' received`);
    }
  }

  submit(): void {
    if (this.blankQuery) {
      this.fg.markAsTouched();
      return;
    }
    if (!this._searchTriggered) {
      this._searchTriggered = true;
      this._refreshSubject.next(this._searchTriggered);
    }
    this.updateFilters();
  }
}
