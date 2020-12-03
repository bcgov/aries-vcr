import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlternateNamesComponent } from './alternate-names.component';

describe('AlternateNamesComponent', () => {
  let component: AlternateNamesComponent;
  let fixture: ComponentFixture<AlternateNamesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AlternateNamesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AlternateNamesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
