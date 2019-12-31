import { Component, OnInit } from '@angular/core';
import { HttpService } from 'app/core/services/http.service';
import { ICredentialTypeResult } from 'app/core/interfaces/icredential-type-results.interface';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { ICredentialTypeOption } from './input.component';

export interface IAdvancedSearchOption {
  label: string;
  helper: string;
}

@Component({
  selector: 'app-advanced-search',
  template: `
    <section class="container" id="home">
      <h2>{{ title }}</h2>
      <div class="header-row">
        <h3 class="header">Search by...</h3>
        <span></span>
        <h3 class="header">What this search type does</h3>
      </div>
      <app-advanced-search-row [label]="searchOptions[0].label" [helper]="searchOptions[0].helper">
        <input />
      </app-advanced-search-row>
      <app-advanced-search-row [label]="searchOptions[1].label" [helper]="searchOptions[1].helper">
        <app-select></app-select>
      </app-advanced-search-row>
      <app-advanced-search-row [label]="searchOptions[2].label" [helper]="searchOptions[2].helper">
        <app-select></app-select>
      </app-advanced-search-row>
    </section>
  `,
  styleUrls: ['./advanced-search.component.scss'],
})
export class AdvancedSearchComponent implements OnInit {
  title: string;

  $credentialTypeOptions: Observable<ICredentialTypeOption[]>;
  searchOptions: IAdvancedSearchOption[];

  constructor(private httpSvc: HttpService) {
    this.title = 'Advanced Search';
  }

  ngOnInit() {
    const $categories = this.httpSvc
      .httpGetRequest<ICredentialTypeResult>('v2/credentialtype')
      .pipe(map(results => results.results.map(credType => ({ id: credType.id, description: credType.description }))));
    $categories.subscribe(obs => console.log(obs));
    this.$credentialTypeOptions = $categories;

    /* TODO: Parameterize these to include a method of defining the input option */
    const searchOptions = [
      { label: 'name', helper: 'Search by the name of the organization.' },
      { label: 'credential type', helper: 'Search by a specific type of credential.' },
      { label: 'historical', helper: 'Include results that have expired or are no longer active.' },
    ];
    this.searchOptions = searchOptions;
  }
}
