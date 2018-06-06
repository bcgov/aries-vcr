
export interface DoingBusinessAs {
  id: number;
  verifiableOrgId: number;
  dbaName: string;
  effectiveDate: string;
  endDate: string;
  // custom properties
  locations?: Location[];
}

export interface InactiveClaimReason {
  id: number;
  shortReason: string;
  reason: string;
  effectiveDate: string;
  endDate: string;
  displayOrder: number;
}

export function blankInactiveClaimReason(): InactiveClaimReason {
  return {
    id: 0,
    shortReason: '',
    reason: '',
    effectiveDate: null,
    endDate: null,
    displayOrder: null
  };
}

export interface IssuerService {
  id: number;
  name: string;
  issuerOrgTLA: string;
  issuerOrgURL: string;
  DID: string;
  jurisdictionId: number;
  effectiveDate: string;
  endDate: string;
}

export function blankIssuerService(): IssuerService {
  return {
    id: 0,
    name: '',
    issuerOrgTLA: null,
    issuerOrgURL: null,
    DID: null,
    jurisdictionId: null,
    effectiveDate: null,
    endDate: null,
  }
}

export interface Location {
  id: number;
  verifiableOrgId: number;
  doingBusinessAsId: number;
  locationTypeId: number;
  addressee: string;
  addlDeliveryInfo: string;
  unitNumber: string;
  streetAddress: string;
  municipality: string;
  province: string;
  postalCode: string;
  latLong: string;
  effectiveDate: string;
  endDate: string;
  // custom properties
  summary?: string;
  type?: LocationType;
  typeName?: string;
}

export function blankLocation(): Location {
  return {
    id: 0,
    verifiableOrgId: null,
    doingBusinessAsId: null,
    locationTypeId: 1,
    addressee: '',
    addlDeliveryInfo: '',
    unitNumber: '',
    streetAddress: '',
    municipality: '',
    province: '',
    postalCode: '',
    latLong: '',
    effectiveDate: null,
    endDate: null,
    summary: '',
  };
}

export interface LocationType {
  id: number;
  locType: string;
  description: string;
  effectiveDate: string;
  endDate: string;
  displayOrder: number;
}

export function blankLocationType(): LocationType {
  return {
    id: 0,
    locType: '',
    description: '',
    effectiveDate: null,
    endDate: null,
    displayOrder: null,
  };
}

export interface Jurisdiction {
  id: number;
  abbrv: string;
  name: string;
  displayOrder: number;
  isOnCommonList: boolean;
  effectiveDate: string;
  endDate: string;
}

export function blankJurisdiction(): Jurisdiction {
  return {
    id: 0,
    abbrv: null,
    name: '',
    displayOrder: null,
    isOnCommonList: null,
    effectiveDate: null,
    endDate: null
  };
}

export interface VerifiableClaim {
  id: number;
  verifiableOrgId: number;
  claimType: number;
  claimJSON: number,
  effectiveDate: string;
  endDate: string;
  inactiveClaimReasonId: number;
  // custom properties
  color?: string;
  issuer?: IssuerService;
  type?: VerifiableClaimType;
  org?: VerifiableOrg;
  typeName?: string;
  inactiveReason?: InactiveClaimReason;
}

export interface VerifiableClaimType {
  id: number;
  claimType: string;
  schemaName: string;
  schemaVersion: string;
  base64Logo: string;
  issuerServiceId: number;
  issuerURL: string;
  effectiveDate: string;
  endDate: string;
}

export function blankClaimType(): VerifiableClaimType {
  return {
    id: 0,
    claimType: '',
    schemaName: null,
    schemaVersion: null,
    base64Logo: null,
    issuerServiceId: null,
    issuerURL: null,
    effectiveDate: null,
    endDate: null,
  };
}

export interface VerifiableOrg {
  id: number;
  orgId: string;
  orgTypeId: number;
  jurisdictionId: number;
  legalName: string;
  effectiveDate: string;
  endDate: string;
  // custom properties
  primaryLocation?: Location;
  type?: VerifiableOrgType;
  locations?: Location[];
  doingBusinessAs?: DoingBusinessAs[];
  claims?: VerifiableClaim[];
  typeName?: string;
}

export interface VerifiableOrgType {
  id: number;
  orgType: string;
  description: string;
  effectiveDate: string;
  endDate: string;
  displayOrder: number;
}

export function blankOrgType(): VerifiableOrgType {
  return {
    id: 0,
    orgType: '',
    description: null,
    effectiveDate: null,
    endDate: null,
    displayOrder: null,
  };
}


// v2 interface

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

