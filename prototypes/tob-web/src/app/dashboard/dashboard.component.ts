import { Component, OnInit, AfterViewInit } from '@angular/core';
import { ActivatedRoute, Router} from '@angular/router';
import { GeneralDataService } from 'app/general-data.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: '../../themes/_active/dashboard/dashboard.component.html',
  styleUrls: ['../../themes/_active/dashboard/dashboard.component.scss']
})
export class DashboardComponent implements OnInit, AfterViewInit {

  public query : string = '';
  public allResults;
  public results = [];
  public searchType = 'name';
  public searchFocused = false;
  private searchTimer;
  private sub;
  private page = 0;
  public more = false;
  public less = false;
  public none = false;
  public inited = false;
  public loading = false;
  public recordCounts : {[key:string]:number} = {};
  private preload;

  constructor(
    private dataService: GeneralDataService,
    private $route: ActivatedRoute,
    private $router: Router
  ) { }

  ngOnInit() {
    this.preload = this.dataService.preloadData(['locations', 'locationtypes', 'verifiableorgtypes']);
    this.preload.then(() => {
      this.recordCounts = {
        orgs: this.dataService.getRecordCount('verifiableorgs'),
        certs: this.dataService.getRecordCount('verifiableclaims')
      };
      this.inited = true;
    });
    this.$route.queryParams.subscribe(params => {
      this.setQuery(params.query);
    });
  }

  ngAfterViewInit() {
    this.preload.then(() => {
      requestAnimationFrame(() => {
        (<HTMLInputElement>document.getElementById('searchInput')).value = this.query;
        this.focusSearch()
      });
    });
  }

  setQuery(q) {
    if(typeof q !== 'string') q = '';
    if(this.query !== q) {
      this.query = q;
      var search = (<HTMLInputElement>document.getElementById('searchInput'));
      if(search) search.value = this.query;
      this.preload.then(data => this.search());
    }
  }

  focusSearch(evt?) {
    (<HTMLInputElement>document.getElementById('searchInput')).select();
    if(evt) evt.preventDefault();
  }

  inputEvent(evt) {
    if(evt.type === 'focus') {
      this.searchFocused = true;
    } else if(evt.type === 'blur') {
      this.searchFocused = false;
    } else if(evt.type === 'input') {
      this.updateSearch(evt);
    }
  }

  updateSearch(evt) {
    let q = evt.target.value;
    let navParams = { queryParams: {}, relativeTo: this.$route };
    if(q !== undefined && q !== null) {
      q = q.trim();
      if(q !== '') {
        navParams.queryParams['query'] = q;
      }
    }
    if (this.searchTimer) clearTimeout(this.searchTimer);
    this.searchTimer = setTimeout(() => {
      this.$router.navigate(['./'], navParams);
    }, 150);
  }

  search(setType? : string) {
    let q = this.query.trim();
    this.loading = true;
    if(setType) {
      this.searchType = setType;
    }
    if(q.length) {
      let srch;
      if(this.searchType === 'name') {
        srch = this.sub = this.dataService.searchOrgs(q);
      } else {
        srch = this.sub = this.dataService.searchLocs(q);
      }
      this.sub.then(data => this.returnSearch(data, srch));
      this.sub.catch(err => this.searchError(err));
    } else {
      this.sub = null;
      this.returnSearch([], this.sub);
    }
  }

  setSearchType(evt) {
    if(this.searchType !== evt.target.value) {
      this.search(evt.target.value);
    }
    if(! this.query.trim().length) {
      requestAnimationFrame(() => this.focusSearch());
    }
  }

  returnSearch(data, from) {
    if(from !== this.sub) return;
    this.page = 0;
    this.allResults = data;
    this.paginate();
    this.loading = false;
  }

  searchError(err) {
    console.error(err);
    this.returnSearch([], this.sub);
  }

  paginate() {
    let rows = this.allResults || [];
    this.results = rows.slice(this.page * 10, (this.page + 1) * 10);
    this.more = (rows.length > (this.page + 1) * 10);
    this.less = (this.page > 0);
    this.none = (rows.length == 0);
  }

  prev() {
    this.page --;
    this.paginate();
  }

  next() {
    this.page ++;
    this.paginate();
  }

}
