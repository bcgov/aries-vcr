export interface IIssuer {
  id: number;
  has_logo: boolean;
  create_timestamp: Date;
  update_timestamp: Date;
  did: string;
  name: string;
  abbreviation: string
  email: string;
  url: string;
  endpoint: string;
}
