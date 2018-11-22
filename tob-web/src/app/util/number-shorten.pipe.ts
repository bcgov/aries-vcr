import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'shortNumber',
  pure: true
})
export class NumberShortenPipe implements PipeTransform {
  constructor() {
  }

  transform(value: any, args?: any): any {
    let ret = '';
    let suffix = '';
    let div = 1;
    if(! value) ret = '0';
    else {
      if(value >= 100000000) {
        div = 1000000000;
        suffix = 'B';
      }
      else if(value >= 100000) {
        div = 1000000;
        suffix = 'M';
      }
      else if(value >= 1000) {
        div = 1000;
        suffix = 'K';
      }
      let base = value / div;
      let rnd = Math.pow(10, base > 10 ? 0 : 1);
      ret = ('' + (Math.round(base * rnd) / rnd)) + suffix;
    }
    return ret;
  }
}
