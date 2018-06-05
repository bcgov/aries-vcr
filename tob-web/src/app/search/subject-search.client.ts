import { Injectable, Inject } from '@angular/core';
import { SearchClient } from './search.client';
import { SearchService } from './search.service';
import { Subject } from '../data-types';


@Injectable()
export class SubjectSearchClient extends SearchClient<Subject> {

  constructor(@Inject(SearchService) _service: SearchService) {
      super(_service);
  }

  loadResult(result: any): Subject {
    return Object.assign(new Subject(), result);
  }

}
