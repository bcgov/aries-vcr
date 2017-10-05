import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BusinessComponent } from 'app/business/business.component';
import { CertComponent } from 'app/cert/cert.component';
import { DashboardComponent } from 'app/dashboard/dashboard.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: 'home',
    component: DashboardComponent,
    data: {
      breadcrumb: 'Search'
    }
  },
  {
    path: 'business/:recordId',
    component: BusinessComponent,
    data: {
      breadcrumb: 'Organization Info'
    }
  },
  {
    path: 'cert',
    component: CertComponent,
    data: {
      breadcrumb: 'Permit and License Info'
    }
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
