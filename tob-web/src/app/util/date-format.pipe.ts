import { Inject, LOCALE_ID, Pipe, PipeTransform } from '@angular/core';
import { formatDate } from '@angular/common';
import { AppConfigService } from '../app-config.service';

@Pipe({
  name: 'dateFormat',
  pure: true
})
export class DateFormatPipe implements PipeTransform {
  constructor(
      @Inject(LOCALE_ID) private _locale: string,
      private _config: AppConfigService) {
  }

  transform(value: any, format = 'mediumDate', timezone?: string): any {
    if (value == null || value === '' || value !== value) return null;
    if(format === 'effectiveDate') format = 'mediumDate';
    else if(format === 'effectiveDateTime') format = 'MMM d, y, h:mm a';
    if (! timezone)
      timezone = this._config.getConfig().DISPLAY_TIMEZONE;
    return formatDate(value, format, this._locale, timezone);
  }
}
