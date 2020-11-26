import { Component, AfterViewInit, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SearchInputComponent } from '../search/input.component';
import { GeneralDataService } from 'app/general-data.service';

@Component({
  selector: 'app-home',
  templateUrl: '../../themes/_active/home/home.component.html',
  styleUrls: ['../../themes/_active/home/home.component.scss'],
})
export class HomeComponent implements OnInit, AfterViewInit {
  @ViewChild('searchInput', { static: false }) _searchInput: SearchInputComponent;
  public inited = false;
  public loadError = null;
  public recordCounts: any = {};
  public filterType = 'name';
  inactive = false;
  credType: number;

  constructor(private _dataService: GeneralDataService, private _route: ActivatedRoute, private _router: Router) {}

  ngOnInit() {
    this._dataService
      .quickLoad()
      .catch(err => {
        this.loadError = err;
        this.inited = true;
      })
      .then(loaded => {
        if (loaded) {
          this.recordCounts.orgs = this._dataService.getRecordCount('topic');
          this.recordCounts.certs = this._dataService.getRecordCount('credential');
          this.recordCounts.active = this._dataService.getRecordCount('active');
          this.recordCounts.registrations = this._dataService.getRecordCount('registrations');
          this.recordCounts.last_week = this._dataService.getRecordCount('last_week');
        }
        this.inited = true;
        setTimeout(() => this.focus(), 50);
      });
  }

  ngAfterViewInit() {
    this.focus();
  }

  focus() {
    // autofocus currently disabled
    // if(this._searchInput) this._searchInput.focus();
  }

  performSearch(evt?) {
    const query = this._searchInput.value;
    console.log(query);
    const inactive = this.inactive ? '' : false;
    const credential_type_id = this.credType;
    this._router.navigate(['../search/name'], {
      relativeTo: this._route,
      queryParams: { query, inactive, credential_type_id },
    });
  }

  setInactive(evt: boolean) {
    console.log('inactive run', evt);
    this.inactive = evt;
  }

  setCredType(id: number) {
    this.credType = id;
  }
}
