import { Component, OnInit, ChangeDetectionStrategy, Input } from '@angular/core';
import { IIssuer } from 'app/core/interfaces/i-issuer.interface';
import { ICredentialSet } from 'app/core/interfaces/i-credential-set.interface';
import { ICredential } from 'app/core/interfaces/i-credential.interface';

@Component({
  selector: 'app-topic-archive-list-header',
  templateUrl: '../../../themes/_active/cred/topic-archive-list-header.component.html',
  styleUrls: [
    '../../../themes/_active/cred/topic-archive-list-header.component.scss',
    '../../../themes/_active/cred/cred.scss',
    '../../../themes/_active/cred/list.component.scss',
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TopicArchiveListHeaderComponent implements OnInit {
  @Input() credSet: ICredentialSet;
  @Input() issuer: IIssuer;
  @Input() url: string;
  @Input() bg: boolean;
  currentCred: ICredential;
  expanded = false;
  credList: ICredential[];
  // dark: boolean;

  constructor() {}

  ngOnInit() {
    this.currentCred = this.credSet.credentials.filter(cred => cred.inactive === false)[0];
    this.credList = this.credSet.credentials.filter(cred => cred.inactive === true);
  }

  // registration-id / cred / topic id
  genLink(type: string, sourceId: string, id: string) {
    const vals = [];
    type === 'registration' ? vals.push('/topic/', sourceId) : vals.push('/topic/', type, sourceId);
    return vals.concat(type, id);
  }
}
