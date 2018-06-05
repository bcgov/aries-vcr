import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';

import { GeneralDataService } from 'app/general-data.service';
import { SearchInfo, SearchResults } from './results.model';


@Injectable()
export class SearchService {

  constructor(
      private _dataService: GeneralDataService,
      private _http: Http,
  ) {
  }

  performSearch(query: string, params?: { [key: string]: string }): Observable<SearchResults<any>> {
    const data: any[] = [
      { 'name': 'value' },
    ];
    const info = new SearchInfo();
    info.pageNum = 1;
    const results = new SearchResults(info, data);
    return Observable.of(results);
  }

  realPerformSearch(query: string, params?: { [key: string]: string }) {
    /*return this.http.get<Item[]>(`${this.apiUrl}/view/projects`, this.options)
      .map( (response: HttpResponse<Item[]>) => {
        var result = response.body.map( (item:Item) =>
          Object.assign(new Item(),item) );
        console.log( result );
        return result;
      });*/
  }
}

