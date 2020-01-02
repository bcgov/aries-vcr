import { IIssuer } from './i-issuer.interface';
import { ICredentialType } from './i-credential-type.interface';
import { ICredential } from './i-credential.interface';

export interface ICredentialSet {
  create_timestamp: string;
  credentials: ICredential[];
  first_effective_date: string;
  id: number;
  last_effective_date: string;
  topic_id: number;
  update_timestamp: string;
  remote_name: string;
}

export interface ICredentialAddress {
  update_timestamp: Date;
  create_timestamp: Date;
  city: string;
  civic_address: string;
  postal_code: string;
  province: string;
  credential_id: string;
  addressee: string;
  id: number;
}

export interface ICredentialAttribute {
  id: number;
  type: string;
  value: string;
  credential_id: string;
}

export interface ICredentialName {
  id: number;
  text: string;
  credential_id: string;
  type: string;
}

export interface ITopic {
  id: string;
  create_timestamp: Date;
  update_timestamp: Date;
  source_id: string;
  names: ICredentialName[];
  local_name: ICredentialName;
  remote_name: ICredentialName;
  addresses: ICredentialAddress;
  related_topics: any[];
}

export interface ISchema {
  id: number;
  create_timestamp: Date;
  update_timestamp: Date;
  name: string;
  version: string;
  origin_did: string;
}
