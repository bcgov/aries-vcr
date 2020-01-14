import { Renderer2 } from '@angular/core';
import { SlotSpec } from './i-timeline';
import { SlotState } from './slot-state.model';
import {
  parseDate,
  clearChildNodes,
  setElementContent
} from './timeline-utils';

export class Slot {
  _elt: HTMLElement;
  _renderer: Renderer2;
  _spec: SlotSpec;
  _state: SlotState = new SlotState();
  name: String;
  start: Date;
  end: Date;

  constructor(spec: SlotSpec) {
    this._spec = spec;
    this.start = parseDate(this._spec.start);
    this.end = parseDate(this._spec.end);
  }

  get elt() {
    return this._elt;
  }

  get spec() {
    return this._spec;
  }

  handleEvent(evt) {
    if (evt.target === this._elt) {
      let update = true;
      if (evt.type === 'focus') this._state.focused = true;
      else if (evt.type === 'blur') this._state.focused = false;
      else if (evt.type === 'mouseenter') this._state.hovered = true;
      else if (evt.type === 'mouseleave') this._state.hovered = false;
      else update = false;
      if (update) this.updateState();
    }
    if (evt.type === 'click') {
      evt.preventDefault();
      let raise = new CustomEvent('slotclick', { detail: this, bubbles: true });
      this._elt.dispatchEvent(raise);
    }
  }

  setState(state, val) {
    this._state[state] = val;
    this.updateState();
  }

  updateState(state?) {
    if (state) Object.assign(this._state, state);
    let classes = {
      active: this._state.active,
      focus: this._state.focused,
      hover: this._state.hovered,
      started: this._state.started,
      ended: this._state.ended
    };
    for (const k in classes) {
      if (classes[k]) this._renderer.addClass(this._elt, k);
      else this._renderer.removeClass(this._elt, k);
    }
  }

  render(renderer: Renderer2) {
    this._renderer = renderer;
    if (!this._elt) {
      this._elt = renderer.createElement(this._spec.url ? 'a' : 'div');
      renderer.addClass(this._elt, 'timeline-slot');
      this._elt.tabIndex = 0;
      if (this._spec.url) this._elt.setAttribute('href', this._spec.url);
      const handler = this.handleEvent.bind(this);
      this._elt.addEventListener('mouseenter', handler, false);
      this._elt.addEventListener('mouseleave', handler, false);
      this._elt.addEventListener('focus', handler, false);
      this._elt.addEventListener('blur', handler, false);
      this._elt.addEventListener('click', handler, false);
      if (this._spec.classNames) {
        for (let c of this._spec.classNames) {
          renderer.addClass(this._elt, c);
        }
      }
    }
    clearChildNodes(this._elt);
    let content = renderer.createElement('div');
    renderer.addClass(content, 'content');
    setElementContent(content, this._spec.htmlContent);
    this._elt.appendChild(content);
    return this._elt;
  }
}
