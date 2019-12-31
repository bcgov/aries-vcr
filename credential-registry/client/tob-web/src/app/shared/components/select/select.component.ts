import { Component, OnInit, Input } from '@angular/core';

export interface ISelectOption {
  value: string;
  description: string;
}

@Component({
  selector: 'app-select',
  templateUrl: './select.component.html',
  styleUrls: ['./select.component.scss'],
})
export class SelectComponent implements OnInit {
  @Input() options: ISelectOption[];
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

  constructor() {}

  ngOnInit() {}

  changeEvent(value: string) {
    console.log('select change', value);
    this.value = value;
    this.onModelChange(value);
    this.onTouch();
  }
}
