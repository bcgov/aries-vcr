import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Filter, Model } from 'app/data-types';

@Component({
  selector: 'app-search-result-list',
  templateUrl: '../../../../themes/_active/search/search-result-list.component.html',
  styleUrls: ['../../../../themes/_active/search/search-result-list.component.scss']
})
export class SearchResultListComponent {
  @Input() blankQuery: boolean;
  @Input() result: any;
  @Input() filters: Filter.FieldSet;

  @Output() nav: EventEmitter<string> = new EventEmitter<string>();

  constructor() { }

  onNav(nav: string): void {
    this.nav.emit(nav);
  }

}
