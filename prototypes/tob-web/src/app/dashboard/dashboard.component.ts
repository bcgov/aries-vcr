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

  constructor(
    private dataService: GeneralDataService,
    private $route: ActivatedRoute,
    private $router: Router
  ) { }

  ngOnInit() {
    this.dataService.preloadData();
    this.$route.queryParams.subscribe(params => {
      let q = params.query;
      if(typeof q !== 'string') q = '';
      if(this.query !== q) {
        this.query = q;
        this.search();
      }
    })
  }

  ngAfterViewInit() {
    this.focusSearch();
  }

  focusSearch() {
    (<HTMLInputElement>document.getElementById('searchInput')).select();
  }

  setFocus(evt) {
    if(evt.type === 'focus') {
      evt.target.parentNode.classList.add('active');
    } else {
      evt.target.parentNode.classList.remove('active');
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
        srch = this.sub = this.dataService.searchOrgs(this.query);
      } else {
        srch = this.sub = this.dataService.searchLocs(this.query);
      }
      this.sub.then(data => this.returnSearch(data, srch));
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
