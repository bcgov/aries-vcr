import { Component, Input } from '@angular/core';
import { Model } from '../data-types';

@Component({
  selector: 'timeline-cred',
  templateUrl: '../../themes/_active/cred/timeline-cred.component.html',
})
export class TimelineCredComponent {
  protected _cred: Model.Credential;

  constructor() { }

  get credential() {
    return this._cred;
  }

  @Input() set credential(cred: Model.Credential) {
    this._cred = cred;
  }

}
