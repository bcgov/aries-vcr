import { Component } from '@angular/core';
import { GeneralDataService } from '../general-data.service';

@Component({
  selector: 'app-contact',
  templateUrl: '../../themes/_active/info/contact.component.html',
  styleUrls: ['../../themes/_active/info/contact.component.scss']
})
export class ContactComponent {

  inited = true;

  constructor(
    private _dataService: GeneralDataService,
  ) {}

  get language() {
    return this._dataService.language;
  }

}
