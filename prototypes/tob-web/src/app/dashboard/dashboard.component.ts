import { Component, OnInit } from '@angular/core';
import { GeneralDataService } from 'app/general-data.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  constructor(
    private dataService: GeneralDataService
  ) { }

  ngOnInit() {
    this.dataService.preloadData();
  }

  private query : string;
  private searchTimer;
  private results = [];

  updateSearch(evt) {
    this.query = evt.target.value;
    if (this.searchTimer) clearTimeout(this.searchTimer);
    this.searchTimer = setTimeout(() => this.search(), 150);
  }

  search() {
    this.results = this.dataService.searchOrgs(this.query);
    console.log(this.results);
  }

}
