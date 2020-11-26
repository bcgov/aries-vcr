import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { DevelopComponent } from './develop.component';

describe('DevelopComponent', () => {
  let component: DevelopComponent;
  let fixture: ComponentFixture<DevelopComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ DevelopComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DevelopComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
