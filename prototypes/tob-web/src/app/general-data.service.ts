import { Injectable } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';
import { Subscription } from 'rxjs/Subscription';
import { map, catchError } from 'rxjs/operators';
import { _throw } from 'rxjs/observable/throw';
import { environment } from '../environments/environment';
import { Fetch, Filter, Model } from './data-types';


@Injectable()
export class GeneralDataService {

  public apiUrl = environment.API_URL;
  private _quickLoaded = false;
  private _orgData : {[key: string]: any} = {};
  private _recordCounts : {[key: string]: number} = {};
  private _currentResultSubj = new BehaviorSubject<Fetch.BaseResult<any>>(null);
  private _loaderSub: Subscription = null;
  private _defaultTopicType = 'registration';

  constructor(
    private _http: HttpClient,
    private _translate: TranslateService,
  ) {
  }

  get language() {
    return this._translate.currentLang;
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

  get defaultTopicType(): string {
    return this._defaultTopicType;
  }

  loadJson(url, params?: HttpParams) : Observable<Object> {
    return this._http.get(url, {params})
      .pipe(catchError(error => {
        console.error("JSON load error", error);
        return _throw(error);
      }));
  }

  postJson(url, payload, params?: HttpParams) : Observable<Object> {
    let headers = {'Content-Type': 'application/json'};
    return this._http.post(url, JSON.stringify(payload), {headers, params})
      .pipe(catchError(error => {
        console.error("JSON load error", error);
        return _throw(error);
      }));
  }

  postParams(url, params: {[key: string]: string}|HttpParams) : Observable<Object> {
    let body = this.makeHttpParams(params);
    return this._http.post(url, body)
      .pipe(catchError(error => {
        console.error("JSON load error", error);
        return _throw(error);
      }));
  }

  loadFromApi(path: string, params?: HttpParams) : Observable<Object> {
    let url = this.getRequestUrl(path);
    if(url) {
      return this.loadJson(url, params);
    }
  }

  quickLoad(force?) {
    return new Promise((resolve, reject) => {
      if(this._quickLoaded && !force) {
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
        .pipe(catchError(error => {
          console.error(error);
          return _throw(error);
        }));
      req.subscribe((data: any) => {
        if(data.counts) {
          for (let k in data.counts) {
            this._recordCounts[k] = parseInt(data.counts[k]);
          }
        }
        if(data.credential_counts) {
          for (let k in data.credential_counts) {
            this._recordCounts[k] = parseInt(data.credential_counts[k]);
          }
        }
        if(data.records) {
          for (let k in data.records) {
            this._orgData[k] = data.records[k];
          }
        }
        this._quickLoaded = true;
        resolve(1);
      }, err => {
        reject(err);
      });
    });
  }

  getRecordCount (type) {
    return this._recordCounts[type] || 0;
  }

  autocomplete (term) : Observable<Object> {
    if(term === '' || typeof(term) !== 'string') {
      return Observable.of([]);
    }
    let params = new HttpParams().set('q', term);
    return this.loadFromApi('search/autocomplete', params)
      .pipe(map(response => {
        let ret = [];
        for(let row of response['results']) {
          let found = null;
          for(let name of row.names) {
            if(~ name.text.toLowerCase().indexOf(term.toLowerCase())) {
              found = name.text;
              break;
            } else if(found === null) {
              found = name.text;
            }
          }
          if(found !== null) {
            ret.push({id: row.id, term: found});
          }
        }
        return ret;
      }));
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

  loadRecord <T>(
      fetch: Fetch.DataLoader<T>,
      id: string | number,
      params?: { [key: string ]: any }) {
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

  loadAll <M extends Model.BaseModel>(
      ctor: Model.ModelCtor<M>): Promise<M[]> {
    let loader = new Fetch.ModelListLoader<M>(ctor);
    let allRows: M[] = [];
    return new Promise((resolve, fail) => {
      loader.stream.subscribe(result => {
        // FIXME - implement pagination
        if(result.loaded) {
          allRows = allRows.concat(result.data);
          resolve(allRows);
        }
      });
      this.loadList(loader);
    });
  }

  loadData <T, R extends Fetch.BaseResult<T>>(fetch: Fetch.BaseLoader<T,R>, path: string, params?: { [key: string ]: any }) {
    if(! params) params = {};
    if(! path)
      // fetch.loadNotFound
      fetch.loadError("Undefined resource path");
    else {
      let httpParams = this.makeHttpParams(params.query);
      let url = this.getRequestUrl(path);
      if(params.primary) {
        if(this._loaderSub)
          this._loaderSub.unsubscribe();
        this._loaderSub = fetch.stream.subscribe((result) => {
          this.setCurrentResult(result);
        });
      }
      fetch.loadFrom(this.loadJson(url, httpParams), {url: url});
    }
  }

  public loadFacetOptions(data) {
    let fields = data.info && data.info.facets && data.info.facets.fields || {};
    let options = {
      credential_type_id: [],
      issuer_id: [],
      'category:entity_type': [],
    };
    if(fields) {
      for(let optname in fields) {
        for(let optitem of fields[optname]) {
          if(! optitem.count)
            // skip facets with no results
            continue;
          let optidx = optname;
          let optval: Filter.Option = {label: optitem.text, value: optitem.value, count: optitem.count};
          if(optname == 'category') {
            let optparts = optitem.value.split('::', 2);
            if(optparts.length == 2) {
              optidx = optname + ':' + optparts[0];
              let lblkey = `category.${optparts[0]}.${optparts[1]}`;
              let label = this._translate.instant(lblkey);
              if(label === lblkey || label === `??${lblkey}??`)
                label = optparts[1];
              optval = {
                label,
                value: optparts[1],
                count: optitem.count,
              };
            }
          }
          if(optidx in options) {
            options[optidx].push(optval);
          }
        }
      }
    }
    for(let name in options) {
      options[name].sort((a,b) => a.label.localeCompare(b.label));
    }
    return options;
  }

  onCurrentResult(sub): Subscription {
    return this._currentResultSubj.subscribe(sub);
  }

  setCurrentResult(result: Fetch.BaseResult<any>) {
    this._currentResultSubj.next(result);
  }

  deleteRecord (mod: string, id: string) {
    return new Promise(resolve => {
      let baseurl = this.getRequestUrl(mod + '/' + id + '/delete');
      let req = this._http.post(baseurl, {params: {id}})
        .pipe(catchError(error => {
          console.error(error);
          resolve(null);
          return _throw(error);
        }));
      req.subscribe(data => {
        console.log('delete result', data);
        resolve(data);
      });
    });
  }

}
