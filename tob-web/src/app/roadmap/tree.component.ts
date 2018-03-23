import { Component, Input } from '@angular/core';

@Component({
  selector: 'roadmap-tree',
  templateUrl: '../../themes/_active/roadmap/tree.component.html',
  styleUrls: ['../../themes/_active/roadmap/tree.component.scss']
})
export class RoadmapTreeComponent {
  @Input('data') data : any[];
  @Input('tree') tree : any[];
  @Input('horizontal') horizontal : boolean;

  constructor(
  ) { }
}
