import { Injectable, Inject } from '@angular/core';
import { SearchClient } from './search.client';
import { SearchService } from './search.service';
import { CredResult } from '../data-types';


@Injectable()
export class CredSearchClient extends SearchClient<CredResult> {

  public method = 'creds';

  constructor(@Inject(SearchService) _service: SearchService) {
      super(_service);
  }

  loadResult(result: any): CredResult {
    return (new CredResult()).load(result);
  }

}
