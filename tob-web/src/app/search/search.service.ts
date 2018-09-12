import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { TranslateService } from '@ngx-translate/core';
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
    private _translate: TranslateService,
  ) {
  }

  getById(resource: string, id: number): Observable<SearchResult<any>> {
    const promise = new Promise((resolve, reject) => {
      this._dataService.loadFromApi(`${resource}/${id}`).subscribe(
        (data: any) => {
          const info = new SearchInfo();
          resolve(new SearchResult(info, data))
        },
        (err: any) => {
          reject(err);
        }
      )
    });
    return Observable.fromPromise(promise);
  }

  getRelatedById(resource: string, id: number, childResource: string): Observable<SearchResults<any>> {
    const promise = new Promise((resolve, reject) => {
      this._dataService.loadFromApi(`${resource}/${id}/${childResource}`).subscribe(
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
        },
        (err: any) => {
          reject(err);
        }
      )
    });
    return Observable.fromPromise(promise);
  }

  performSearch(params?: { [key: string]: string }): Observable<SearchResults<any>> {
    if(! params) params = {};

    let promise = new Promise((resolve, reject) => {
      function returnResult(
          rows: any[],
          info: any
      ) {
        const searchInfo = new SearchInfo();
        searchInfo.pageNum = info.page || null;
        searchInfo.firstIndex = info.firstIndex || null;
        searchInfo.lastIndex = info.lastIndex || null;
        searchInfo.totalCount = info.total || null;
        searchInfo.next = info.next || null;
        searchInfo.previous = info.previous || null;
        resolve(new SearchResults(searchInfo, rows));
      }
      function handle(request) {
        request.subscribe(
          (rows: any) => {
            returnResult(
              rows.results,
              {
                total: rows.total,
                // page_size: // rows.page_size,
                page: rows.page,
                firstIndex: rows.first_index,
                lastIndex: rows.last_index,
                next: rows.next,
                previous: rows.previous
              }
            );
          },
          (err: any) => {
            reject(err);
          });
      }

      // TODO: Refactor this into something better
      if (params.resource === 'credentials') {
        handle(this._dataService.loadFromApi(
          `search/credential?${params.filter}=${params.query}&page=${params.pageNum}`));
      } else if (params.resource === 'issuer') {
        handle(this._dataService.loadFromApi(``));
      } else if (params.resource === 'creds' || params.resource == 'credtypes') {
        handle(
          this._dataService.loadJson('assets/testdata/' + params.resource + '.json', {t: new Date().getTime()})
        );
      }
      else {
        returnResult([], {});
      }
    });
    return Observable.fromPromise(promise);
  }

  translateError(err: any): Observable<string> {
    if(! err) return Observable.create(null);
    if(err.status === 404) {
      return this._translate.get('general.not-found');
    }
    return this._translate.get('general.other-error');
  }

}

