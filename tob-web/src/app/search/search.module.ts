import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { LocalizeRouterModule } from 'localize-router';
import { CredSearchClient } from './cred-search.client';
import { IssuerClient } from './issuer.client';
import { TopicClient } from './topic.client';
import { CredentialClient } from './cred.client';
import { TopicCredClient } from './topic-cred.client';
import { IssuerCredentialTypeClient } from './credential-type.client';
import { NameSearchClient } from './name-search.client';
import { TopicSearchClient } from './topic-search.client';
import { SearchService } from './search.service';
import { SubjectSearchClient } from './subject-search.client';
import { SearchInputComponent } from './input.component';
import { SearchNavComponent } from './nav.component';

const ROUTES = [];

@NgModule({
  declarations: [
    SearchInputComponent,
    SearchNavComponent,
  ],
  providers: [
    CredSearchClient,
    IssuerClient,
    TopicClient,
    CredentialClient,
    TopicCredClient,
    IssuerCredentialTypeClient,
    NameSearchClient,
    TopicSearchClient,
    SearchService,
    SubjectSearchClient,
  ],
  imports: [
    CommonModule,
    TranslateModule.forChild(),
    RouterModule.forChild(ROUTES),
    LocalizeRouterModule.forChild(ROUTES),
  ],
  exports: [
    SearchInputComponent,
    SearchNavComponent,
  ]
})
export class SearchModule {}

