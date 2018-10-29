import { Pipe, PipeTransform } from '@angular/core';
import { DatePipe } from '@angular/common';

@Pipe({
  name: 'dateFormat'
})
export class DateFormatPipe extends DatePipe implements PipeTransform {
  transform(value: any, args?: any): any {
    let format = arguments[1] || 'mediumDate';
    let timezone = arguments[2] || 'UTC';
    if(format === 'effectiveDate') format = 'mediumDate';
    else if(format === 'effectiveDateTime') format = 'MMM d, y, h:mm a';
    // may want to automatically strip off time if equal to midnight
    return super.transform(value, format, timezone);
  }
}
