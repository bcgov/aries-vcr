import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { LocalizeRouterModule } from 'localize-router';
import { AddressComponent } from '../address/address.component';
import { CredFormComponent } from './form.component';
import { CredListComponent } from './list.component';
import { NameListComponent } from './name-list.component';
import { NamePanelComponent } from './name-panel.component';

const ROUTES = [];

@NgModule({
  declarations: [
    AddressComponent,
    CredFormComponent,
    CredListComponent,
    NameListComponent,
    NamePanelComponent,
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
    CredFormComponent,
    CredListComponent,
    NameListComponent,
    NamePanelComponent,
  ]
})
export class CredModule {}

