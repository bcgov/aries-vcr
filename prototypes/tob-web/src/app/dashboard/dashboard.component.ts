import { Component, OnInit, AfterViewInit } from '@angular/core';
import { GeneralDataService } from 'app/general-data.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, AfterViewInit {

  constructor(
    private dataService: GeneralDataService
  ) { }

  ngOnInit() {
    this.dataService.preloadData();

  }

  ngAfterViewInit() {
    (<HTMLInputElement>document.getElementById('searchInput')).select();
  }

  public query : string;
  public allResults;
  public results = [];
  private searchTimer;
  private sub;
  private page = 0;
  private more = false;
  private less = false;
  private none = false;
  private loading = false;

  updateSearch(evt) {
    this.query = evt.target.value;
    if (this.searchTimer) clearTimeout(this.searchTimer);
    this.searchTimer = setTimeout(() => this.search(), 150);
  }

  search() {
    let srch = this.sub = this.dataService.searchOrgs(this.query);
    this.loading = true;
    this.sub.then(data => this.returnSearch(data, srch));
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
