import { Injectable, Inject } from '@angular/core';
import { SearchClient } from './search.client';
import { SearchService } from './search.service';
import { IssuerResult } from '../data-types';


@Injectable()
export class IssuerClient extends SearchClient<IssuerResult> {

  public method = 'issuer';

  constructor(@Inject(SearchService) _service: SearchService) {
      super(_service);
  }

  loadResult(result: any): IssuerResult {
    return (new IssuerResult()).load(result);
  }

}
