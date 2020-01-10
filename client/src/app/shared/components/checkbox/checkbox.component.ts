import { Component, OnInit, Output, Input } from '@angular/core';
import { EventEmitter } from 'protractor';
import { ControlValueAccessor } from '@angular/forms';

@Component({
  selector: 'app-checkbox',
  templateUrl: './checkbox.component.html',
  styleUrls: ['./checkbox.component.scss'],
})
export class CheckboxComponent implements OnInit, ControlValueAccessor {
  @Input() label: string;
  @Input() checked = false;

  value: any;
  onModelChange: any;
  onTouch: any;
  disabled: boolean;

  writeValue(obj: any): void {
    this.value = obj;
  }
  registerOnChange(fn: any): void {
    this.onModelChange = fn;
  }
  registerOnTouched(fn: any): void {
    this.onTouch = fn;
  }
  setDisabledState?(isDisabled: boolean): void {
    this.disabled = isDisabled;
  }

  constructor() {
    this.value = this.checked;
  }

  ngOnInit() {}

  changeEvent(evt, bool: boolean) {
    const charCode = evt.keyCode || evt.which;
    if (charCode === 32) {
      event.preventDefault();
      return evt.target.click();
    }
    this.value = bool;
    this.onModelChange(bool);
    this.onTouch();
  }
}
