export interface ICredentialTypeResult {
  total: number;
  page_size: number;
  page: number;
  first_index: number;
  last_index: number;
  next?: null;
  previous?: null;
  results?: ResultsEntity[] | null;
}
export interface ResultsEntity {
  id: number;
  issuer: Issuer;
  has_logo: boolean;
  create_timestamp: string;
  update_timestamp: string;
  description: string;
  credential_def_id: string;
  last_issue_date?: string | null;
  url: string;
  schema: Schema;
}
export interface Issuer {
  id: number;
  has_logo: boolean;
  create_timestamp: string;
  update_timestamp: string;
  did: string;
  name: string;
  abbreviation: string;
  email: string;
  url: string;
  endpoint: string;
}
export interface Schema {
  id: number;
  create_timestamp: string;
  update_timestamp: string;
  name: string;
  version: string;
  origin_did: string;
}
