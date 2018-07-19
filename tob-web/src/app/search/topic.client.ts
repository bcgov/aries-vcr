import { Injectable, Inject } from '@angular/core';
import { SearchClient } from './search.client';
import { SearchService } from './search.service';
import { TopicResult } from '../data-types';


@Injectable()
export class TopicClient extends SearchClient<TopicResult> {

  public resource = 'topic';
  public childResource = 'formatted';

  constructor(@Inject(SearchService) _service: SearchService) {
      super(_service);
  }

  loadResult(result: any): TopicResult {
    return (new TopicResult()).load(result);
  }

}
