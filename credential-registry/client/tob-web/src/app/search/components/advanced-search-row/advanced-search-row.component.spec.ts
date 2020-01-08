import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdvancedSearchRowComponent } from './advanced-search-row.component';

describe('AdvancedSearchRowComponent', () => {
  let component: AdvancedSearchRowComponent;
  let fixture: ComponentFixture<AdvancedSearchRowComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdvancedSearchRowComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdvancedSearchRowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
