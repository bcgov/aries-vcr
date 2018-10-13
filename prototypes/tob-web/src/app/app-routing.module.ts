import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { NotFoundComponent } from './util/not-found.component';

import { CredFormComponent } from './cred/form.component';
import { HomeComponent } from './home/home.component';
import { IssuerFormComponent } from './issuer/form.component';
import { SearchComponent } from './search/form.component';
import { TopicFormComponent } from './topic/form.component';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    component: HomeComponent
  },
  {
    path: 'search',
    redirectTo: '/search/name',
    pathMatch: 'full'
  },
  {
    path: 'search/:filterType',
    component: SearchComponent,
    data: {
      breadcrumb: 'search.breadcrumb'
    }
  },
  {
    path: 'topic/:sourceType/:sourceId',
    data: {
      breadcrumb: 'topic.breadcrumb'
    },
    children: [
      {
        path: '',
        component: TopicFormComponent,
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
    path: 'topic/:sourceId',
    data: {
      breadcrumb: 'topic.breadcrumb'
    },
    children: [
      {
        path: '',
        component: TopicFormComponent,
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
    path: 'issuer/:issuerId',
    component: IssuerFormComponent,
    data: {
      breadcrumb: 'issuer.breadcrumb',
    }
  },
  {
    path: '**',
    component: NotFoundComponent,
    data: {
      breadcrumb: 'not-found.breadcrumb'
    }
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes),
  ],
  exports: [
    RouterModule,
  ]
})
export class AppRoutingModule { }
