import { Component, OnInit, OnDestroy } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { IssuerResult, CredentialTypeResult } from '../data-types';
import { IssuerClient } from '../search/issuer.client';
import { IssuerCredentialTypeClient } from '../search/credential-type.client';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'issuer-form',
  templateUrl: '../../themes/_active/issuer/form.component.html',
  styleUrls: ['../../themes/_active/issuer/form.component.scss']
})
export class IssuerFormComponent implements OnInit, OnDestroy {
  id: number;
  loaded: boolean;
  credentialTypesLoaded: boolean;
  record: IssuerResult;
  credentialTypeRecords: CredentialTypeResult[];
  error: string;
  private _idSub: Subscription;
  private _issuerSub: Subscription;
  private _issuerCredentialTypeSub: Subscription;

  constructor(
    private _route: ActivatedRoute,
    private _issuerClient: IssuerClient,
    private _issuerCredentialTypeClient: IssuerCredentialTypeClient,
    private _sanitizer: DomSanitizer,
  ) { }

  ngOnInit() {
    this._idSub = this._route.params.subscribe(params => {
      this.id = +params['issuerId'];

      this._issuerSub = this._issuerClient.subscribe(this._receiveIssuer.bind(this))
      this._issuerClient.getById(this.id);

      this._issuerCredentialTypeSub = this._issuerCredentialTypeClient.subscribe(this._receiveCredentialTypes.bind(this))
      this._issuerCredentialTypeClient.getRelatedById(this.id);
    });
  }

  ngOnDestroy() {
    this._idSub.unsubscribe();
    this._issuerSub.unsubscribe();
    this._issuerCredentialTypeSub.unsubscribe();
  }

  get safeImg() {
    if(this.record.logo_b64) {
      let src = 'data:image/*;base64,' + this.record.logo_b64;
      return this._sanitizer.bypassSecurityTrustUrl(src);
    }
  }

  protected _receiveIssuer(loading: boolean) {
    if (!this._issuerClient.result) return;
    this.record = this._issuerClient.result.data;
    this.loaded = true;
  }

  protected _receiveCredentialTypes(loading: boolean) {
    if (!this._issuerCredentialTypeClient.results) return;
    this.credentialTypeRecords = this._issuerCredentialTypeClient.results.rows;
    this.credentialTypesLoaded = true;
  }

}
