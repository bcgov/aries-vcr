import { Injectable, Inject } from '@angular/core';
import { SearchClient } from './search.client';
import { SearchService } from './search.service';
import { CredentialTypeResult } from '../data-types';


@Injectable()
export class IssuerCredentialTypeClient extends SearchClient<CredentialTypeResult> {

  public resource = 'issuer';
  public childResource = 'credentialtype';

  constructor(@Inject(SearchService) _service: SearchService) {
      super(_service);
  }

  loadResult(result: any): CredentialTypeResult {
    return (new CredentialTypeResult()).load(result);
  }

}
