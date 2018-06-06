import { Injectable, Inject } from '@angular/core';
import { SearchClient } from './search.client';
import { SearchService } from './search.service';
import { NameResult } from '../data-types';


@Injectable()
export class NameSearchClient extends SearchClient<NameResult> {

  public method = 'names';

  constructor(@Inject(SearchService) _service: SearchService) {
      super(_service);
  }

  loadResult(result: any): NameResult {
    return (new NameResult()).load(result);
  }

}
