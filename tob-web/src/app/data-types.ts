
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
          ? null : (new attr_map[k]).load(result[k]);
      }
    }
    if(list_map) {
      for(let k in list_map) {
        obj[k] = (result[k] === null || result[k] === undefined)
          ? [] : result[k].map((v) => (new list_map[k]).load(v));
      }
    }
  }
  return obj;
}

export class AddressResult {
  id: number;
  credential: CredResult;
  addressee: string;
  civicAddress: string;
  city: string;
  province: string;
  postalCode: string;
  country: string;
  addressType: string;
  startDate: string;
  endDate: string;

  load(result: any) {
    return load_data(this, result, {credential: CredResult});
  }
}

export class ContactResult {
  id: number;
  credential: CredResult;
  text: string;
  type: string;
  startDate: string;
  endDate: string;

  load(result: any) {
    return load_data(this, result, {credential: CredResult});
  }

  get typeClass(): string {
    var t = this.type;
    if(t === 'contact.email') return 'email';
    if(t === 'contact.phone' || t == 'contact.phone-business') return 'phone';
    if(t === 'contact.website') return 'website';
    return 'contact';
  }
}

export class CredResult {
  id: number;
  subject: SubjectResult;
  credentialType: CredTypeResult;
  startDate: string;
  endDate: string;

  // extra API fields
  addresses: AddressResult[];
  contacts: ContactResult[];
  names: NameResult[];
  people: PersonResult[];

  load(result: any) {
    return load_data(this, result, {
      credentialType: CredTypeResult,
      subject: SubjectResult,
    }, {
      addresses: AddressResult,
      contacts: ContactResult,
      names: NameResult,
      people: PersonResult,
    });
  }

  get issuer(): IssuerResult {
    return this.credentialType && this.credentialType.issuer;
  }
  get haveAddresses() {
    return this.addresses && this.addresses.length;
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
}

export class CredTypeResult {
  id: number;
  // schema: SchemaResult
  issuer: IssuerResult;
  description: string;
  // processorConfig: string;
  startDate: string;
  endDate: string;

  load(result: any) {
    return load_data(this, result, {
      issuer: IssuerResult
    });
  }
}

export class IssuerResult {
  id: number;
  // did: string;
  name: string;
  url: string;
  startDate: string;
  endDate: string;

  load(result: any) {
    return load_data(this, result);
  }
}

export class NameResult {
  id: number;
  credential: CredResult;
  text: string;
  type: string;
  startDate: string;
  endDate: string;

  // extra API fields
  address: AddressResult;

  load(result: any) {
    return load_data(this, result, {
      address: AddressResult,
      credential: CredResult,
    });
  }

  get issuer(): IssuerResult {
    return this.credential && this.credential.credentialType &&
      this.credential.credentialType.issuer;
  }
}

export class PersonResult {
  id: number;
  credential: CredResult;
  fullName: string;
  type: string;
  startDate: string;
  endDate: string;

  load(result: any) {
    return load_data(this, result, {
      credential: CredResult
    });
  }
}

export class SubjectResult {
  id: number;
  sourceId: string;
  initialCredential: CredResult;
  startDate: string;
  endDate: string;

  // extra API fields
  names: NameResult[];

  load(result: any) {
    return load_data(this, result, {
      initialCredential: CredResult
    }, {
      names: NameResult
    });
  }
}

