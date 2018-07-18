import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';
import 'rxjs/add/observable/fromPromise';

import { GeneralDataService } from 'app/general-data.service';
import { SearchInfo, SearchResults } from './results.model';


@Injectable()
export class SearchService {

  constructor(
      private _dataService: GeneralDataService,
      private _http: HttpClient,
  ) {
  }

  // TODO: be smarter
  performSearch(params?: { [key: string]: string }): Observable<SearchResults<any>> {
    if(! params) params = {};

    let promise = new Promise((resolve) => {
      function returnResult(rows: any[]) {
        console.log(rows)
        const info = new SearchInfo();
        info.pageNum = 1;
        info.firstIndex = 1;
        info.lastIndex = rows.length;
        info.totalCount = rows.length;
        setTimeout(() => {
          resolve(new SearchResults(info, rows));
        }, 500);
      }

      if (params.method === 'topics') {
        this._dataService.loadFromApi(`api/v2/search/topic?${params.filter}=${params.query}`).subscribe(
          (rows: any[]) => {
            setTimeout
            returnResult(rows)
          }
        )
      } else if(params.method === 'creds' || params.method == 'credtypes') {
        this._dataService.loadJson('assets/testdata/' + params.method + '.json', {t: new Date().getTime()})
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

