import { Injectable } from '@angular/core';
import { BehaviorSubject, of } from 'rxjs';
import { ICredentialSet } from 'app/core/interfaces/i-credential-set.interface';

export type StateOptions = 'true' | 'false' | '';
@Injectable({
  providedIn: 'root'
})
export class TopicStateService {
  currentState: StateOptions;

  filterActive = 'true';

  private credentialSets$ = new BehaviorSubject<ICredentialSet[]>(null);

  get credentialSets() {
    return this.credentialSets$.asObservable();
  }

  setCredential(credSets: ICredentialSet[]) {
    this.credentialSets$.next(credSets);
  }

  filterCredentials(
    issuerId: number,
    credentialType: number,
    credSet: ICredentialSet[]
  ) {
    if (!issuerId && !credentialType) {
      return this.credentialSets$.value;
    }
    const returnCreds = [];
    if (credentialType != null) {
      for (const creds of credSet) {
        if (
          creds.credentials.some(
            itm => itm.credential_type.id === credentialType
          )
        ) {
          returnCreds.push(creds);
        }
      }
    }
    if (issuerId != null) {
      for (const creds of credSet) {
        if (
          creds.credentials.some(
            itm => itm.credential_type.issuer.id === issuerId
          )
        ) {
          returnCreds.push(creds);
        }
      }
    }
    return returnCreds;
  }

  constructor() {}
}
