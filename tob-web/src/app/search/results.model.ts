
export class SearchInfo {
  public pageNum: number = 0;
  public pageCount: number = 0;
  public resultCount: number = 0;
  public totalCount: number = 0;
  public timing: number = 0;
  public params: {[key: string]: any};
}

export class SearchResults<T> {
  public info: SearchInfo;
  private _rows: T[] = [];

  constructor(
    info: SearchInfo,
    rows: T[]
  ) {
    this.info = info;
    this.rows = rows;
  }

  get rows() : T[] {
    return this._rows;
  }

  set rows(vals: T[]) {
    this._rows = [...vals];
  }
}
