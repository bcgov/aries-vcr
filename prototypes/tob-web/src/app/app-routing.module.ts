import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BusinessComponent } from 'app/business/business.component';
import { CertComponent } from 'app/cert/cert.component';
import { IssuerComponent } from 'app/issuer/issuer.component';
import { DashboardComponent } from 'app/dashboard/dashboard.component';
import { RoadmapComponent } from 'app/roadmap/roadmap.component';
import { NotFoundComponent } from 'app/not-found/not-found.component';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    component: DashboardComponent,
    data: {
      breadcrumb: 'dashboard.breadcrumb'
    }
  },
  {
    path: 'org/:orgId',
    data: {
      breadcrumb: 'org.breadcrumb'
    },
    children: [
      {
        path: '',
        component: BusinessComponent
      },
      {
        path: 'cert/:certId',
        data: {
          breadcrumb: 'cert.breadcrumb'
        },
        children: [
          {
            path: '',
            component: CertComponent,
          },
          {
            path: 'issuer',
            component: IssuerComponent,
            data: {
              breadcrumb: 'issuer.breadcrumb'
            }
          }
        ]
      }
    ]
  },
  {
    path: 'issuer/:issuerId',
    component: IssuerComponent,
    data: {
      breadcrumb: 'issuer.breadcrumb'
    }
  },
  {
    path: 'recipe',
    redirectTo: 'recipe/start_a_restaurant'
  },
  {
    path: 'recipe/:recipeId',
    component: RoadmapComponent,
    data: {
      breadcrumb: 'recipe.breadcrumb'
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
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
