import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { AddressComponent } from '../address/address.component';
import { CredListComponent } from './cred-list.component';
import { NameListComponent } from './name-list.component';
import { NamePanelComponent } from './name-panel.component';


@NgModule({
  declarations: [
    AddressComponent,
    CredListComponent,
    NameListComponent,
    NamePanelComponent,
  ],
  providers: [
  ],
  imports: [
    CommonModule,
    TranslateModule.forChild(),
    RouterModule.forChild([]),
  ],
  exports: [
    AddressComponent,
    CredListComponent,
    NameListComponent,
    NamePanelComponent,
  ]
})
export class CredModule {}

