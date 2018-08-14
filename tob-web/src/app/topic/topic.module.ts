import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { LocalizeRouterModule } from 'localize-router';
import { CredModule } from '../cred/cred.module';
import { UtilModule } from '../util/util.module';
import { TopicFormComponent } from '../topic/form.component';
import { TopicListComponent } from '../topic/list.component';

const ROUTES = [];

@NgModule({
  declarations: [
    TopicFormComponent,
    TopicListComponent,
  ],
  providers: [
  ],
  imports: [
    CommonModule,
    FormsModule,
    TranslateModule.forChild(),
    RouterModule.forChild(ROUTES),
    LocalizeRouterModule.forChild(ROUTES),
    CredModule,
    UtilModule,
  ],
  exports: [
    TopicFormComponent,
    TopicListComponent,
  ]
})
export class TopicModule {}

