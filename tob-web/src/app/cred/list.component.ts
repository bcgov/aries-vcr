import { Component, Input } from '@angular/core';
import { CredResult } from '../data-types';

@Component({
  selector: 'cred-list',
  templateUrl: '../../themes/_active/cred/list.component.html',
  styleUrls: [
    '../../themes/_active/cred/cred.scss',
    '../../themes/_active/cred/list.component.scss']
})
export class CredListComponent {

  @Input() records: CredResult[];
  @Input() subjectId: string;

}
