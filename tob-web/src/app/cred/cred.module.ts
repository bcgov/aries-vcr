import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { LocalizeRouterModule } from 'localize-router';
import { CredFormComponent } from './form.component';
import { CredListComponent } from './list.component';
import { CredTypeListComponent } from './type-list.component';
import { IssuerFormComponent } from '../issuer/form.component';
import { NamePanelComponent } from './name-panel.component';
import { UtilModule } from '../util/util.module';


const ROUTES = [];

@NgModule({
  declarations: [
    CredFormComponent,
    CredListComponent,
    CredTypeListComponent,
    IssuerFormComponent,
    NamePanelComponent,
  ],
  providers: [
  ],
  imports: [
    CommonModule,
    TranslateModule.forChild(),
    RouterModule.forChild(ROUTES),
    LocalizeRouterModule.forChild(ROUTES),
    UtilModule,
  ],
  exports: [
    CredFormComponent,
    CredListComponent,
    CredTypeListComponent,
    IssuerFormComponent,
    NamePanelComponent,
  ]
})
export class CredModule {}

