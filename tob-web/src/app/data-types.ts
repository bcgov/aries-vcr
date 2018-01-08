
export interface DoingBusinessAs {
  id: number;
  verifiableOrgId: number;
  dbaName: string;
  effectiveDate: string;
  endDate: string;
  // custom properties
  locations?: Location[];
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
