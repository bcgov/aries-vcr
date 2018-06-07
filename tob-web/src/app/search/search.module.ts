import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CredSearchClient } from './cred-search.client';
import { NameSearchClient } from './name-search.client';
import { SearchService } from './search.service';
import { SubjectSearchClient } from './subject-search.client';
import { SearchInputComponent } from './input.component';
import { SearchNavComponent } from './nav.component';


@NgModule({
  declarations: [
    SearchInputComponent,
    SearchNavComponent,
  ],
  providers: [
    CredSearchClient,
    NameSearchClient,
    SearchService,
    SubjectSearchClient,
  ],
  imports: [
    CommonModule,
  ],
  exports: [
    SearchInputComponent,
    SearchNavComponent,
  ]
})
export class SearchModule {}

