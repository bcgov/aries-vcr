import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { LocalizeRouterModule } from 'localize-router';
import { NgbTypeaheadModule } from '@ng-bootstrap/ng-bootstrap';

import { SearchComponent } from './form.component';
import { SearchFiltersComponent } from './filters.component';
import { SearchInputComponent } from './input.component';
import { SearchNavComponent } from './nav.component';
import { CredModule } from '../cred/cred.module';
import { UtilModule } from '../util/util.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from 'app/shared/shared.module';
import { AdvancedSearchComponent } from './advanced-search.component';
import { AdvancedSearchRowComponent } from './components/advanced-search-row/advanced-search-row.component';

const ROUTES = [];

@NgModule({
  declarations: [
    SearchComponent,
    SearchFiltersComponent,
    SearchInputComponent,
    SearchNavComponent,
    AdvancedSearchComponent,
    AdvancedSearchRowComponent,
  ],
  providers: [],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    TranslateModule.forChild(),
    RouterModule.forChild(ROUTES),
    LocalizeRouterModule.forChild(ROUTES),
    CredModule,
    UtilModule,
    NgbTypeaheadModule,
    SharedModule,
  ],
  exports: [SearchComponent, SearchFiltersComponent, SearchInputComponent, SearchNavComponent],
})
export class SearchModule {}
