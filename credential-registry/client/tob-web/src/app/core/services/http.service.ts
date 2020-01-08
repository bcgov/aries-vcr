import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'environments/environment';
import { of, Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';

const apiUrl = environment.API_URL;

@Injectable({
  providedIn: 'root',
})
export class HttpService {
  private baseUrl: string;

  credentialSet(id: number) {
    return `topic/${id}/credentialset`;
  }

  constructor(private http: HttpClient) {
    this.baseUrl = apiUrl;
  }

  httpGetRequest<T>(path: string, params: { [param: string]: string } = {}): Observable<T> {
    return this.http.get<T>(`${this.baseUrl}/${path}`, { params });
    // .pipe(catchError(err => of(err)));
  }
}
