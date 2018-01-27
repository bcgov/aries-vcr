import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import { MockData } from './mock-data';
import {
    VerifiableOrg, VerifiableOrgType, VerifiableClaim, VerifiableClaimType, IssuerService, Jurisdiction,
    blankOrgType, blankClaimType, blankIssuerService, blankJurisdiction } from './data-types';
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
  private quickLoaded = false;
  private recordCounts : {[key: string]: number} = {};

  quickLoad(force?) {
    return new Promise(resolve => {
      if(this.quickLoaded && !force) {
        resolve(1);
        return;
      }
      let baseurl = this.getRequestUrl('');
      console.log('base url: ' + baseurl);
      if(! baseurl) {
        resolve(0);
        return;
      }
      let req = this.http.get(baseurl + 'quickload')
        .map((res: Response) => res.json())
        .catch(error => {
          console.error(error);
          resolve(1);
          return Observable.throw(error);
        });
      req.subscribe(data => {
        console.log('quickload', data);
        if(data.counts) {
          for (let k in data.counts) {
            this.recordCounts[k] = parseInt(data.counts[k]);
          }
        }
        if(data.records) {
          for (let k in data.records) {
            this.orgData[k] = data.records[k];
          }
        }
        this.quickLoaded = true;
        resolve(1);
      });
    });
  }

  preloadData(reqTypes?) {
    return this.quickLoad().then(response => new Promise(resolve => {
      let baseurl = this.getRequestUrl('');
      console.log('base url: ' + baseurl);
      if(! baseurl) {
        resolve(0);
        return;
      }
      let types = reqTypes || ['issuerservices', 'jurisdictions', 'locationtypes', 'verifiableclaimtypes', 'verifiableorgtypes'];
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
    }));
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

  getRecordCount (type) {
    return this.recordCounts[type] || 0;
  }

  getOrgData (type) : Object[] {
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
      org.jurisdiction = <Jurisdiction>this.findOrgData('jurisdictions', org.jurisdictionId) || blankJurisdiction();
      org.type = <VerifiableOrgType>this.findOrgData('verifiableorgtypes', org.orgTypeId) || blankOrgType();
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

  formatClaim(claim : VerifiableClaim) {
    let type = <VerifiableClaimType>this.findOrgData('verifiableclaimtypes', claim.claimType);
    claim.type = type || blankClaimType();
    claim.typeName = type.claimType || '';
    claim.color = ['green', 'orange', 'blue', 'purple'][claim.claimType % 4];
    let issuer = <IssuerService>this.findOrgData('issuerservices', type.issuerServiceId);
    claim.issuer = issuer || blankIssuerService();
    return claim;
  }

  formatClaims(claims) {
    if (!claims) claims = [];
    let result = [];
    let seen = {};
    let sorted = this.sortClaims(claims);
    for(var i = 0; i < sorted.length; i++) {
      let claim = <VerifiableClaim>Object.assign({}, sorted[i]);
      let grp = seen[claim.claimType];
      if(! grp) {
        grp = seen[claim.claimType] = {others: []};
        grp.top = this.formatClaim(claim);
        result.push(grp);
      } else {
        grp.others.push(claim);
      }
    }
    return result;
  }

  sortClaims(claims) {
    let base = (claims || []).slice();
    return base.sort((a, b) => b.effectiveDate.localeCompare(a.effectiveDate));
  }

}

