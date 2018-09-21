import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs';
import { Subscription } from 'rxjs/Subscription';

function load_data<T>(
    obj: T,
    result: any,
    attr_map?: {[key: string]: any},
    list_map?: {[key: string]: any}): T {
  if(obj && result) {
    Object.assign(obj, result);
    if(attr_map) {
      for(let k in attr_map) {
        obj[k] = (result[k] === null || result[k] === undefined)
          ? null : (new Model[attr_map[k]])._load(result[k]);
      }
    }
    if(list_map) {
      for(let k in list_map) {
        obj[k] = (result[k] === null || result[k] === undefined)
          ? [] : result[k].map((v) => (new Model[list_map[k]])._load(v));
      }
    }
  }
  return obj;
}


export namespace Model {

  export interface ModelCtor<M extends BaseModel> {
    new (value?: any): M;
    propertyMap: {[key: string]: string};
    listPropertyMap: {[key: string]: string};
    resourceName: string;
    childResource: string;
    extPath: string;
  }

  export abstract class BaseModel {
    static propertyMap: {[key: string]: string} = {};
    static listPropertyMap: {[key: string]: string} = {};
    static resourceName: string;
    static childResource: string;
    static extPath: string;

    constructor(data?: any) {
      if(data !== undefined && data !== null) {
        this._load(data);
      }
    }

    _load<T extends BaseModel>(result: any) {
      let ctor = (this.constructor as ModelCtor<T>);
      return load_data(this, result, ctor.propertyMap, ctor.listPropertyMap);
    }

    get pageTitle(): string {
      return null;
    }
  }

  export class Address extends BaseModel {
    id: number;
    addressee: string;
    civic_address: string;
    city: string;
    province: string;
    postal_code: string;
    country: string;
    address_type: string;

    static resourceName = 'address';
  }

  export class Category extends BaseModel {
    id: number;
    type: string;
    value: string;

    static resourceName = 'category';
  }

  export class Contact extends BaseModel {
    id: number;
    credential: Credential;
    text: string;
    type: string;
    startDate: string;
    endDate: string;

    static resourceName = 'contact';

    static propertyMap = {
      credential: 'Credential',
    };

    get typeClass(): string {
      var t = this.type;
      if(t === 'contact.email') return 'email';
      if(t === 'contact.phone' || t == 'contact.phone-business') return 'phone';
      if(t === 'contact.website') return 'website';
      return 'contact';
    }
  }

  export class Credential extends BaseModel {
    id: number;
    credential_type: CredentialType;
    effective_date: string;
    inactive: boolean;
    revoked: boolean;

    addresses: Address[];
    categories: Category[];
    contacts: Contact[];
    names: Name[];
    people: Person[];
    topic: Topic;

    get pageTitle(): string {
      return this.credential_type && this.credential_type.description;
    }

    static resourceName = 'credential';

    static propertyMap = {
      credential_type: 'CredentialType',
      topic: 'Topic',
    };
    static listPropertyMap = {
      addresses: 'Address',
      categories: 'Category',
      contacts: 'Contact',
      names: 'Name',
      people: 'Person',
    };

    get issuer(): Issuer {
      return this.credential_type && this.credential_type.issuer;
    }
    set issuer(val: Issuer) {
    }
    get haveAddresses() {
      return this.topic.addresses && this.topic.addresses.length;
    }
    get haveContacts() {
      return this.contacts && this.contacts.length;
    }
    get haveNames() {
      return this.names && this.names.length;
    }
    get havePeople() {
      return this.people && this.people.length;
    }
    get haveCategories() {
      return this.categories && this.categories.length;
    }
  }

  export class CredentialFormatted extends Credential {
    static extPath = 'formatted';
  }

  export class CredentialSearchResult extends Credential {
    static resourceName = 'search/credential/topic';
  }

  export class CredentialVerifyResult extends BaseModel {
    success: boolean;
    result: any;

    static resourceName = 'credential';
    static extPath = 'verify';

    get claims() {
      let ret = [];
      if(typeof this.result === 'object' && this.result.proof) {
        let attrs = this.result.proof.requested_proof.revealed_attrs;
        for(let k in attrs) {
          ret.push({name: k, value: attrs[k].raw});
        }
      }
      ret.sort((a,b) => a.name.localeCompare(b.name));
      return ret;
    }

    get status(): string {
      return this.success ? 'cred.verified' : 'cred.not-verified';
    }

    get text(): string {
      if(typeof this.result === 'string')
        return this.result;
      return JSON.stringify(this.result, null, 2);
    }
  }

  export class CredentialType extends BaseModel {
    id: number;
    // schema: Schema;
    issuer: Issuer;
    description: string;
    // processorConfig: string;
    credential_def_id: string;
    // visible_fields: string;
    has_logo: boolean;

    static resourceName = 'credentialtype';

    static propertyMap = {
      issuer: 'Issuer',
    };

    get logo_url(): string {
      if(this.has_logo) {
        return `${CredentialType.resourceName}/${this.id}/logo`;
      }
    }
  }

  export class Issuer extends BaseModel {
    id: number;
    did: string;
    name: string;
    abbreviation: string;
    email: string;
    url: string;
    has_logo: boolean;

    static resourceName = 'issuer';

    get pageTitle(): string {
      return this.name;
    }

    get logo_url(): string {
      if(this.has_logo) {
        return `${Issuer.resourceName}/${this.id}/logo`;
      }
    }
  }

  export class IssuerCredentialType extends CredentialType {
    static resourceName = 'issuer';
    static childResource = 'credentialtype';
  }

  export class Name extends BaseModel {
    id: number;
    credential: Credential;
    text: string;
    type: string;
    startDate: string;
    endDate: string;

    // extra API fields
    // address: Address;
    issuer: Issuer;

    static resourceName = 'name';

    static propertyMap = {
      credential: 'Credential',
      issuer: 'Issuer',
    };
  }

  export class Person extends BaseModel {
    id: number;
    credential: Credential;
    fullName: string;
    type: string;
    startDate: string;
    endDate: string;

    static resourceName = 'person';

    static propertyMap = {
      credential: 'Credential',
    };
  }

  export class Topic extends BaseModel {
    id: number;
    source_id: string;
    type: string;

    addresses: Address[];
    names: Name[];
    contacts: Contact[];
    people: Person[];
    categories: Category[];

    static resourceName = 'topic';

    static propertyMap = {
      address: 'Address',
      category: 'Category',
    };

    get pageTitle(): string {
      if(this.names && this.names.length) {
        return this.names[0].text;
      }
    }

    get typeLabel(): string {
      if(this.type) return ('name.'+this.type).replace(/_/g, '-');
      return '';
    }

    get link(): string[] {
      return ['/topic/', this.type, this.source_id];
    }

    extLink(...args): string[] {
      return this.link.concat(args)
    }
  }

  export class TopicFormatted extends Topic {
    static extPath = 'formatted';
  }

  export class TopicRelatedFrom extends Topic {
    static childResource = 'related_from';
  }

  export class TopicRelatedTo extends Topic {
    static childResource = 'related_to';
  }

}
// end Model


export namespace Fetch {

  export class BaseResult<T> {
    public data: T;
    public meta: any;

    constructor(
      protected _ctor: (any) => T,
      protected _input?: any,
      public error?: any,
      public loading: boolean = false,
      _meta: any = null) {
        this.input = _input;
        this.meta = _meta || {};
    }

    get input(): any {
      return this._input;
    }

    set input(value: any) {
      this._input = value;
      this.data = value ? this._ctor(value) : null;
    }

    get empty(): boolean {
      return ! this.data;
    }

    get loaded(): boolean {
      return ! this.empty && ! this.loading;
    }

    get notFound(): boolean {
      return this.error && this.error.obj && this.error.obj.status === 404;
    }
  }

  export class Pagination {
    public pageNum: number = 1;
    public pageCount: number = 0;
    public resultCount: number = 0;
    public totalCount: number = 0;
    public firstIndex = 0;
    public lastIndex = 0;
    public timing: number = 0;
    public previous: string = null;
    public next: string = null;
    public params: {[key: string]: any};

    get havePrevious(): boolean {
      return this.previous != null;
    }

    get haveNext(): boolean {
      return this.next != null;
    }

    static fromResult(value: any): Pagination {
      let ret = new Pagination();
      if(value) {
        ret.pageNum = value.page || null;
        ret.firstIndex = value.first_index || null;
        ret.lastIndex = value.last_index || null;
        ret.totalCount = value.total || null;
        ret.next = value.next || null;
        ret.previous = value.previous || null;
      }
      return ret;
    }
  }

  export class ListResult<T> extends BaseResult<T[]> {
    public pagination: Pagination;
    public facets: any;

    set input(value: any) {
      this._input = value;
      if(value instanceof Array) {
        this.data = this._ctor(value);
      }
      else if(value && 'results' in value && value['results'] instanceof Array) {
        this.data = this._ctor(value['results']);
        this.pagination = Pagination.fromResult(value);
      }
      else {
        this.data = null;
      }
    }
  }

  export interface ResultCtor<T, R extends BaseResult<T>> {
    new (
      ctor: (any) => T,
      input?: any,
      error?: any,
      loading?: boolean,
      meta?: any): R;
  }

  export class RequestParams {
    path: string;
    resource: string;
    recordId: string;
    childResource: string;
    childId: string;
    extPath: string;

    static fromModel<M extends Model.BaseModel>(ctor: Model.ModelCtor<M>) {
      let req = new RequestParams();
      req.resource = ctor.resourceName;
      req.childResource = ctor.childResource;
      req.extPath = ctor.extPath;
      return req;
    }

    static from(params: any) {
      let req = new RequestParams();
      if(params)
        Object.assign(req, params);
      return req;
    }

    extend(info: RequestParams | { [key: string]: any }) {
      let ret = new RequestParams();
      Object.assign(ret, this);
      if(info)
        Object.assign(ret, info);
      return ret;
    }

    getRecordPath(recordId?: string, childId?: string, extPath?: string): string {
      let path = null;
      if(this.path) {
        path = this.path;
      }
      else if(this.resource) {
        if(! recordId) recordId = this.recordId;
        if(! extPath) extPath = this.extPath;
        if(recordId) {
          path = `${this.resource}/${recordId}`;
          if(this.childResource) {
            if(! childId) childId = this.childId;
            if(childId)
              path = `${path}/${this.childResource}/${childId}`;
            else
              path = null;
          }
          else if(extPath) {
            path = `${path}/${extPath}`;
          }
        }
      }
      return path;
    }

    getListPath(recordId?: string, extPath?: string): string {
      let path = null;
      if(this.path) {
        path = this.path;
      }
      else if(this.resource) {
        if(! recordId) recordId = this.recordId;
        if(! extPath) extPath = this.extPath;
        path = this.resource;
        if(this.childResource) {
          if(recordId)
            path = `${path}/${recordId}/${this.childResource}`;
          else
            path = null;
        }
        else if(extPath) {
          path = `${path}/${extPath}`;
        }
      }
      return path;
    }
  }

  export class BaseLoader<T, R extends BaseResult<T>> {
    _result: BehaviorSubject<R>;
    _sub: Subscription;

    constructor(
        protected _rctor: ResultCtor<T, R>,
        protected _map: (any) => T,
        protected _req?: RequestParams) {
      if(! this._req) this._req = new RequestParams();
      this._result = new BehaviorSubject(this._makeResult());
    }

    complete() {
      this._clearSub();
      if(this._result) {
        this._result.complete();
        this._result = null;
      }
    }

    reset() {
      this._clearSub();
      this.result = this._makeResult();
    }

    _clearSub() {
      if(this._sub) {
        this._sub.unsubscribe();
        this._sub = null;
      }
    }

    protected _makeResult(input?: any, error?: any, loading: boolean=false, meta=null) {
      return new this._rctor(this._map, input, error, loading, meta);
    }

    get stream(): Observable<R> {
      return this._result.asObservable();
    }

    get ready(): Observable<R> {
      return this.stream.filter(result => result.loaded);
    }

    get result(): R {
      return this._result.value;
    }

    set result(val: R) {
      this._result.next(val);
    }

    get request(): RequestParams {
      return this._req;
    }

    loadData(data: any, meta=null) {
      this.result = this._makeResult(data, null, false, meta);
    }

    loadError(err: any, meta=null) {
      this.result = this._makeResult(null, err, false, meta);
    }

    loadFrom(obs: Observable<any>, meta=null) {
      this._clearSub();
      this.result = this._makeResult(null, null, true, meta);
      this._sub = obs.subscribe(
        (result) => this.loadData(result, meta),
        (err) => this.loadError(err, meta)
      );
    }

    loadNotFound(meta=null) {
      this.loadError({obj: {status: 404}});
    }
  }

  export class DataLoader<T> extends BaseLoader<T, BaseResult<T>> {
    constructor(
        map: (any) => T,
        req?: RequestParams) {
      super(BaseResult, map, req);
    }
  }

  export class JsonLoader extends DataLoader<any> {
    constructor(req?: RequestParams) {
      super(val => val, req);
    }
  }

  export class ListLoader<T> extends BaseLoader<T[], ListResult<T>> {
    public pagination;

    constructor(
        protected _mapEntry: (any) => T,
        req?: RequestParams) {
      super(
        ListResult,
        data => {
          let list = null;
          if(data instanceof Array) {
            list = [];
            for(let row of data) {
              list.push(_mapEntry(row));
            }
          } else if(data) {
            console.error("Expected array");
          }
          return list;
        },
        req);
    }
  }

  export class ModelLoader<M extends Model.BaseModel> extends DataLoader<M> {
    constructor(ctor: Model.ModelCtor<M>, req?: RequestParams) {
      let creq = RequestParams.fromModel(ctor).extend(req);
      super((data) => new ctor(data), creq);
    }
  }

  export class ModelListLoader<M extends Model.BaseModel> extends ListLoader<M> {
    constructor(ctor: Model.ModelCtor<M>, req?: RequestParams) {
      let creq = RequestParams.fromModel(ctor).extend(req);
      super((data) => new ctor(data), creq);
    }
  }
}
// end Fetch
