import { Component, OnInit } from '@angular/core';
import { HttpService } from 'app/core/services/http.service';
import { ICredentialTypeResult } from 'app/core/interfaces/icredential-type-results.interface';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { ICredentialTypeOption } from './input.component';

@Component({
  selector: 'app-advanced-search',
  template: `
    <app-select></app-select>

    <app-checkbox></app-checkbox>
  `,
  styleUrls: ['./advanced-search.component.scss'],
})
export class AdvancedSearchComponent implements OnInit {
  $credentialTypeOptions: Observable<ICredentialTypeOption[]>;

  constructor(private httpSvc: HttpService) {}

  ngOnInit() {
    const $categories = this.httpSvc
      .httpGetRequest<ICredentialTypeResult>('v2/credentialtype')
      .pipe(map(results => results.results.map(credType => ({ id: credType.id, description: credType.description }))));
    $categories.subscribe(obs => console.log(obs));
    this.$credentialTypeOptions = $categories;
  }
}
