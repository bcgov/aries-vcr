import { Component, Input } from '@angular/core';
import { TopicResult } from '../data-types';

@Component({
  selector: 'topic-list',
  templateUrl: '../../themes/_active/topic/list.component.html',
  styleUrls: [
    '../../themes/_active/cred/cred.scss',
    '../../themes/_active/topic/list.component.scss']
})
export class TopicListComponent {

  @Input() public records: TopicResult[];

  typeLabel(val: string): string {
    if(val) return ('name.'+val).replace(/_/g, '-');
    return '';
  }

}
