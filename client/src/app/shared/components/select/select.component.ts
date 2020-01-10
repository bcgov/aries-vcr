import { Component, OnInit, Input, forwardRef } from '@angular/core';
import { LangChangeEvent, TranslateService } from '@ngx-translate/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

export interface ISelectOption {
  value: string | boolean | number;
  description: string;
}

@Component({
  selector: 'app-select',
  templateUrl: '../../../../themes/_active/shared/select.component.html',
  styleUrls: ['../../../../themes/_active/shared/select.component.scss'],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => SelectComponent),
      multi: true,
    },
  ],
})
export class SelectComponent implements OnInit, ControlValueAccessor {
  @Input() options: ISelectOption[];
  @Input() selected: ISelectOption;

  value: any;
  onModelChange: (any) => void;
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

  constructor(public translate: TranslateService) {}

  ngOnInit() {}

  changeEvent(value: string) {
    this.value = value;
    this.onModelChange(value);
    this.onTouch();
  }
}
