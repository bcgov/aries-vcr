import { Injectable, Inject } from '@angular/core';
import { SearchClient } from './search.client';
import { SearchService } from './search.service';
import { CredTypeResult } from '../data-types';


@Injectable()
export class CredTypeSearchClient extends SearchClient<CredTypeResult> {

  public method = 'credtypes';

  constructor(@Inject(SearchService) _service: SearchService) {
      super(_service);
  }

  loadResult(result: any): CredTypeResult {
    return (new CredTypeResult()).load(result);
  }

}
