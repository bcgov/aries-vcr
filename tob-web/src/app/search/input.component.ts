import {
  Component, AfterViewInit, ElementRef, EventEmitter,
  Input, Output, Renderer2, ViewChild } from '@angular/core';


@Component({
  selector: 'search-input',
  templateUrl: '../../themes/_active/search/input.component.html',
  styleUrls: ['../../themes/_active/search/input.component.scss']
})
export class SearchInputComponent implements AfterViewInit {

  @ViewChild('queryInput') private _input : ElementRef;
  @Output() queryChange = new EventEmitter<string>();
  @Output() focusChange = new EventEmitter<boolean>();

  protected _delay: number = 150;
  protected _focused: boolean = false;
  protected _inputTimer;
  protected _loading: boolean = false;
  protected _query: string;

  constructor(
    private _renderer: Renderer2,
  ) {}

  get value() {
    return this._query;
  }

  set value(val: string) {
    this._query = val;
    if(this._input) this._input.nativeElement.value = val;
  }

  get focused() {
    return this._focused;
  }

  focus() {
    requestAnimationFrame(() => {
      if(this._input) this._input.nativeElement.select();
    });
  }

  get loading() {
    return this._loading;
  }

  @Input() set loading(val: boolean) {
    this._loading = val;
  }

  ngAfterViewInit() {
    /*this.preload.then(() => {
      requestAnimationFrame(() => {
        (<HTMLInputElement>document.getElementById('searchInput')).value = this.query;
        this.focusSearch()
      });
    });*/
    if(! this._input) {
      console.error('search input element not found');
      return;
    }
    let elt = this._input.nativeElement;
    this._renderer.listen(this._input.nativeElement, 'focus', (event) => {
      this._focused = true;
      this.focusChange.emit(this._focused);
    });
    this._renderer.listen(this._input.nativeElement, 'blur', (event) => {
      this._focused = false;
      this.focusChange.emit(this._focused);
    });
    this._renderer.listen(this._input.nativeElement, 'input', (event) => {
      this.updateQuery(event.target.value, true);
    });
    this._renderer.listen(this._input.nativeElement, 'change', (event) => {
      this.updateQuery(event.target.value);
    });
  }

  protected updateQuery(value: string, live?: boolean) {
    let old = this._query;
    if(value === undefined || value === null) {
      value = '';
    }
    this._query = value.trim();
    if(old !== value) {
      clearTimeout(this._inputTimer);
      if(live) {
        this._inputTimer = setTimeout(this.updated.bind(this), this._delay);
      } else {
        this.updated();
      }
    }
  }

  protected updated() {
    this.queryChange.emit(this._query);
  }
}
