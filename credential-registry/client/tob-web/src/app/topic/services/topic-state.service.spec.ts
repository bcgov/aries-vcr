import { TestBed } from '@angular/core/testing';

import { TopicStateService } from './topic-state.service';

describe('TopicStateService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: TopicStateService = TestBed.get(TopicStateService);
    expect(service).toBeTruthy();
  });
});
