import { Component, Input } from '@angular/core';
import { CredentialResult } from '../data-types';

@Component({
  selector: 'cred-list',
  templateUrl: '../../themes/_active/cred/list.component.html',
  styleUrls: [
    '../../themes/_active/cred/cred.scss',
    '../../themes/_active/cred/list.component.scss']
})
export class CredListComponent {

  @Input() records: CredentialResult[];
  @Input() topicId: string;

}
