import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { environment } from '../environments/environment';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';


@Injectable()
export class GeneralDataService {

  public apiUrl = environment.API_URL;
  private quickLoaded = false;
  private orgData : {[key: string]: any} = {};
  private recordCounts : {[key: string]: number} = {};

  constructor(private _http: HttpClient) {
  }

  getRequestUrl(path: string) : string {
    let root = (<any>window).testApiUrl || this.apiUrl;
    // let root = 'http://localhost:8081'
    if(root) {
      if(! root.endsWith('/')) root += '/';
      return root + path;
    }
  }

  loadFromApi(path: string): Observable<Object> {
    let url = this.getRequestUrl(path);
    if(url) {
      return this._http.get(url)
        .catch(error => {
            console.error(error);
            return Observable.throw(error);
        });
    }
  }

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
      let req = this._http.get(baseurl + 'quickload')
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

  getRecordCount (type) {
    return this.recordCounts[type] || 0;
  }

  loadJson(url, params?) : Observable<Object> {
    let req = this._http.get(url, {params: params})
      .catch(error => {
        console.error("JSON load error", error);
        return Observable.throw(error);
      });
    return req;
  }

  deleteRecord (mod: string, id: string) {
    return new Promise(resolve => {
      let baseurl = this.getRequestUrl(mod + '/' + id + '/delete');
      let req = this._http.post(baseurl, {params: {id}})
        .catch(error => {
          console.error(error);
          resolve(null);
          return Observable.throw(error);
        });
      req.subscribe(data => {
        console.log('delete result', data);
        resolve(data);
      });
    });
  }

  verifyCred (credId: string) {
    return new Promise((resolve, reject) => {
      return resolve(this.loadFromApi(`credential/${credId}/verify`).toPromise());
    });
  }

}

