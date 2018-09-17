import { BrowserModule } from '@angular/platform-browser';
import { Location } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppRoutingModule, routes } from './app-routing.module';
import { TranslateModule, TranslateLoader, TranslateService } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { LocalizeParser, LocalizeRouterModule, LocalizeRouterSettings } from 'localize-router';
import { LocalizeRouterHttpLoader } from 'localize-router-http-loader';
import { MissingTranslationHandler, MissingTranslationHandlerParams } from '@ngx-translate/core';

import { AppComponent } from './app.component';
import { AppHeaderComponent } from './app-header/app-header.component';
import { AppFooterComponent } from './app-footer/app-footer.component';
import { BreadcrumbComponent } from './breadcrumb/breadcrumb.component';
import { GeneralDataService } from 'app/general-data.service';
import { AdminModule } from './admin/admin.module';
import { SearchBoxDirective } from './search-box/search-box.directive';

import { HomeComponent } from './home/home.component';

import { CredModule } from './cred/cred.module';
import { SearchModule } from './search/search.module';
import { TopicModule } from './topic/topic.module';
import { UtilModule } from './util/util.module';


const ROUTE_PREFIX : string = 'ROUTES.';

export function createTranslateLoader(http: HttpClient) {
  return new TranslateHttpLoader(http, './assets/i18n/', '.json');
}
export function createLocalizeLoader(translate: TranslateService, location: Location, settings: LocalizeRouterSettings, http: HttpClient) {
  // list of locales could be loaded from an external file, ie. locales.json
  //return new ManualParserLoader(translate, location, settings, ['en', 'fr'], ROUTE_PREFIX);
  return new LocalizeRouterHttpLoader(translate, location, settings, http, './assets/locales.json');
}
export class MyMissingTranslationHandler implements MissingTranslationHandler {
  handle(params: MissingTranslationHandlerParams) {
    // used to highlight missing translation strings - otherwise they will be blank
    // FIXME - disable in production
    // params: {key, translateService}
    if(params.key.substring(0, ROUTE_PREFIX.length) === ROUTE_PREFIX) {
      return params.key.substring(ROUTE_PREFIX.length);
    }
    console.warn("missing translation: " + params.key);
    return '??' + params.key + '??';
  }
}


@NgModule({
  declarations: [
    AppComponent,
    AppHeaderComponent,
    AppFooterComponent,
    SearchBoxDirective,
    BreadcrumbComponent,
    HomeComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    AppRoutingModule,
    NgbModule.forRoot(),
    AdminModule,
    CredModule,
    SearchModule,
    TopicModule,
    TranslateModule.forRoot({
      loader: {
        provide: TranslateLoader,
        useFactory: createTranslateLoader,
        deps: [HttpClient]
      }
    }),
    LocalizeRouterModule.forRoot(routes, {
      parser: {
        provide: LocalizeParser,
        useFactory: createLocalizeLoader,
        deps: [TranslateService, Location, LocalizeRouterSettings, HttpClient]
      }
    }),
  ],
  exports: [
    CredModule,
    SearchModule,
    TopicModule,
    TranslateModule,
    UtilModule,
  ],
  providers: [
    GeneralDataService,
    {provide: MissingTranslationHandler, useClass: MyMissingTranslationHandler},
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

