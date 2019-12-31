import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CheckboxComponent } from './components/checkbox/checkbox.component';
import { SelectComponent } from './components/select/select.component';

@NgModule({
  imports: [CommonModule],
  declarations: [CheckboxComponent, SelectComponent],
  exports: [CheckboxComponent, SelectComponent],
})
export class SharedModule {}
