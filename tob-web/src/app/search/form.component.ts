import { Component, AfterViewInit, Input, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GeneralDataService } from '../general-data.service';
import { Fetch, Model } from '../data-types';
import { CredListComponent } from '../cred/list.component';
import { SearchInputComponent } from './input.component';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'app-search',
  templateUrl: '../../themes/_active/search/form.component.html',
  styleUrls: ['../../themes/_active/search/form.component.scss']
})
export class SearchComponent implements OnInit, OnDestroy, AfterViewInit {

  @ViewChild('searchInput') _searchInput: SearchInputComponent;
  @ViewChild('credList') _nameList: CredListComponent;
  protected _curQuery: string;
  protected _filterType: string;
  protected _loader = new Fetch.ModelListLoader(Model.CredentialSearchResult);
  protected _searching = false;
  protected _querySub: Subscription;
  protected _typeSub: Subscription;
  protected _pageNum: number;

  constructor(
    private _dataService: GeneralDataService,
    private _route: ActivatedRoute,
    private _router: Router,
  ) {}

  ngOnInit() {
    this._loader.stream.subscribe(result => {
      this._searching = result.loading;
    });
    this._typeSub = this._route.params.subscribe(params => {
      this.filterType = params['filterType'];
    });
  }

  ngAfterViewInit() {
    this._querySub = this._route.queryParams.subscribe(params => {
      if(this._searchInput) {
        this._searchInput.value = params['query'];
        this._curQuery = this._searchInput.value;
        if(! this._curQuery.length)
          this._searchInput.focus();
      }
      setTimeout(this.updateQuery.bind(this), 50);
    });
  }

  ngOnDestroy() {
    this._querySub.unsubscribe();
    this._typeSub.unsubscribe();
    this._loader.complete();
  }

  get inited(): boolean {
    return true;
  }

  get error(): string {
    return this._loader.result && this._loader.result.error;
  }

  get filterType(): string {
    return this._filterType;
  }

  @Input() set filterType(filter: string) {
    this._filterType = filter;
    //this._searchInput.value = '';
    this.updateQuery();
  }

  get results(): Fetch.ListResult<Model.CredentialSearchResult> {
    return this._loader.result;
  }

  get creds(): Model.CredentialSearchResult[] {
    return this.results.data || [];
  }

  get resultInfo(): Fetch.Pagination {
    return this.results.pagination;
  }

  get searching(): boolean {
    return this._searching;
  }

  /*setFilterType(filter: string) {
    this._router.navigate(['../', filter]);
  }*/

  public handleNav(nav: string) {
    if (nav === 'previous') {
      this._pageNum --;
    } else if (nav == 'next') {
      this._pageNum ++;
    } else {
      console.warn(`Invalid nav '${nav}' received`);
    }
    this._performSearch();
  }

  public updateQuery() {
    if(! this._searchInput) return;
    this._pageNum = 1;
    let value = this._searchInput.value;
    if(this._curQuery !== value) {
      this._router.navigate([], { relativeTo: this._route, queryParams: {query: value }, queryParamsHandling: 'merge' });
      return;
    }
    this._performSearch();
  }

  _performSearch() {
    let value = this._searchInput.value;
    if(value !== null && value.length) {
      this._dataService.loadList(this._loader, {query: {page: this._pageNum, name: value}});
    } else {
      this._loader.reset();
    }
  }

}
