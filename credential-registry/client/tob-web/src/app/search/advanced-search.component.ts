import { Component, OnInit } from '@angular/core';
import { HttpService } from 'app/core/services/http.service';
import { ICredentialTypeResult } from 'app/core/interfaces/icredential-type-results.interface';
import { map, debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { ISelectOption } from 'app/shared/components/select/select.component';
import { FormGroup, FormControl } from '@angular/forms';
import { GeneralDataService } from 'app/general-data.service';
import { ActivatedRoute, Router } from '@angular/router';

export interface IAdvancedSearchOption {
  label: string;
  helper: string;
}

@Component({
  selector: 'app-advanced-search',
  templateUrl: '../../themes/_active/search/advanced-search.component.html',
  styleUrls: ['../../themes/_active/search/advanced-search.component.scss'],
})
export class AdvancedSearchComponent implements OnInit {
  title: string;

  $credentialTypeOptions: Observable<ISelectOption[]>;
  credTypeSelected: ISelectOption;
  searchOptions: IAdvancedSearchOption[];
  yesNoSelected: ISelectOption;
  yesNoOptions: ISelectOption[];
  fg: FormGroup;

  constructor(
    private httpSvc: HttpService,
    private dataSvc: GeneralDataService,
    private router: Router,
    private route: ActivatedRoute,
  ) {
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

  submit(value: { text: string; type: string; archived: string }) {
    const { text: query, archived: inactive, type: credential_type_id } = value;

    this.router.navigate(['../search/name'], {
      relativeTo: this.route,
      queryParams: { query, inactive, credential_type_id },
    });
  }
}
