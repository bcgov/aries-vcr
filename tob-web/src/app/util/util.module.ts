import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { LocalizeRouterModule } from 'localize-router';
import { AddressComponent } from './address.component';
import { AttributeComponent } from './attribute.component';
import { AttributeListComponent } from './attribute-list.component';
import { BreadcrumbComponent } from './breadcrumb.component';
import { DateFormatPipe } from './date-format.pipe';
import { ErrorMessageComponent } from './error-message.component';
import { LoadingIndicatorComponent } from './loading-indicator.component';
import { PageScrollComponent } from './pagescroll.component';
import { NotFoundComponent } from './not-found.component';
import { ResolveUrlPipe } from './resolve-url.pipe';

const ROUTES = [];

@NgModule({
  declarations: [
    AddressComponent,
    AttributeComponent,
    AttributeListComponent,
    BreadcrumbComponent,
    DateFormatPipe,
    ErrorMessageComponent,
    LoadingIndicatorComponent,
    PageScrollComponent,
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
    AttributeComponent,
    AttributeListComponent,
    BreadcrumbComponent,
    DateFormatPipe,
    ErrorMessageComponent,
    LoadingIndicatorComponent,
    PageScrollComponent,
    NotFoundComponent,
    ResolveUrlPipe,
  ]
})
export class UtilModule {}

