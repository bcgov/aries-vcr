import { Component, Input } from '@angular/core';
import { CredResult, IssuerResult, NameResult, TopicResult, AddressResult, ContactResult, PersonResult } from '../data-types';

@Component({
  selector: 'name-panel',
  templateUrl: '../../themes/_active/cred/name-panel.component.html',
  styleUrls: [
    '../../themes/_active/cred/cred.scss',
    '../../themes/_active/cred/name-panel.component.scss']
})
export class NamePanelComponent {

  @Input() record: TopicResult;

  // get cred(): CredResult {
  //   return this.record ? this.record.credential : null;
  // }

  get people(): PersonResult[] {
    return this.record && this.record.people && this.record.people.length ? this.record.people : [];
  }

  get contacts(): ContactResult[] {
    return this.record && this.record.contacts && this.record.contacts.length ? this.record.contacts : [];
  }

  get addresses(): AddressResult[] {
    return this.record && this.record.addresses && this.record.addresses.length ? this.record.addresses : [];
  }

  get name(): NameResult {
    console.log(this.record && this.record.names && this.record.names.length ? this.record.names[0] : null)
    return this.record && this.record.names && this.record.names.length ? this.record.names[0] : null;
  }

  get issuer(): IssuerResult {
    return this.name ? this.name.issuer : null;
  }

}
