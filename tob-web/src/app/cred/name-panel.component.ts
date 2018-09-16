import { Component, Input } from '@angular/core';
import { Model } from '../data-types';

@Component({
  selector: 'name-panel',
  templateUrl: '../../themes/_active/cred/name-panel.component.html',
  styleUrls: [
    '../../themes/_active/cred/cred.scss',
    '../../themes/_active/cred/name-panel.component.scss']
})
export class NamePanelComponent {

  @Input() record: Model.Topic;
  @Input() link: boolean = false;

  // get cred(): CredentialResult {
  //   return this.record ? this.record.credential : null;
  // }

  get people(): Model.Person[] {
    return this.record && this.record.people && this.record.people.length ? this.record.people : [];
  }

  get contacts(): Model.Contact[] {
    return this.record && this.record.contacts && this.record.contacts.length ? this.record.contacts : [];
  }

  get addresses(): Model.Address[] {
    return this.record && this.record.addresses && this.record.addresses.length ? this.record.addresses : [];
  }

  get name(): Model.Name {
    return this.record && this.record.names && this.record.names.length ? this.record.names[0] : null;
  }

  get categories(): Model.Category[] {
    return this.record && this.record.categories && this.record.categories.length ? this.record.categories : [];
  }

  get issuer(): Model.Issuer {
    return this.name ? this.name.issuer : null;
  }

}
