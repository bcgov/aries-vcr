import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { LocalizeRouterModule } from 'localize-router';
import { AddressComponent } from './address.component';
import { DateFormatPipe } from './date-format.pipe';
import { ErrorMessageComponent } from './error-message.component';
import { LoadingIndicatorComponent } from './loading-indicator.component';
import { NotFoundComponent } from './not-found.component';
import { ResolveUrlPipe } from './resolve-url.pipe';

const ROUTES = [];

@NgModule({
  declarations: [
    AddressComponent,
    DateFormatPipe,
    ErrorMessageComponent,
    LoadingIndicatorComponent,
    NotFoundComponent,
    ResolveUrlPipe,
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
    ErrorMessageComponent,
    LoadingIndicatorComponent,
    NotFoundComponent,
    ResolveUrlPipe,
  ]
})
export class UtilModule {}

