import { BrowserModule } from '@angular/platform-browser';
import { Location } from '@angular/common';
import { NgModule } from '@angular/core';
import { Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppRoutingModule, routes } from './app-routing.module';
import {
  TranslateModule, TranslateLoader, TranslateService,
  MissingTranslationHandler, MissingTranslationHandlerParams
  } from '@ngx-translate/core';
import { LocalizeParser, LocalizeRouterModule, LocalizeRouterSettings, ALWAYS_SET_PREFIX } from 'localize-router';
import { ILocalizeRouterParserConfig } from 'localize-router-http-loader';
import { Observable } from 'rxjs';

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

export class WebpackTranslateLoader implements TranslateLoader {
  getTranslation(lang: string): Observable<any> {
    return Observable.fromPromise(System.import(`../themes/_active/assets/i18n/${lang}.json`));
  }
}
export class WebpackLocalizeRouterLoader extends LocalizeParser {
  load(routes: Routes): Promise<any> {
    return new Promise((resolve) => {
      System.import(`../themes/_active/assets/locales.json`)
        .then((data: ILocalizeRouterParserConfig) => {
            this.locales = data.locales;
            this.prefix = data.prefix || '';
            this.init(routes).then(resolve);
          }
        );
    });
  }
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
        useClass: WebpackTranslateLoader
      }
    }),
    LocalizeRouterModule.forRoot(routes, {
      parser: {
        provide: LocalizeParser,
        useClass: WebpackLocalizeRouterLoader,
        deps: [TranslateService, Location, LocalizeRouterSettings]
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
    {provide: ALWAYS_SET_PREFIX, useValue: true},
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

