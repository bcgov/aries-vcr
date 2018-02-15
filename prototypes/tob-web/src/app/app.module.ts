import { BrowserModule } from '@angular/platform-browser';
import { Location } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule, Http } from '@angular/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppRoutingModule, routes } from './app-routing.module';
import { TranslateModule, TranslateLoader, TranslateService } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { LocalizeParser, LocalizeRouterModule, LocalizeRouterSettings, ManualParserLoader } from 'localize-router';
import { MissingTranslationHandler, MissingTranslationHandlerParams } from '@ngx-translate/core';

import { AppComponent } from './app.component';
import { BusinessComponent } from './business/business.component';
import { CertComponent } from './cert/cert.component';
import { SearchBoxDirective } from './search-box/search-box.directive';
import { GeneralDataService } from 'app/general-data.service';
import { DashboardComponent } from './dashboard/dashboard.component';
import { IssuerComponent } from './issuer/issuer.component';
import { RoadmapComponent } from './roadmap/roadmap.component';
import { AdminModule } from 'app/admin/admin.module';
import { BreadcrumbComponent } from './breadcrumb/breadcrumb.component';

const ROUTE_PREFIX : string = 'ROUTES.';

export function createTranslateLoader(http: Http) {
  return new TranslateHttpLoader(http, './assets/i18n/', '.json');
}
export function createLocalizeLoader(translate: TranslateService, location: Location, settings: LocalizeRouterSettings) {
  // list of locales could be loaded from an external file, ie. locales.json
  return new ManualParserLoader(translate, location, settings, ['en', 'fr'], ROUTE_PREFIX);
}
export class MyMissingTranslationHandler implements MissingTranslationHandler {
  handle(params: MissingTranslationHandlerParams) {
    // used to highlight missing translation strings - otherwise they will be blank
    // FIXME - disable in production
    // params: {key, translateService}
    if(params.key.substring(0, ROUTE_PREFIX.length) === ROUTE_PREFIX)
      return;
    return '??' + params.key + '??';
  }
}


@NgModule({
  declarations: [
    AppComponent,
    BusinessComponent,
    CertComponent,
    SearchBoxDirective,
    DashboardComponent,
    IssuerComponent,
    RoadmapComponent,
    BreadcrumbComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AppRoutingModule,
    NgbModule,
    AdminModule,
    TranslateModule.forRoot({
      loader: {
        provide: TranslateLoader,
        useFactory: (createTranslateLoader),
        deps: [Http]
      }
    }),
    LocalizeRouterModule.forRoot(routes, {
      parser: {
        provide: LocalizeParser,
        useFactory: (createLocalizeLoader),
        deps: [TranslateService, Location, LocalizeRouterSettings]
      }
    })
  ],
  providers: [
    GeneralDataService,
    {provide: MissingTranslationHandler, useClass: MyMissingTranslationHandler}
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

