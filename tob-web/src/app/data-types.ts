
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

export class CredentialResult {
  id: number;
  credential_type: CredTypeResult;
  issuer: IssuerResult;
  start_date: string;
  end_date: string;

  addresses: AddressResult[];
  contacts: ContactResult[];
  names: NameResult[];
  people: PersonResult[];

  load(result: any) {
    return load_data(this, result, {
      credential_type: CredTypeResult,
      issuer: IssuerResult,
    }, {
      addresses: AddressResult,
      contacts: ContactResult,
      names: NameResult,
      people: PersonResult,
    });
  }
}

export class CredResult {
  id: number;
  credential_type: CredTypeResult;
  start_date: string;
  end_date: string;

  // extra API fields
  addresses: AddressResult[];
  contacts: ContactResult[];
  names: NameResult[];
  people: PersonResult[];

  load(result: any) {
    return load_data(this, result, {
      credentialType: CredTypeResult,
    }, {
      addresses: AddressResult,
      contacts: ContactResult,
      names: NameResult,
      people: PersonResult,
    });
  }

  // get issuer(): IssuerResult {
  //   return this.credentialType && this.credentialType.issuer;
  // }
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
  did: string;
  name: string;
  abbreviation: string;
  email: string;
  url: string;

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
  // address: AddressResult;
  issuer: IssuerResult;

  load(result: any) {
    return load_data(this, result, {
      issuer: IssuerResult,
      credential: CredResult,
    });
  }

  // get issuer(): IssuerResult {
  //   return this.credential && this.credential.credentialType &&
  //     this.credential.credentialType.issuer;
  // }
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

export class TopicResult {
  id: number;
  source_id: string;
  type: string;

  addresses: AddressResult[];
  names: NameResult[];
  contacts: ContactResult[];
  people: PersonResult[];

  load(result: any) {
    return load_data(this, result, {
      address: AddressResult,
    });
  }

}

export class CredentialTypeResult {
  id: number;
  description: string;
  create_timestamp: string;

  load(result: any) {
    return load_data(this, result, {});
  }
}
