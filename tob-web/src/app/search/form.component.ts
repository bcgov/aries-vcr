import { Component, AfterViewInit, Input, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GeneralDataService } from '../general-data.service';
import { Fetch, Filter, Model } from '../data-types';
import { CredListComponent } from '../cred/list.component';
import { SearchInputComponent } from './input.component';
import { Subscription } from 'rxjs/Subscription';
import { TranslateService } from '@ngx-translate/core';


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
    name: "issuer_id",
    label: "cred.issuer"
  },
  {
    name: "credential_type_id",
    label: "cred.cred-type"
  },
  {
    name: "category:entity_type",
    label: "attribute.entity_type"
  },
  {
    name: "inactive",
    label: "attribute.entity_status",
    options: [
      {
        tlabel: "general.show-inactive",
        value: ""
      }
    ],
    defval: "false",
    blank: true
  }
  /*
  {
    name: "revoked",
    label: "cred.status",
    options: [
      {
        tlabel: "general.show-revoked",
        value: ""
      }
    ],
    defval: "false",
    blank: true
  }
  */
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
  protected _loader = new Fetch.ModelListLoader(Model.CredentialFacetSearchResult, {persist: true});
  protected _querySub: Subscription;
  protected _typeSub: Subscription;
  protected _inited = false;

  constructor(
    private _dataService: GeneralDataService,
    private _route: ActivatedRoute,
    private _router: Router,
    private _translate: TranslateService,
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
    this._loader.ready.subscribe(this.handleFacets.bind(this));
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
    if(this._inited)
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

  public handleFacets(data) {
    let fields = data.info.facets.fields;
    let options = {
      credential_type_id: [],
      issuer_id: [],
      'category:entity_type': [],
    };
    if(fields) {
      for(let optname in fields) {
        for(let optitem of fields[optname]) {
          let optidx = optname;
          let optval: Filter.Option = {label: optitem.text, value: optitem.value, count: optitem.count};
          if(optname == 'category') {
            if(! optitem.count)
              // skip empty category values
              continue;
            let optparts = optitem.value.split('::', 2);
            if(optparts.length == 2) {
              optidx = optname + ':' + optparts[0];
              let lblkey = `category.${optparts[0]}.${optparts[1]}`;
              let label = this._translate.instant(lblkey);
              if(label === lblkey || label === `??${lblkey}??`)
                label = optparts[1];
              optval = {
                label,
                value: optparts[1],
                count: optitem.count,
              };
            }
          }
          if(optidx in options) {
            options[optidx].push(optval);
          }
        }
      }
    }
    for(let name in options) {
      options[name].sort((a,b) => a.label.localeCompare(b.label));
      this._filters.setOptions(name, options[name]);
    }
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
