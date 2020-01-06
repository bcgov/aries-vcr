import { Component, OnInit } from '@angular/core';
import { HttpService } from 'app/core/services/http.service';
import { ICredentialTypeResult } from 'app/core/interfaces/icredential-type-results.interface';
import { map, debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { ICredentialTypeOption } from './input.component';
import { ISelectOption } from 'app/shared/components/select/select.component';
import { FormGroup, FormControl } from '@angular/forms';
import { GeneralDataService } from 'app/general-data.service';
import { ActivatedRoute } from '@angular/router';

export interface IAdvancedSearchOption {
  label: string;
  helper: string;
}

@Component({
  selector: 'app-advanced-search',
  template: `
    <section class="container" id="home">
      <app-breadcrumb></app-breadcrumb>
      <h2>{{ title }}</h2>
      <div class="header-row">
        <h3 class="header">Search by...</h3>
        <span></span>
        <h3 class="header">What this search type does</h3>
      </div>
      <form [formGroup]="fg">
        <app-advanced-search-row [label]="searchOptions[0].label" [helper]="searchOptions[0].helper">
          <input
            class="form-control"
            formControlName="text"
            [ngbTypeahead]="typeaheadSearch"
            (selectItem)="typeaheadSelected($event)"
          />
        </app-advanced-search-row>
        <app-advanced-search-row
          formControlName="type"
          [label]="searchOptions[1].label"
          [helper]="searchOptions[1].helper"
          *ngIf="$credentialTypeOptions | async as options"
        >
          <app-select [options]="options" [selected]="credTypeSelected"></app-select>
        </app-advanced-search-row>
        <app-advanced-search-row [label]="searchOptions[2].label" [helper]="searchOptions[2].helper">
          <app-select formControlName="archived" [options]="yesNoOptions" [selected]="yesNoSelected"></app-select>
        </app-advanced-search-row>
        <button type="submit" class="btn btn-primary">
          Advanced Search
        </button>
      </form>
    </section>
  `,
  styleUrls: ['./advanced-search.component.scss'],
})
export class AdvancedSearchComponent implements OnInit {
  title: string;

  $credentialTypeOptions: Observable<ISelectOption[]>;
  credTypeSelected: ISelectOption;
  searchOptions: IAdvancedSearchOption[];
  yesNoSelected: ISelectOption;
  yesNoOptions: ISelectOption[];
  fg: FormGroup;

  constructor(private httpSvc: HttpService, private dataSvc: GeneralDataService, private route: ActivatedRoute) {
    this.title = 'Advanced Search';

    this.yesNoOptions = [
      {
        value: '',
        description: 'Yes',
      },
    ];

    this.yesNoSelected = {
      value: false,
      description: 'No',
    };

    this.credTypeSelected = {
      value: null,
      description: 'Any credential type',
    };

    const fg = new FormGroup({
      type: new FormControl(),
      text: new FormControl(),
      archived: new FormControl('false'),
    });

    this.fg = fg;
  }

  ngOnInit() {
    const query = this.route.snapshot.queryParamMap.get('query');
    this.fg.controls.text.patchValue(query);
    this.fg.updateValueAndValidity();
    const $categories = this.httpSvc
      .httpGetRequest<ICredentialTypeResult>('credentialtype')
      .pipe(
        map(results => results.results.map(credType => ({ value: credType.id, description: credType.description }))),
      );
    this.$credentialTypeOptions = $categories;

    /* TODO: Parameterize these to include a method of defining the input option */
    const searchOptions = [
      { label: 'name', helper: 'Search by the name of the organization.' },
      { label: 'credential type', helper: 'Search by a specific type of credential.' },
      { label: 'historical credentials', helper: 'Include results that have expired or are no longer active.' },
    ];
    this.searchOptions = searchOptions;
  }

  get typeaheadSearch() {
    return (text$: Observable<string>) => {
      return text$.pipe(
        debounceTime(200),
        distinctUntilChanged(),
        switchMap(term => this.dataSvc.autocomplete(term, this.fg.value.archived)),
        map((result: any[]) => result.map(item => item['term'])),
      );
    };
  }

  typeaheadSelected(evt) {
    evt.preventDefault();
    const val = evt.item;
    this.fg.controls.text.patchValue(val);
    this.fg.updateValueAndValidity({ emitEvent: true });
  }
}
