import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { environment } from '../environments/environment';
import { Fetch } from './data-types';
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
    if(typeof path === 'string' && path.match(/^(\/\/|\w+:\/\/)\w/)) {
      // absolute URL
      return path;
    }
    let root = (<any>window).testApiUrl || this.apiUrl;

    if(root) {
      if(! root.endsWith('/')) root += '/';
      return root + path;
    }
  }

  loadJson(url, params?: HttpParams) : Observable<Object> {
    return this._http.get(url, {params: params})
      .catch(error => {
        console.error("JSON load error", error);
        return Observable.throw(error);
      });
  }

  loadFromApi(path: string, params?: HttpParams) : Observable<Object> {
    let url = this.getRequestUrl(path);
    if(url) {
      return this.loadJson(url, params);
    }
  }

  quickLoad(force?) {
    return new Promise((resolve, reject) => {
      if(this.quickLoaded && !force) {
        resolve(1);
        return;
      }
      let baseurl = this.getRequestUrl('');
      console.log('base url: ' + baseurl);
      if(! baseurl) {
        reject("Base URL not defined");
        return;
      }
      let req = this._http.get(baseurl + 'quickload')
        .catch(error => {
          console.error(error);
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
      }, err => {
        reject(err);
      });
    });
  }

  getRecordCount (type) {
    return this.recordCounts[type] || 0;
  }

  autocomplete (term) : Observable<Object> {
    if(term === '' || typeof(term) !== 'string') {
      return Observable.of([]);
    }
    let params = new HttpParams().set('q', term);
    return this.loadFromApi('search/autocomplete', params)
      .map(response => response["result"]);
  }

  makeHttpParams(query?: { [key: string ]: string } | HttpParams) {
    let httpParams: HttpParams;
    if(query instanceof HttpParams) {
      httpParams = query;
    } else {
      httpParams = new HttpParams();
      if(query) {
        for(let k in query) {
          httpParams = httpParams.set(k, query[k]);
        }
      }
    }
    return httpParams;
  }

  fixRecordId (id: number | string) {
    if(typeof id === 'number')
      id = ''+id;
    return id;
  }

  loadRecord <T>(fetch: Fetch.DataLoader<T>, id: string | number, params?: { [key: string ]: any }) {
    if(! params) params = {};
    let path = params.path || fetch.request.getRecordPath(
      this.fixRecordId(id), this.fixRecordId(params.childId), params.extPath);
    return this.loadData(fetch, path, params);
  }

  loadList <T>(fetch: Fetch.ListLoader<T>, params?: { [key: string ]: any }) {
    if(! params) params = {};
    let path = params.path || fetch.request.getListPath(params.parentId, params.extPath);
    return this.loadData(fetch, path, params);
  }

  loadData <T, R extends Fetch.BaseResult<T>>(fetch: Fetch.BaseLoader<T,R>, path: string, params?: { [key: string ]: any }) {
    if(! params) params = {};
    if(! path)
      fetch.loadError("Undefined resource path");
    else {
      let httpParams = this.makeHttpParams(params.query);
      let url = this.getRequestUrl(path);
      fetch.loadFrom(this.loadJson(url, httpParams), {url: url});
    }
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

}

