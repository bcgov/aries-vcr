import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import { MockData } from './mock-data';
import { VerifiedOrg } from './data-types';
import { environment } from '../environments/environment';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';


@Injectable()
export class GeneralDataService {

  public apiUrl = environment.TOB_API_URL;

  constructor(private http: Http) {
  }

  getRequestUrl(path: string) : string {
    let root = this.apiUrl;
    if(root) {
      if(! root.endsWith('/')) root += '/';
      return root + path;
    }
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

  loadVerifiedOrg(recordId): Observable<any> { // Observable<VerifiedOrg> {
    return this.loadRecord('verifiedorgs', recordId)
      .map((res: Object) => {
        let row : {[key:string]: any} = res; // <VerifiedOrg>res;
        row.primaryLocation = (new MockData()).fetchRecord('verifiedorgs', 1).primaryLocation;
        row.type = {};
        return row;
      });
  }

  // -- client-side search implementation --

  private orgData : {[key: string]: any} = {};

  preloadData() {
    let baseurl = this.getRequestUrl('');
    console.log('base url: ' + baseurl);
    if(! baseurl) return;
    let types = ['verifiedorgs', 'voorgtypes', 'jurisdictions', 'volocations'];
    for (let i = 0; i < types.length; i++) {
      let type = types[i];
      let req = this.http.get(baseurl + type)
        .map((res: Response) => res.json())
        .catch(error => {
          console.error(error);
          return Observable.throw(error);
        });
      req.subscribe(data => {
        console.log(type, data);
        this.orgData[type] = data;
      });
    }
  }

  findOrgData (type, id) {
    if (this.orgData[type]) {
      for (let i = 0; i < this.orgData[type].length; i++) {
        if (this.orgData[type][i].id === id) {
          return this.orgData[type][i];
        }
      }
    }
  }

  matchQuery (org, query) {
    let qp = ('' + query).toLowerCase().trim().split(/\s+/);
    let nm = org.LegalName.toLowerCase();
    if (!qp[0].length) {
      return 0;
    }
    if (nm.indexOf(qp.join(' ')) === 0) {
      return 2;
    }
    for (let i = 0; i < qp.length; i++) {
      if (nm.indexOf(qp) < 0) {
        return 0;
      }
    }
    return 1;
  }

  searchOrgs (query: string) {
    let fst = [];
    let lst = [];
    if (this.orgData.verifiedorgs) {
      let orgs = this.orgData.verifiedorgs;
      let locs = this.orgData.volocations;
      console.log(this.orgData);
      for (let i = 0; i < orgs.length; i++) {
        let org = Object.assign({}, orgs[i]);
        let m = this.matchQuery(org, query);
        if (m) {
          org.jurisdiction = this.findOrgData('jurisdictions', org.jurisdictionId) || {};
          org.type = this.findOrgData('voorgtypes', org.orgTypeId) || {};
          org.primaryLocation = {};
          if (locs) {
            for (let j = 0; j < locs.length; j++) {
              if (locs[j].verifiedOrgId === org.id && locs[j].voLocationTypeId === 1) {
                org.primaryLocation = locs[j];
              }
            }
          }
          if (m === 2) {
            fst.push(org);
          } else {
            lst.push(org);
          }
        }
      }
    }
    return fst.concat(lst);
  }

}

