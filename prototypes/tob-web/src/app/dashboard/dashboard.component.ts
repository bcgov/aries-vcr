import { Component, OnInit, AfterViewInit } from '@angular/core';
import { ActivatedRoute, Router} from '@angular/router';
import { GeneralDataService } from 'app/general-data.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, AfterViewInit {

  public query : string = '';
  public allResults;
  public results = [];
  public searchType = 'name';
  private searchTimer;
  private sub;
  private page = 0;
  public more = false;
  public less = false;
  public none = false;
  public loading = false;
  private preload;

  constructor(
    private dataService: GeneralDataService,
    private $route: ActivatedRoute,
    private $router: Router
  ) { }

  ngOnInit() {
    this.preload = this.dataService.preloadData(['locations', 'locationtypes', 'verifiableorgtypes']);
    this.$route.queryParams.subscribe(params => {
      this.setQuery(params.query);
    });
  }

  ngAfterViewInit() {
    (<HTMLInputElement>document.getElementById('searchInput')).value = this.query;
    this.focusSearch();
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

  focusSearch() {
    (<HTMLInputElement>document.getElementById('searchInput')).select();
  }

  inputEvent(evt) {
    if(evt.type === 'focus') {
      evt.target.parentNode.classList.add('active');
    } else if(evt.type === 'blur') {
      evt.target.parentNode.classList.remove('active');
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
      this.focusSearch();
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

  orgCount() {
    return this.dataService.getRecordCount('verifiableorgs');
  }

  claimCount() {
    return this.dataService.getRecordCount('verifiableclaims');
  }

}
