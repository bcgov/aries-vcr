import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import { MockData } from './mock-data';
import { VerifiedOrg } from './data-types';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';


@Injectable()
export class GeneralDataService {

  public apiUrl = 'http://127.0.0.1:8000/';

  constructor(private http: Http) {
    console.log(http);
  }

  getRequestUrl(path: string) : string {
    if(! this.apiUrl) return null;
    return this.apiUrl + path + '?pors_user_id=1';
  }

  loadRecord(moduleId: string, recordId: string): Observable<Object> {
    let url = this.getRequestUrl(moduleId + '/' + recordId);
    if(url) {
      return this.http.get(url)
        .map((res: Response) => res.json())
        .catch(error => {
            console.error(error);
            return Observable.throw(error);
        });
    }
    return Observable.create((obs) => {
      let data = new MockData();
      obs.next(data.fetchRecord(moduleId, recordId));
      obs.complete();
    });
  }

  loadVerifiedOrg(recordId): Observable<VerifiedOrg> {
    return this.loadRecord('verifiedOrgs', recordId)
      .map((res: Object) => <VerifiedOrg>res);
  }

}

