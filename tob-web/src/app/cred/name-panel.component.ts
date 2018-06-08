import { Component, Input } from '@angular/core';
import { CredResult, IssuerResult, NameResult } from '../data-types';

@Component({
  selector: 'name-panel',
  templateUrl: '../../themes/_active/cred/name-panel.component.html',
  styleUrls: [
    '../../themes/_active/cred/cred.scss',
    '../../themes/_active/cred/name-panel.component.scss']
})
export class NamePanelComponent {

  @Input() record: NameResult;

  get cred(): CredResult {
    return this.record ? this.record.credential : null;
  }

  get issuer(): IssuerResult {
    return this.record ? this.record.credential.credentialType.issuer: null;
  }

}
