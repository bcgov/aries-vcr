import { ICredentialType } from "./i-credential-type.interface";
import { ICredentialAddress, ICredentialAttribute, ICredentialName, ITopic, ICredentialSet } from "./i-credential-set.interface";

export interface ICredential {
  id: number;
  create_timestamp: Date;
  effective_date: Date;
  inactive:	boolean;
  latest:	boolean;
  revoked:	boolean;
  revoked_date:	Date;
  wallet_id: String;
  credential_type: ICredentialType
  credential_set?: ICredentialSet;
  addresses: ICredentialAddress[];
  attributes: ICredentialAttribute[];
  names: ICredentialName[];
  local_name: ICredentialName;
  remote_name: ICredentialName;
  topic: ITopic;
  related_topics: ITopic[];

}

export interface ICredentialByIdParams {
  name?: string;
  inactive?: string;
  latest?: string;
  revoked?: string;
  category?: string;
  credential_type_id?: string
  issuer_id?: string;
  topic_id?: string;
  id: string;
}

