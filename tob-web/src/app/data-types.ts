
export interface VOType {
  id: number;
  theType: string;
  description: string;
  effectiveDate: string;
  expirationDate: string;
  displayOrder: number;
}

export interface VOLocationType {
  id: number;
  theType: string;
  description: string;
  effectiveDate: string;
  expirationDate: string;
  displayOrder: number;
}

export interface VOLocation {
  id: number;
  voLocationTypeId: VOLocationType;
  addressee?: string;
  addlDeliveryInfo?: string;
  unitNumber?: string;
  streetAddress?: string;
  municipality?: string;
  province?: string;
  postalCode?: string;
  latLong?: string;
}

export interface Jurisdiction {
  id: 0;
  jurisdictionAbbrv: string;
  jurisdictionName: string;
  displayOrder: number;
  isOnCommonList: true;
  effectiveDate: string;
  expirationDate: string;
}

export interface VerifiedOrg {
  id: number;
  busId: string;
  orgType: VOType;
  jurisdictionId: Jurisdiction;
  LegalName: string;
  primaryLocation: VOLocation;
  effectiveDate: string;
  endDate: string;
}
