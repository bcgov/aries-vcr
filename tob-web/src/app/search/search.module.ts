import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchService } from './search.service';
import { SubjectSearchClient } from './subject-search.client';
import { SearchInputComponent } from './input.component';
import { SubjectSearchComponent } from './subject-search.component';


@NgModule({
  declarations: [
    SearchInputComponent,
    SubjectSearchComponent,
  ],
  providers: [
    SearchService,
    SubjectSearchClient,
  ],
  imports: [
    CommonModule,
  ],
  exports: [
    SearchInputComponent,
    SubjectSearchComponent,
  ]
})
export class SearchModule {}

