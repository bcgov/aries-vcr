import { Component, AfterViewInit, Input, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GeneralDataService } from '../general-data.service';
import { Fetch, Filter, Model } from '../data-types';
import { CredListComponent } from '../cred/list.component';
import { SearchInputComponent } from './input.component';
import { Subscription } from 'rxjs/Subscription';

const FilterSpec = [
  {
    name: "name",
    alias: "query",
    hidden: true
  },
  {
    name: "page",
    defval: "1",
    hidden: true
  },
  {
    name: "inactive",
    label: "attribute.entity_status",
    options: [
      {
        label: "general.period-current",
        value: "false"
      },
      {
        label: "general.period-historical",
        value: "true"
      },
      {
        label: "general.status-any",
        value: ""
      }
    ],
    defval: "false",
    blank: true
  },
  {
    name: "revoked",
    label: "cred.status",
    options: [
      {
        label: "general.status-nonrevoked",
        value: "false"
      },
      {
        label: "general.status-revoked",
        value: "true"
      },
      {
        label: "general.status-any",
        value: ""
      }
    ],
    defval: "false",
    blank: true
  }
];

@Component({
  selector: 'app-search',
  templateUrl: '../../themes/_active/search/form.component.html',
  styleUrls: ['../../themes/_active/search/form.component.scss']
})
export class SearchComponent implements OnInit, OnDestroy, AfterViewInit {

  @ViewChild('searchInput') _searchInput: SearchInputComponent;
  @ViewChild('credList') _nameList: CredListComponent;
  protected _filters = new Filter.FieldSet(FilterSpec);
  protected _filterType: string;
  protected _loader = new Fetch.ModelListLoader(Model.CredentialSearchResult, {persist: true});
  protected _querySub: Subscription;
  protected _typeSub: Subscription;
  protected _inited = false;

  constructor(
    private _dataService: GeneralDataService,
    private _route: ActivatedRoute,
    private _router: Router,
  ) {}

  ngOnInit() {
    this._filters.stream.subscribe(fs => {
      if(this._inited) {
        let queryParams = this._filters.queryParams;
        this._router.navigate([], { relativeTo: this._route, queryParams, queryParamsHandling: 'merge' });
      }
    });
    this._querySub = this._route.queryParams.subscribe(params => {
      this._filters.loadQuery(params);
      setTimeout(this.initSearch.bind(this), 50);
    });
    this._typeSub = this._route.params.subscribe(params => {
      this.filterType = params['filterType'];
    });
  }

  ngAfterViewInit() {
    if(this._searchInput) {
      this._searchInput.value = this._filters.getFieldValue('name');
    }
  }

  ngOnDestroy() {
    this._querySub.unsubscribe();
    this._typeSub.unsubscribe();
    this._filters.complete();
    this._loader.complete();
  }

  get filterType(): string {
    return this._filterType;
  }

  @Input() set filterType(filter: string) {
    this._filterType = filter;
    //this._searchInput.value = '';
    this.updateQuery();
  }

  get filters() {
    return this._filters;
  }

  get result$() {
    return this._loader.stream;
  }

  get inited() {
    return this._inited;
  }

  /*setFilterType(filter: string) {
    this._router.navigate(['../', filter]);
  }*/

  get pageNum(): number {
    let val = this._filters.getFieldValue('page');
    return parseInt(val || '1', 10);
  }

  public handleNav(nav: string) {
    if (nav === 'previous') {
      this._filters.setFieldValue('page', Math.min(this.pageNum - 1, 1));
    } else if (nav == 'next') {
      this._filters.setFieldValue('page', this.pageNum + 1);
    } else {
      console.warn(`Invalid nav '${nav}' received`);
    }
  }

  public updateQuery() {
    if(this._searchInput) {
      this._filters.update({
        name: this._searchInput.value,
        page: '1'
      });
    }
  }

  public initSearch() {
    if(this._searchInput)
      this._searchInput.value = this._filters.getFieldValue('name');
    this._inited = true;
    this._performSearch();
  }

  get blankQuery() {
    return this._filters.getFieldValue('name') === '';
  }

  _performSearch() {
    let query = this._filters.values;
    if('name' in query && query['name'] !== '') {
      this._dataService.loadList(this._loader, {query});
    } else {
      this._loader.reset();
    }
  }

}
