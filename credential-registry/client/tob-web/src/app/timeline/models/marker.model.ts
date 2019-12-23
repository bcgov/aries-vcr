import { Renderer2 } from '@angular/core';
import { MarkerSpec } from './i-timeline';

export class Marker {
  date: Date;
  classNames: string[];
  label: string;
  start: Date;
  end: Date;
  link: string;
  _elt: HTMLElement;
  _labelElt: HTMLElement;
  _renderer: Renderer2;

  constructor(spec?: MarkerSpec) {
    if (spec) {
      this.classNames = spec.classNames;
      this.date = spec.date;
      this.label = spec.label;
      this.link = spec.link ? spec.link : null
    }
  }

  setRange(start: Date, end: Date) {
    this.start = start;
    this.end = end;
  }

  render(renderer: Renderer2, isLink: boolean = false) {
    this._renderer = renderer;

    if (! this._elt) {
      this._elt = renderer.createElement('div');
      if (this.classNames) {
        for (const c of this.classNames) {
          renderer.addClass(this._elt, c);
        }
      }
      if (isLink) {
        this._labelElt = renderer.createElement('a')
        this._labelElt.appendChild(document.createTextNode(this.label))
        this._labelElt.setAttribute('href', this.link)
        renderer.addClass(this._elt, 'timeline-marker');
        renderer.addClass(this._elt, 'short-date-marker');


        this._elt.appendChild(this._labelElt)
      } else {
        if (this.label) {
          this._labelElt = renderer.createElement('label');
          this._labelElt.appendChild(document.createTextNode(this.label));
          renderer.addClass(this._elt, 'timeline-marker');
          this._elt.appendChild(this._labelElt);

        }
      }
    }
    return this._elt;
  }

  update(width) {
    let hide = true;
    if (this.start && this.end && this.date && width) {
      const startTime = this.start.getTime();
      const endTime = this.end.getTime();
      const markTime = this.date.getTime();
      if (markTime >= startTime && markTime < endTime) {
        hide = false;
        const pos = Math.round((markTime - startTime) * width / (endTime - startTime)) - 1;
        this._elt.style.left = '' + pos + 'px';
      }
    }
    this._elt.style.display = hide ? 'none' : null;
  }
}
