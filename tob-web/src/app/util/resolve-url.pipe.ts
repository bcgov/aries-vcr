import { Pipe, PipeTransform } from '@angular/core';
import { GeneralDataService } from '../general-data.service';

@Pipe({
  name: 'resolveUrl'
})
export class ResolveUrlPipe implements PipeTransform {
  constructor(
    private _dataService: GeneralDataService,
  ) {}
  transform(value: any, args?: any): any {
    return this._dataService.getRequestUrl(value);
  }
}
