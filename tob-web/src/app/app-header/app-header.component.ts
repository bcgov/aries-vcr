import { Component, Host } from '@angular/core';
import { AppComponent } from '../app.component';

@Component({
  selector: 'app-header',
  templateUrl: '../../themes/_active/app-header/app-header.component.html',
  styleUrls: ['../../themes/_active/app-header/app-header.component.scss']
})
export class AppHeaderComponent {

  constructor (
    @Host() public parent: AppComponent
  ) { }

}
