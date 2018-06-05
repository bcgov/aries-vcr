import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LocalizeRouterModule } from 'localize-router';
import { TranslateModule } from '@ngx-translate/core';
import { Routes, RouterModule } from '@angular/router';
import { SearchModule } from '../search/search.module';

import { HomeComponent } from '../home/home.component';

export const ROUTES: Routes = [
  {
    path: 'v2',
    redirectTo: 'v2/home',
    pathMatch: 'full'
  },
  {
    path: 'v2/home',
    component: HomeComponent,
    data: {
      breadcrumb: 'dashboard.breadcrumb'
    }
  },
];

@NgModule({
  declarations: [
    HomeComponent,
  ],
  imports: [
    CommonModule,
    SearchModule,
    RouterModule.forChild(ROUTES),
    TranslateModule.forChild(),
    LocalizeRouterModule.forChild(ROUTES),
  ],
})
export class v2Module {}
