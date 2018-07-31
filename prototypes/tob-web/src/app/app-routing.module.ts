import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { NotFoundComponent } from './not-found/not-found.component';

import { CredFormComponent } from './cred/form.component';
import { CredModule } from './cred/cred.module';
import { HomeComponent } from './home/home.component';
import { IssuerFormComponent } from './issuer/form.component';
//import { RoadmapComponent } from './roadmap/roadmap.component';
import { SearchComponent } from './search/form.component';
import { SubjectFormComponent } from './subject/form.component';
import { SearchModule } from './search/search.module';

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
    path: 'topic/:topicId',
    data: {
      breadcrumb: 'topic.breadcrumb'
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
    path: 'issuer/:issuerId',
    component: IssuerFormComponent,
    data: {
      breadcrumb: 'issuer.breadcrumb',
    }
  },
  /*{
    path: 'recipe',
    redirectTo: 'recipe/start_a_restaurant'
  },
  {
    path: 'recipe/:recipeId',
    component: RoadmapComponent,
    data: {
      breadcrumb: 'recipe.breadcrumb'
    }
  },*/
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
    CredModule,
    SearchModule,
  ],
  exports: [
    RouterModule,
    CredModule,
    SearchModule,
  ]
})
export class AppRoutingModule { }
