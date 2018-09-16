import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { LocalizeRouterModule } from 'localize-router';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { SearchComponent } from './form.component';
import { SearchInputComponent } from './input.component';
import { SearchNavComponent } from './nav.component';
import { CredModule } from '../cred/cred.module';
import { UtilModule } from '../util/util.module';

const ROUTES = [];

@NgModule({
  declarations: [
    SearchComponent,
    SearchInputComponent,
    SearchNavComponent,
  ],
  providers: [
  ],
  imports: [
    CommonModule,
    TranslateModule.forChild(),
    RouterModule.forChild(ROUTES),
    LocalizeRouterModule.forChild(ROUTES),
    CredModule,
    UtilModule,
    NgbModule,
  ],
  exports: [
    SearchComponent,
    SearchInputComponent,
    SearchNavComponent,
  ]
})
export class SearchModule {}

