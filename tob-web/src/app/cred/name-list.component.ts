import { Component, Input } from '@angular/core';
import { NameResult } from '../data-types';

@Component({
  selector: 'name-list',
  templateUrl: '../../themes/_active/cred/name-list.component.html',
  styleUrls: [
    '../../themes/_active/cred/cred.scss',
    '../../themes/_active/cred/name-list.component.scss']
})
export class NameListComponent {

  @Input() records: NameResult[];

}
