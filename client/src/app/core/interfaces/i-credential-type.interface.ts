import { IIssuer } from "./i-issuer.interface";

export interface ICredentialType {
  id: number;
  issuer: IIssuer;
  has_logo: boolean;
  create_timestamp: string;
  update_timestamp: string;
  description: string;
  credential_def_id: string;
  last_issue_date: string;
  url: string;
  schema
}
