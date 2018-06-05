import { Component, OnInit, AfterViewInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { SubjectSearchClient } from './subject-search.client';
import { SearchResults } from './results.model';
import { Subject } from '../data-types';


@Component({
  selector: 'subject-search',
  templateUrl: '../../themes/_active/search/subject-search.component.html',
  styleUrls: ['../../themes/_active/search/subject-search.component.scss']
})
export class SubjectSearchComponent implements OnInit, AfterViewInit {

  public query : string = '';

  constructor(
    private _route : ActivatedRoute,
    private _client: SubjectSearchClient,
  ) {}

  get results() : SearchResults<Subject> {
    return this._client.results;
  }

  ngOnInit() {
    /*this.preload = this.dataService.preloadData(['locations', 'locationtypes', 'verifiableorgtypes']);
    this.preload.then(() => {
      this.recordCounts = {
        orgs: this.dataService.getRecordCount('verifiableorgs'),
        certs: this.dataService.getRecordCount('verifiableclaims')
      };
      this.inited = true;
    });*/
    this._route.queryParams.subscribe(params => {
      this.setQuery(params.query);
    });
  }

  ngAfterViewInit() {
    /*this.preload.then(() => {
      requestAnimationFrame(() => {
        (<HTMLInputElement>document.getElementById('searchInput')).value = this.query;
        this.focusSearch()
      });
    });*/
  }

  setQuery(q) {
    /*if(typeof q !== 'string') q = '';
    if(this.query !== q) {
      this.query = q;
      var search = (<HTMLInputElement>document.getElementById('searchInput'));
      if(search) search.value = this.query;
      this.preload.then(data => this.search());
    }*/
  }

  /*focusSearch(evt?) {
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
  }*/

  prev() {
    this._client.previousPage();
  }

  next() {
    this._client.nextPage();
  }

}
