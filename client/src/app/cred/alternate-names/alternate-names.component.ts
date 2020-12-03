import { Component, Input } from '@angular/core';

import { Model } from 'app/data-types';

@Component({
  selector: 'alternate-names',
  templateUrl: './alternate-names.component.html',
  styleUrls: ['./alternate-names.component.scss']
})
export class AlternateNamesComponent {
  @Input() isCollapsed = true;
  @Input() topic: Model.Topic;
}
