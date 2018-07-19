import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';
import 'rxjs/add/observable/fromPromise';

import { GeneralDataService } from 'app/general-data.service';
import { SearchInfo, SearchResults, SearchResult } from './results.model';


// TODO: Refactor this into a more generic APIservice with
//       search being one of its capabilities.
@Injectable()
export class SearchService {

  constructor(
      private _dataService: GeneralDataService,
      private _http: HttpClient,
  ) {
  }
  
  getById(resource: string, id: number): Observable<SearchResult<any>> {
    const promise = new Promise((resolve) => {
      this._dataService.loadFromApi(`api/v2/${resource}/${id}`).subscribe(
        (data: any) => {
          const info = new SearchInfo();
          resolve(new SearchResult(info, data))
        }
      )
    });
    return Observable.fromPromise(promise);
  }

  getRelatedById(resource: string, id: number, childResource: string): Observable<SearchResults<any>> {
    const promise = new Promise((resolve) => {
      this._dataService.loadFromApi(`api/v2/${resource}/${id}/${childResource}`).subscribe(
        (rows: any[] | any) => {

          // Sometimes this is an array of results.
          // Sometimes it's a single result.
          // More weirdness – needs refactor.
          if (rows instanceof Array) {
            const info = new SearchInfo();
            info.pageNum = 1;
            info.firstIndex = 1;
            info.lastIndex = rows.length;
            info.totalCount = rows.length;
            resolve(new SearchResults(info, rows))
          } else {
            // Single result
            const info = new SearchInfo();
            resolve(new SearchResult(info, rows))
          }
        }
      )
    });
    return Observable.fromPromise(promise);
  }

  performSearch(params?: { [key: string]: string }): Observable<SearchResults<any>> {
    if(! params) params = {};

    console.log(params)

    let promise = new Promise((resolve) => {
      function returnResult(rows: any[]) {
        const info = new SearchInfo();
        info.pageNum = 1;
        info.firstIndex = 1;
        info.lastIndex = rows.length;
        info.totalCount = rows.length;
        setTimeout(() => {
          resolve(new SearchResults(info, rows));
        }, 500);
      }

      // TODO: Refactor this into something better
      if (params.resource === 'topics') {
        this._dataService.loadFromApi(`api/v2/search/topic?${params.filter}=${params.query}`).subscribe(
          (rows: any[]) => {
            setTimeout
            returnResult(rows)
          }
        )
      } else if (params.resource === 'issuer') {
        this._dataService.loadFromApi(`api/v2/`).subscribe(
          (rows: any[]) => {
            setTimeout
            returnResult(rows)
          }
        )
      } else if (params.resource === 'creds' || params.resource == 'credtypes') {
        this._dataService.loadJson('assets/testdata/' + params.resource + '.json', {t: new Date().getTime()})
          .subscribe((rows: any[]) => {
            setTimeout
            returnResult(rows);
          });
      }
      else {
        returnResult([]);
      }
    });
    return Observable.fromPromise(promise);
  }

}

