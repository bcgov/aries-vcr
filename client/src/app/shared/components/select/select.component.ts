import { Component, Input, forwardRef } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { ControlValueAccessor, FormControl, NG_VALUE_ACCESSOR } from '@angular/forms';

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
export class SelectComponent implements ControlValueAccessor {
  private select = new FormControl('');

  @Input() options: ISelectOption[];
  @Input() translateSelector: string;

  onTouch: (any) => void;

  constructor(public translate: TranslateService) { }

  writeValue(value: any): void {
    value && this.select.setValue(value);
  }

  registerOnChange(fn: any): void {
    this.select.valueChanges.subscribe(fn);
  }

  registerOnTouched(fn: any): void {
    this.onTouch = fn;
  }

  setDisabledState?(isDisabled: boolean): void {
    isDisabled ? this.select.disable() : this.select.enable();
  }

  changeEvent(value: string) {
    this.select.setValue(value);
    this.onTouch(value);
  }
}
