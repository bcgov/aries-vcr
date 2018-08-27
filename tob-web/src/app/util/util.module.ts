import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { LocalizeRouterModule } from 'localize-router';
import { AddressComponent } from './address.component';
import { DateFormatPipe } from './date-format.pipe';
import { NotFoundComponent } from './not-found.component';

const ROUTES = [];

@NgModule({
  declarations: [
    AddressComponent,
    DateFormatPipe,
    NotFoundComponent,
  ],
  providers: [
  ],
  imports: [
    CommonModule,
    TranslateModule.forChild(),
    RouterModule.forChild(ROUTES),
    LocalizeRouterModule.forChild(ROUTES),
  ],
  exports: [
    AddressComponent,
    DateFormatPipe,
    NotFoundComponent,
  ]
})
export class UtilModule {}

