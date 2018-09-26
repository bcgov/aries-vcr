import { Component, Input } from '@angular/core';
import { Model } from '../data-types';
import { TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'attribute-view',
  templateUrl: '../../themes/_active/util/attribute.component.html',
  styleUrls: ['../../themes/_active/cred/cred.scss']
})
export class AttributeComponent {

  @Input() record: Model.Attribute;

  constructor(
    private _translate: TranslateService,
  ) {}

  get formatted(): string {
    return this.record.value;
  }

  get categoryValue() {
    let lbl = `category.${this.record.type}.${this.record.value}`;
    return this._translate.stream(lbl).map(
      lbl => (! lbl || lbl.substring(0, 2) == '??') ? this.record.value : lbl
    );
  }
}
