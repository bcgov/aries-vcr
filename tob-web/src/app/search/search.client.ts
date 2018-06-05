import { Subscription } from 'rxjs/Subscription';
import { SearchResults } from './results.model';
import { SearchService } from './search.service';


export abstract class SearchClient<T> {

  public results: SearchResults<T>;
  public error: any;

  private _query: string;
  private _params: { [key: string]: any } = {};
  private _search: Subscription;

  constructor(
    protected _service : SearchService,
  ) {}

  get query() {
    return this._query;
  }

  set query(val: string) {
    this._query = val;
  }

  get params() {
    return this._params;
  }

  set params(params: { [key: string]: any }) {
    this._params = Object.assign({}, params);
  }

  get pageNum() {
    return parseInt(this._params['page']) || 0;
  }

  set pageNum(val: number) {
    this._params['page'] = val || 0;
  }

  updateParams(params: { [key: string]: any }) {
    this._params = Object.assign({}, this._params, params);
  }

  performSearch() {
    this.pageNum = 0;
    this.updateSearch();
  }

  updateSearch() {
    this.cancelSearch();
    this._search = this._service.performSearch(this._query, this._params)
      .subscribe(
        this.returnResults.bind(this),
        this.returnError.bind(this),
        this.searchUpdated.bind(this));
  }

  cancelSearch() {
    if(this._search) {
      this._search.unsubscribe();
      this._search = null;
    }
  }

  nextPage() {
  }

  previousPage() {
  }

  private returnResults(results: SearchResults<any>) {
    this.results = new SearchResults(
      results.info,
      this.loadResults(results.rows));
  }

  loadResults(results: any[]): T[] {
    return results.map(this.loadResult, this);
  }

  abstract loadResult(result: any): T;

  private returnError(err: any) {
    console.error('got error: ', err);
  }

  private searchUpdated() {
    console.log('results updated');
  }

}
