import { Component } from '@angular/core';

@Component({
  selector: 'app-pagescroll',
  templateUrl: '../../themes/_active/util/pagescroll.component.html',
  styleUrls: ['../../themes/_active/util/pagescroll.component.scss'],
  host: {
    '(window:scroll)': 'onScroll($event)',
  }
})
export class PageScrollComponent {
  visible: boolean = false;

  constructor() {
  }

  scrollTop(evt?) {
    if(evt) evt.preventDefault();
    window.scrollTo(0, 0);
  }

  onScroll() {
    this.visible = window.scrollY > 0;
  }
}
