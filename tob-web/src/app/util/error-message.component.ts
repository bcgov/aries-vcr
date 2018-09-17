import { Component, Input } from '@angular/core';

@Component({
  selector: 'error-message',
  templateUrl: '../../themes/_active/util/error-message.component.html'
})
export class ErrorMessageComponent {
  @Input() error: any;
  @Input() title: string;

  get formatted(): string {
    let err = this.error;
    let ret = null;
    if(err) {
      try {
        let body = JSON.parse(err._body);
        if(body && body.detail)
          ret = body.detail;
      } catch(e) {
        if(! (e instanceof SyntaxError))
          console.error(e);
      }
      if(! ret) {
        if(err.statusText)
          ret = `HTTP Error: ${err.statusText}`;
        else
          ret = 'Unknown error';
      }
    }
    return ret;
  }

  notFound(): boolean {
    return this.error && this.error.obj && this.error.obj.status === 404;
  }
}
