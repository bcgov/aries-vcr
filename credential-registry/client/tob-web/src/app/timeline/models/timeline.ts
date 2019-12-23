import { Renderer2 } from '@angular/core';
import { Axis } from './axis.model';
import { Layout, RowSpec, MarkerSpec } from './i-timeline';
import { Marker } from './marker.model';
import { Row } from './row.model';

export namespace Timeline {

  const YEAR_LEN = 31536000000;

  function clearChildNodes(elt: Node, fromIdx?: number) {
    if (! elt) return;
    for (let i = elt.childNodes.length - 1; i >= (fromIdx || 0); i--) {
      elt.removeChild(elt.childNodes[i]);
    }
  }

  function addElementContent(elt, content) {
    if (typeof content === 'string') {
      elt.appendChild(document.createTextNode(content));
    } else if (elt) {
      elt.appendChild(content);
    }
  }

  function setElementContent(elt, content) {
    if (typeof content === 'string') {
      elt.innerHTML = content;
    } else if (Array.isArray(content)) {
      elt.innerHTML = '';
      for (const part of content) {
        addElementContent(elt, part);
      }
    }
  }

  export function parseDate(date: string | Date) {
    let result: Date = null;
    if (typeof date === 'string') {
      result = new Date(date);
    } else {
      result = date;
    }
    if (result && isNaN(result.getTime())) {
      result = null;
    }
    return result;
  }

  function offsetDate(date: Date, offset: number) {
    const time = date.getTime() + (offset || 0);
    const d = new Date();
    d.setTime(time);
    return d;
  }

  export class TimelineView {
    _elts: {[key: string]: HTMLElement} = {
      container: null,
      controlsOuter: null,
      controlsInner: null,
      axisOuter: null,
      rowsOuter: null,
    };
    _axis: Axis;
    _layout: Layout = {};
    _lastLayout: Layout;
    _nextLayout: Layout;
    _gestureStartLayout: Layout;
    _markers: Marker[] = [];
    _rendered = false;
    _renderer: Renderer2;
    _resetRange: {start: Date, end: Date};
    _rows: Row[] = [];
    _redrawTimer: number;
    _updateTimer: number;
    _shortDateMarkers: Marker[];

    constructor(container: HTMLElement, layout: Layout, renderer: Renderer2) {
      this._elts.container = container;
      this._layout = layout || {};
      this._renderer = renderer;
    }

    get container() {
      return this._elts.container;
    }

    get rows() {
      return this._rows;
    }

    setRows(vals: RowSpec[]) {
      this._rows = (vals || []).map(val => new Row(val));
      this.redraw();
    }

    setMarkers(vals: MarkerSpec[]) {
      this._markers = (vals || []).map(val => new Marker(val));
      this.redraw();
    }

    setShortDateMarkers(vals: MarkerSpec[]) {
      this._shortDateMarkers = (vals || []).map(val => new Marker(val));
      this.redraw();
    }

    setRange(start: string | Date, end: string | Date, relative?: boolean) {
      let startDate = parseDate(start);
      let endDate = parseDate(end);
      if (startDate && endDate && endDate.getTime() < startDate.getTime()) {
        // swap if in wrong order
        const dt = startDate;
        startDate = endDate;
        endDate = dt;
      }
      const layout = Object.assign({}, this._layout);
      layout.start = startDate;
      layout.end = endDate;
      if (!relative) this._resetRange = {start: startDate, end: endDate}
      this.setLayout(layout);
    }

    moveRange(delta, layout?: Layout) {
      if (! layout) layout = this._layout;
      if (layout.start && layout.end) {
        let startTime = layout.start.getTime();
        const diff = layout.end.getTime() - startTime;
        startTime -= Math.round(diff * delta / 300);
        const start = new Date();
        start.setTime(startTime);
        const end = offsetDate(start, diff);
        this.setRange(start, end, true);
      }
    }

    scaleRange(delta, layout?: Layout) {
      if (! layout) layout = this._layout;
      if (layout.start && layout.end) {
        const startTime = layout.start.getTime();
        const diff = layout.end.getTime() - startTime;
        let offs = Math.round(diff * delta);
        if (diff + offs * 2 > YEAR_LEN * 200) {
          offs = (YEAR_LEN * 200 - diff) / 2;
        }
        const start = offsetDate(layout.start, -offs);
        const end = offsetDate(layout.end, +offs);
        this.setRange(start, end, true);
      }
    }

    resetRange() {
      if (this._resetRange) {
        const layout = Object.assign({}, this._layout);
        layout.start = this._resetRange.start;
        layout.end = this._resetRange.end;
        this.setLayout(layout);
      }
    }

    get layout() {
      return this._layout;
    }

    setLayout(newLayout: Layout) {
      if (! newLayout) return;
      if (this._layout && ! newLayout.noAnimate && this._rendered
          && newLayout.start && newLayout.end && this._layout.start && this._layout.end) {
        if (! newLayout.time) {
          newLayout.time = new Date().getTime() + 200;
        }
        this._lastLayout = this._layout;
        this._lastLayout.time = new Date().getTime();
        this._nextLayout = newLayout;
        this.update();
      } else {
        newLayout.time = new Date().getTime();
        this._lastLayout = this._layout;
        this._layout = newLayout;
        this._nextLayout = null;
        this.redraw();
      }
    }

    handleEvent(evt) {
      if (evt.type === 'mousewheel') {
        if (evt.ctrlKey) {
          if (evt.deltaY) {
            const delta = evt.deltaY * 0.01;
            this.scaleRange(delta);
            evt.preventDefault();
          }
        } else {
          if (Math.abs(evt.deltaX) > Math.abs(evt.deltaY)) {
            let delta = - evt.deltaX * 2;
            delta = Math.sign(delta) * Math.min(Math.abs(delta), 50);
            this.moveRange(delta);
            evt.preventDefault();
          }
        }
      } else if (evt.type === 'gesturestart') {
        evt.preventDefault();
        evt.stopPropagation();
        this._gestureStartLayout = Object.assign({}, this._layout);
      } else if (evt.type === 'gesturechange') {
        evt.preventDefault();
        evt.stopPropagation();
        if (evt.scale) {
          this.scaleRange(- evt.scale, this._gestureStartLayout);
        }
      } else if (evt.type === 'gestureend') {
        evt.preventDefault();
        this._gestureStartLayout = null;
      }
    }

    handleControl(evt) {
      let tgt = evt.target;
      while (tgt && ! tgt.name && tgt.parentNode && tgt.parentNode !== window) {
        tgt = tgt.parentNode;
      }
      const evtName = tgt && tgt.name;
      if (evtName == 'zoomin') {
        this.scaleRange(-0.1);
      } else if (evtName == 'zoomout') {
        this.scaleRange(0.1);
      } else if (evtName == 'prev') {
        this.moveRange(10);
      } else if (evtName == 'fastprev') {
        this.moveRange(100);
      } else if (evtName == 'next') {
        this.moveRange(-10);
      } else if (evtName == 'fastnext') {
        this.moveRange(-100);
      } else if (evtName == 'reset') {
        this.resetRange();
      }
    }

    render() {
      const rdr = this._renderer;
      const elts = this._elts;
      if (rdr && ! this._rendered) {
        if (! elts.container) {
          elts.container = rdr.createElement('div');
        }
        const handler = this.handleEvent.bind(this);
        rdr.listen(elts.container, 'mousewheel', handler);
        rdr.listen(elts.container, 'gesturestart', handler);
        rdr.listen(elts.container, 'gesturechange', handler);
        rdr.listen(elts.container, 'gestureend', handler);
        // disable forward/back gesture in Chrome
        rdr.listen(elts.container, 'pointermove', handler);
        rdr.addClass(elts.container, 'timeline-outer');
        elts.controlsOuter = rdr.createElement('div');
        rdr.addClass(elts.controlsOuter, 'controls-outer');
        rdr.addClass(elts.controlsOuter, 'row');
        elts.controlsInner = rdr.createElement('div');
        rdr.addClass(elts.controlsInner, 'controls-inner');
        rdr.addClass(elts.controlsInner, 'col');
        rdr.addClass(elts.controlsInner, 'text-center');
        elts.controlsOuter.appendChild(elts.controlsInner);
        this.renderControls();
        elts.rowsOuter = rdr.createElement('div');
        rdr.addClass(elts.rowsOuter, 'rows-outer');
        elts.axisOuter = rdr.createElement('div');
        rdr.addClass(elts.axisOuter, 'axis-outer');
        this._axis = new Axis();
        this._axis.setRange(this._layout.start, this._layout.end);
        elts.axisOuter.appendChild(this._axis.render(rdr));
        this._rendered = true;
        this.redraw();
      }
      return elts.container;
    }

    renderControls() {
      const groups = [
        ['fastprev', 'prev'],
        ['zoomout', 'zoomin'],
        ['reset'],
        ['next', 'fastnext'],
      ];
      const icons = {
        fastprev: 'fa-angle-double-left',
        prev: 'fa-angle-left',
        zoomin: 'fa-search-plus',
        zoomout: 'fa-search-minus',
        reset: 'fa-undo',
        next: 'fa-angle-right',
        fastnext: 'fa-angle-double-right',
      };
      const rdr = this._renderer;
      for (const btns of groups) {
        const grp = rdr.createElement('div');
        rdr.addClass(grp, 'btn-group');
        grp.setAttribute('role', 'group');
        for (const btn of btns) {
          const elt = rdr.createElement('button');
          elt.setAttribute('type', 'button');
          rdr.addClass(elt, 'btn');
          rdr.addClass(elt, 'btn-sm');
          rdr.addClass(elt, 'btn-secondary');
          elt.name = btn;
          elt.tabIndex = 0;
          const icon = rdr.createElement('span');
          rdr.addClass(icon, 'fa');
          rdr.addClass(icon, icons[btn]);
          elt.appendChild(icon);
          grp.appendChild(elt);
          rdr.listen(elt, 'click', this.handleControl.bind(this));
        }
        this._elts.controlsInner.appendChild(grp);
        this._elts.controlsInner.appendChild(document.createTextNode(' '));
      }
    }

    redraw() {
      if (! this._rendered) return;
      clearTimeout(this._updateTimer);
      this._updateTimer = null;
      if (this._redrawTimer) return;
      this._redrawTimer = requestAnimationFrame(this._performRedraw.bind(this));
    }

    _performRedraw() {
      const container = this._elts.container;
      const first = container.childNodes[0];
      const body = [this._elts.controlsOuter, this._elts.rowsOuter, this._elts.axisOuter];
      for (const elt of body) {
        container.insertBefore(elt, first);
      }
      clearChildNodes(container, body.length);
      const rowFirst = this._elts.rowsOuter.childNodes[0];
      let zIndex = 40;
      let clearPos = 0;
      for (const mark of this._markers) {
        const elt = !mark.link ? mark.render(this._renderer, false) : mark.render(this._renderer, true);
        this._elts.rowsOuter.insertBefore(elt, rowFirst);
        // elt.style.zIndex = '' + Math.max(0, zIndex);
        clearPos ++;
      }
      for (const row of this._rows) {
        const elt = row.render(this._renderer);
        this._elts.rowsOuter.insertBefore(elt, rowFirst);
        elt.style.zIndex = '' + Math.max(0, zIndex--);
        clearPos ++;
      }

      clearChildNodes(this._elts.rowsOuter, clearPos);
      this._performUpdate();
    }

    update() {
      if (this._updateTimer) return;
      this._updateTimer = requestAnimationFrame(this._performUpdate.bind(this));
    }

    _updateLayout() {
      if (this._nextLayout) {
        const now = new Date().getTime();
        if (this._nextLayout.time <= now) {
          this._nextLayout.time = now;
          this._layout = this._nextLayout;
          this._nextLayout = null;
        } else {
          // move closer to layout
          const startTime = this._lastLayout.time;
          const diff = this._nextLayout.time - startTime;
          const scale = (now - startTime) / diff;
          if (this._nextLayout.start != this._lastLayout.start) {
            this._layout.start = offsetDate(this._lastLayout.start, diff * scale);
          }
          if (this._nextLayout.end != this._lastLayout.end) {
            this._layout.end = offsetDate(this._lastLayout.end, diff * scale);
          }
          return false;
        }
      }
      return true;
    }

    _performUpdate() {
      clearTimeout(this._updateTimer);
      this._updateTimer = null;
      const reUp = ! this._updateLayout();
      if (this._elts.container) {
        const width = this._elts.container.clientWidth;

        // reposition slots
        const rowsWidth = this._elts.rowsOuter.clientWidth;
        for (const row of this._rows) {
          row.setRange(this._layout.start, this._layout.end);
          row.update(rowsWidth);
        }

        // redraw axis
        const axisWidth = this._elts.axisOuter.clientWidth;
        this._axis.setRange(this._layout.start, this._layout.end);
        this._axis.update(axisWidth);

        // reposition markers
        for (const mark of this._markers) {
          mark.setRange(this._layout.start, this._layout.end);
          mark.update(rowsWidth);
        }
      }
      if (reUp) {
        this.update();
      }
    }
  }
}
