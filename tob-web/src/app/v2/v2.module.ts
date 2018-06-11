import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LocalizeRouterModule } from 'localize-router';
import { Routes, RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { SearchModule } from '../search/search.module';

import { HomeComponent } from '../home/home.component';
import { CredModule } from '../cred/cred.module';
import { CredFormComponent } from '../cred/form.component';
import { IssuerFormComponent } from '../issuer/form.component';
import { SubjectFormComponent } from '../subject/form.component';

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
  {
    path: 'v2/subject/:subjId',
    data: {
      breadcrumb: 'subject.breadcrumb'
    },
    children: [
      {
        path: '',
        component: SubjectFormComponent,
      },
      {
        path: 'cred/:credId',
        component: CredFormComponent,
        data: {
          breadcrumb: 'cred.breadcrumb'
        }
      }
    ]
  },
  {
    path: 'v2/issuer/:issuerId',
    component: IssuerFormComponent,
    data: {
      breadcrumb: 'issuer.breadcrumb',
    }
  }
];

@NgModule({
  declarations: [
    HomeComponent,
    IssuerFormComponent,
    SubjectFormComponent,
  ],
  imports: [
    CommonModule,
    CredModule,
    SearchModule,
    RouterModule.forChild(ROUTES),
    TranslateModule.forChild(),
    LocalizeRouterModule.forChild(ROUTES),
  ],
})
export class v2Module {}
