import {
  Component,
  OnInit,
  ChangeDetectionStrategy,
  Input
} from '@angular/core';

@Component({
  selector: 'app-topic-archive-list-item',
  templateUrl:
    '../../../themes/_active/cred/topic-archive-list-item.component.html',
  styleUrls: ['./topic-archive-list-item.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TopicArchiveListItemComponent implements OnInit {
  @Input() type: string;
  @Input() registerDate: string;
  @Input() endDate: string;
  // @Input() issuerName: string;
  @Input() details: string;

  constructor() {}

  ngOnInit() {}
}
