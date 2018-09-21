import { Component, Input } from '@angular/core';
import { Model } from '../data-types';

@Component({
  selector: 'attribute-view',
  template: `<div *ngIf="record" [class]="'claim-info '+typeClass" [innerHTML]="formatted"></div>`,
  styleUrls: ['../../themes/_active/cred/cred.scss']
})
export class AttributeComponent {

  @Input() record: Model.Attribute;

  get formatted(): string {
    return this.record.value;
  }

  get typeClass(): string {
    return this.record.typeClass;
  }
}
