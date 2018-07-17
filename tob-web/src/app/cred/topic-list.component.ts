import { Component, Input } from '@angular/core';
import { TopicResult } from '../data-types';

@Component({
  selector: 'topic-list',
  templateUrl: '../../themes/_active/cred/topic-list.component.html',
  styleUrls: [
    '../../themes/_active/cred/cred.scss',
    '../../themes/_active/cred/name-list.component.scss']
})
export class TopicListComponent {

  @Input() public records: TopicResult[];

}
