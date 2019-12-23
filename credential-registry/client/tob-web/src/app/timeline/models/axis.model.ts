import { Renderer2 } from '@angular/core';
import { clearChildNodes, setElementContent } from './timeline-utils';

const YEAR_LEN = 31536000000;

export class Axis {
  start: Date;
  end: Date;
  _elt: HTMLElement;
  _renderer: Renderer2;
  _ticks: HTMLElement[] = [];

  render(renderer: Renderer2) {
    this._renderer = renderer;
    if (!this._elt) {
      this._elt = renderer.createElement('div');
      renderer.addClass(this._elt, 'timeline-axis');
    }
    return this._elt;
  }

  setRange(start: Date, end: Date) {
    this.start = start;
    this.end = end;
  }

  update(width) {
    clearChildNodes(this._elt);
    if (this.start && this.end && width) {
      let inc = 1;
      let startYear = this.start.getFullYear();
      let startTime = this.start.getTime();
      let endTime = this.end.getTime();
      let range = endTime - startTime;
      let yearStep = 1;
      let subtick = 0;
      let slotWidth = width / (range / YEAR_LEN);
      if (slotWidth > 200) subtick = 11;
      else if (slotWidth > 100) subtick = 3;
      else if (slotWidth > 50) subtick = 1;
      else if (slotWidth > 20) yearStep = subtick = 2;
      else if (slotWidth > 10) yearStep = subtick = 5;
      else if (slotWidth > 7) yearStep = subtick = 10;
      else {
        yearStep = 25;
        subtick = 5;
      }
      startYear -= startYear % yearStep;
      let tickidx = 0;
      let dt = new Date(startYear, 0, 1);
      let endYear = this.end.getFullYear() + yearStep * 2;
      for (let year = startYear; year <= endYear; year += yearStep) {
        let next = new Date(year + yearStep, 0, 1);
        let pos = ((dt.getTime() - startTime) * width) / range;
        if (pos > width) break;
        if (pos > 0) {
          let tick = this._ticks[tickidx++];
          if (!tick) {
            tick = this._renderer.createElement('div');
            this._renderer.addClass(tick, 'tick');
            this._ticks.push(tick);
          }
          this._renderer.removeClass(tick, 'small');
          tick.style.left = '' + Math.round(pos) + 'px';
          this._elt.appendChild(tick);
        }

        let nextpos = ((next.getTime() - startTime) * width) / range;
        for (let i = 0; i < subtick; i++) {
          let tpos = pos + ((nextpos - pos) * (i + 1)) / (subtick + 1);
          if (tpos < 0) continue;
          let tick = this._ticks[tickidx++];
          if (!tick) {
            tick = this._renderer.createElement('div');
            this._renderer.addClass(tick, 'tick');
            this._ticks.push(tick);
          }
          this._renderer.addClass(tick, 'small');
          tick.style.left = '' + Math.round(tpos) + 'px';
          this._elt.appendChild(tick);
        }

        let date = this._renderer.createElement('div');
        this._renderer.addClass(date, 'date');
        setElementContent(date, ['' + dt.getFullYear()]);
        date.style.left = '' + Math.round(pos) + 'px';
        this._elt.appendChild(date);

        dt = next;
      }
    }
  }
}
