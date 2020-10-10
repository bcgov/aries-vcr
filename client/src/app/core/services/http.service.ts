import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { of, Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { API_URL } from './api.service';

@Injectable({
  providedIn: 'root',
})
export class HttpService {

  constructor(
    @Inject(API_URL) private baseUrl: string,
    private http: HttpClient
  ) { }

  httpGetRequest<T>(path: string, params: { [param: string]: string } = {}): Observable<T> {
    return this.http.get<T>(`${this.baseUrl}/${path}`, { params });
    // .pipe(catchError(err => of(err)));
  }

  credentialSet(id: number) {
    return `topic/${id}/credentialset`;
  }
}
