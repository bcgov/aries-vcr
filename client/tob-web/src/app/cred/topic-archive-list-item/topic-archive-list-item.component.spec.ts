import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TopicArchiveListItemComponent } from './topic-archive-list-item.component';

describe('TopicArchiveListItemComponent', () => {
  let component: TopicArchiveListItemComponent;
  let fixture: ComponentFixture<TopicArchiveListItemComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TopicArchiveListItemComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TopicArchiveListItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
