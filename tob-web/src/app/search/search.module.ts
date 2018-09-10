import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { LocalizeRouterModule } from 'localize-router';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CredSearchClient } from './cred-search.client';
import { IssuerClient } from './issuer.client';
import { TopicClient } from './topic.client';
import { CredentialClient } from './cred.client';
import { TopicCredClient } from './topic-cred.client';
import { TopicRelatedClient } from './topic-related.client';
import { TopicRelatedFromClient } from './topic-related-from.client';
import { IssuerCredentialTypeClient } from './credential-type.client';
import { NameSearchClient } from './name-search.client';
import { TopicSearchClient } from './topic-search.client';
import { SearchService } from './search.service';

import { SearchComponent } from './form.component';
import { SearchInputComponent } from './input.component';
import { SearchNavComponent } from './nav.component';
import { TopicModule } from '../topic/topic.module';

const ROUTES = [];

@NgModule({
  declarations: [
    SearchComponent,
    SearchInputComponent,
    SearchNavComponent,
  ],
  providers: [
    CredSearchClient,
    IssuerClient,
    TopicClient,
    CredentialClient,
    TopicCredClient,
    TopicRelatedClient,
    TopicRelatedFromClient,
    IssuerCredentialTypeClient,
    NameSearchClient,
    TopicSearchClient,
    SearchService,
  ],
  imports: [
    CommonModule,
    TranslateModule.forChild(),
    RouterModule.forChild(ROUTES),
    LocalizeRouterModule.forChild(ROUTES),
    TopicModule,
    NgbModule,
  ],
  exports: [
    SearchComponent,
    SearchInputComponent,
    SearchNavComponent,
  ]
})
export class SearchModule {}

