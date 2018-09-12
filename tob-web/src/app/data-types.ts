
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

// TODO: convert response format to camelCase?
export class AddressResult {
  id: number;
  addressee: string;
  civic_address: string;
  city: string;
  province: string;
  postal_code: string;
  country: string;
  address_type: string;

  load(result: any) {
    return load_data(this, result, {});
  }
}

export class CategoryResult {
  id: number;
  type: string;
  value: string;

  load(result: any) {
    return load_data(this, result, {});
  }
}

export class ContactResult {
  id: number;
  credential: CredentialResult;
  text: string;
  type: string;
  startDate: string;
  endDate: string;

  load(result: any) {
    return load_data(this, result, {credential: CredentialResult});
  }

  get typeClass(): string {
    var t = this.type;
    if(t === 'contact.email') return 'email';
    if(t === 'contact.phone' || t == 'contact.phone-business') return 'phone';
    if(t === 'contact.website') return 'website';
    return 'contact';
  }
}

export class CredentialResult {
  id: number;
  credential_type: CredentialTypeResult;
  effective_date: string;
  revoked: string;

  addresses: AddressResult[];
  categories: CategoryResult[];
  contacts: ContactResult[];
  names: NameResult[];
  people: PersonResult[];
  topic: TopicResult;

  load(result: any) {
    return load_data(this, result, {
      credential_type: CredentialTypeResult,
      topic: TopicResult,
    }, {
      addresses: AddressResult,
      categories: CategoryResult,
      contacts: ContactResult,
      names: NameResult,
      people: PersonResult,
    });
  }

  get issuer(): IssuerResult {
    return this.credential_type && this.credential_type.issuer;
  }
  set issuer(val: IssuerResult) {
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
  get haveCategories() {
    return this.categories && this.categories.length;
  }
}


export class CredentialTypeResult {
  id: number;
  // schema: SchemaResult;
  issuer: IssuerResult;
  description: string;
  // processorConfig: string;
  credential_def_id: string;
  logo_b64: string;
  // visible_fields: string;

  load(result: any) {
    return load_data(this, result, {
      issuer: IssuerResult
    });
  }
}

export class IssuerResult {
  id: number;
  did: string;
  name: string;
  abbreviation: string;
  email: string;
  url: string;
  logo_b64: string;

  load(result: any) {
    return load_data(this, result);
  }
}

export class NameResult {
  id: number;
  credential: CredentialResult;
  text: string;
  type: string;
  startDate: string;
  endDate: string;

  // extra API fields
  // address: AddressResult;
  issuer: IssuerResult;

  load(result: any) {
    return load_data(this, result, {
      issuer: IssuerResult,
      credential: CredentialResult,
    });
  }
}


  // get issuer(): IssuerResult {
  //   return this.credential && this.credential.credentialType &&
  //     this.credential.credentialType.issuer;
  // }


export class PersonResult {
  id: number;
  credential: CredentialResult;
  fullName: string;
  type: string;
  startDate: string;
  endDate: string;

  load(result: any) {
    return load_data(this, result, {
      credential: CredentialResult
    });
  }
}

export class TopicResult {
  id: number;
  source_id: string;
  type: string;

  addresses: AddressResult[];
  names: NameResult[];
  contacts: ContactResult[];
  people: PersonResult[];
  categories: CategoryResult[];

  load(result: any) {
    return load_data(this, result, {
      address: AddressResult,
      category: CategoryResult
    });
  }

  get typeLabel(): string {
    if(this.type) return ('name.'+this.type).replace(/_/g, '-');
    return '';
  }
}

