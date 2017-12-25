import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import { MockData } from './mock-data';
import { VerifiableOrg } from './data-types';
import { environment } from '../environments/environment';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';


@Injectable()
export class GeneralDataService {

  public apiUrl = environment.API_URL;

  constructor(private http: Http) {
  }

  getRequestUrl(path: string) : string {
    let root = (<any>window).testApiUrl || this.apiUrl;
    if(root) {
      if(! root.endsWith('/')) root += '/';
      return root + path;
    }
  }

  loadFromApi(path: string): Observable<Object> {
    let url = this.getRequestUrl(path);
    if(url) {
      return this.http.get(url)
        .map((res: Response) => res.json())
        .catch(error => {
            console.error(error);
            return Observable.throw(error);
        });
    }
  }

  loadRecord(moduleId: string, recordId: string): Observable<Object> {
    let ret = this.loadFromApi(moduleId + '/' + recordId);
    if(! ret) {
      ret = Observable.create((obs) => {
        let data = new MockData();
        obs.next(data.fetchRecord(moduleId, recordId));
        obs.complete();
      });
    }
    return ret;
  }

  loadVerifiableOrg(recordId): Observable<VerifiableOrg> {
    return this.loadRecord('verifiableorgs', recordId)
      .map((res: Object) => {
        let row = <VerifiableOrg>res;
        /*let locs = this.getOrgData('locations');
        if(locs) {
          console.log('locs', locs);
          for (let j = 0; j < locs.length; j++) {
            let loc = <Location>locs[j];
            if (loc.verifiableOrgId === row.id && loc.locationTypeId === 1) {
              row.primaryLocation = locs[j];
            }
          }
        }
        if(! row.primaryLocation) {
          row.primaryLocation = (new MockData()).fetchRecord('verifiableorgs', 1).primaryLocation;
        }*/
        row.type = {
          id: 0,
          orgType: '',
          description: '',
          effectiveDate: '',
          endDate: '',
          displayOrder: 0,
        };
        return row;
      });
  }

  // -- client-side search implementation --

  private orgData : {[key: string]: any} = {};

  preloadData(reqTypes?) {
    return new Promise(resolve => {
      let baseurl = this.getRequestUrl('');
      console.log('base url: ' + baseurl);
      if(! baseurl) return;
      let types = reqTypes || ['verifiableorgtypes', 'locationtypes', 'jurisdictions', 'locations'];
      let wait = 0;
      for (let i = 0; i < types.length; i++) {
        let type = types[i];
        if(this.orgData[type]) continue;
        wait ++;
        let req = this.http.get(baseurl + type)
          .map((res: Response) => res.json())
          .catch(error => {
            console.error(error);
            if(! --wait) resolve(1);
            return Observable.throw(error);
          });
        req.subscribe(data => {
          console.log(type, data);
          this.orgData[type] = data;
          if(! --wait) resolve(1);
        });
      }
      if(! wait) resolve(0);
    });
  }

  findOrgData (type, id) : Object {
    if (this.orgData[type]) {
      for (let i = 0; i < this.orgData[type].length; i++) {
        if (this.orgData[type][i].id === id) {
          return this.orgData[type][i];
        }
      }
    }
  }

  getOrgData (type) : {[key:string]: Object} {
    return this.orgData[type];
  }

  searchLocs (query: string) {
    let adj = (loc) => {
      loc.type = this.findOrgData('locationtypes', loc.locationTypeId) || {};
    };
    return this.searchMod('locations', {text: query}, adj);
  }

  searchOrgs (query: string) {
    let adj = (org) => {
      let locs = this.orgData.locations;
      org.jurisdiction = this.findOrgData('jurisdictions', org.jurisdictionId) || {};
      org.type = this.findOrgData('verifiableorgtypes', org.orgTypeId) || {};
      org.primaryLocation = {summary: '', street: ''};
      if (locs) {
        for (let j = 0; j < locs.length; j++) {
          if (locs[j].verifiableOrgId === org.id && locs[j].locationTypeId === 1) {
            let loc = Object.assign({}, locs[j]);
            loc.street = loc.streetAddress || '';
            if(loc.unitNumber != null) {
              loc.street = '' + loc.unitNumber + '-' + loc.street;
            }
            loc.summary = '' + loc.municipality + ', ' + loc.province;
            org.primaryLocation = loc;
          }
        }
      }
    };
    return this.searchMod('verifiableorgs', {text: query}, adj);
  }

  searchMod (mod: string, params: any, adj: any) {
    return new Promise(resolve => {
      let baseurl = this.getRequestUrl('search/' + mod);
      let req = this.http.get(baseurl, {params: params})
        .map((res: Response) => res.json())
        .catch(error => {
          console.error(error);
          resolve(null);
          return Observable.throw(error);
        });
      req.subscribe(data => {
        console.log('search results', data);
        let orgs = [];
        if(Array.isArray(data)) {
          for(let i = 0; i < data.length; i++) {
            let org = Object.assign({}, data[i]);
            if(adj) adj(org);
            orgs.push(org);
          }
        }
        resolve(orgs);
      });
    });
  }

}

