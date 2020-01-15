import { Slot } from './slot.model';

import { Renderer2 } from '@angular/core';

import { RowSpec, SlotSpec } from './i-timeline';

export class Row {
  slots: Slot[] = [];
  classNames: string[];
  height: number;
  start: Date;
  end: Date;
  _elt: HTMLElement;
  _renderer: Renderer2;
  _next: HTMLElement;
  _prev: HTMLElement;

  constructor(spec?: RowSpec) {
    if (spec) {
      this.classNames = spec.classNames;
      this.height = spec.height;
      this.setSlots(spec.slots);
    }
  }

  setSlots(specs: SlotSpec[]) {
    if (specs) {
      this.slots = specs.map(evt => new Slot(evt));
    } else {
      this.slots = [];
    }
  }

  setRange(start: Date, end: Date) {
    this.start = start;
    this.end = end;
  }

  get elt() {
    return this._elt;
  }

  render(renderer: Renderer2) {
    this._renderer = renderer;
    if (!this._elt) {
      this._elt = renderer.createElement('div');
      renderer.addClass(this._elt, 'timeline-row');
      if (this.classNames) {
        for (let c of this.classNames) {
          renderer.addClass(this._elt, c);
        }
      }
    }
    return this._elt;
  }

  update(width) {
    if (this.start && this.end && width) {
      let startTime = this.start.getTime();
      let endTime = this.end.getTime();
      let range = endTime - startTime;
      let havePrev = false;
      let haveNext = false;
      // determine visible slots and compute offsets
      for (let evt of this.slots) {
        let elt = evt.render(this._renderer);
        let startPos = -1;
        let endPos = width + 1;
        let updState = { hovered: false, started: false, ended: false };

        if (evt.start) {
          let evtStart = evt.start.getTime();
          if (evtStart < startTime) havePrev = true;
          if (evtStart > endTime) {
            haveNext = true;
            if (elt.parentNode) elt.parentNode.removeChild(elt);
            continue;
          }
          startPos =
            Math.round(
              ((Math.max(startTime, evtStart) - startTime) * width) / range
            ) - 1;
          if (startPos > 0) updState['started'] = true;
        }
        elt.style.left = '' + startPos + 'px';

        if (evt.end) {
          let evtEnd = evt.end.getTime();
          if (evtEnd > endTime) haveNext = true;
          if (evtEnd < startTime) {
            havePrev = true;
            if (elt.parentNode) elt.parentNode.removeChild(elt);
            continue;
          }
          endPos =
            Math.round(
              ((Math.min(endTime, evtEnd) - startTime) * width) / range
            ) + 1;
          if (endPos < width) updState['ended'] = true;
        }
        evt.updateState(updState);
        elt.style.width = '' + Math.max(endPos - startPos, 1) + 'px';
        this.elt.appendChild(elt);
      }
      if (havePrev) {
        if (!this._prev) {
          let link = this._renderer.createElement('div');
          this._renderer.addClass(link, 'fa');
          this._renderer.addClass(link, 'fa-caret-right');
          this._renderer.addClass(link, 'prev-link');
          link.tabIndex = 0;
          this._prev = link;
        }
        this.elt.appendChild(this._prev);
      } else if (this._prev && this._prev.parentNode) {
        this._prev.parentNode.removeChild(this._prev);
      }
      if (haveNext) {
        if (!this._next) {
          let link = this._renderer.createElement('div');
          this._renderer.addClass(link, 'fa');
          this._renderer.addClass(link, 'fa-caret-left');
          this._renderer.addClass(link, 'next-link');
          link.tabIndex = 0;
          this._next = link;
        }
        this.elt.appendChild(this._next);
      } else if (this._next && this._next.parentNode) {
        this._next.parentNode.removeChild(this._next);
      }
    }
  }
}
