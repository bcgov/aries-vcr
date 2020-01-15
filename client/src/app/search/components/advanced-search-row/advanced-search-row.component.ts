import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-advanced-search-row',
  templateUrl: './advanced-search-row.component.html',
  styleUrls: ['./advanced-search-row.component.scss'],
})
export class AdvancedSearchRowComponent implements OnInit {
  @Input() label: string;
  @Input() helper: string;
  constructor() {}

  ngOnInit() {}
}
