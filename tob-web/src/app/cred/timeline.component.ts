import { Component, OnInit, OnDestroy, Input, ChangeDetectionStrategy, Inject, LOCALE_ID } from '@angular/core';
import { GeneralDataService } from '../general-data.service';
import { Fetch, Model } from '../data-types';
import { Subscription } from 'rxjs/Subscription';
import { DateFormatPipe } from '../util/date-format.pipe';
import { LocalizeRouterService } from 'localize-router';


function escapeHtml(unsafe) {
  return unsafe.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
               .replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}

@Component({
  selector: 'credset-timeline',
  templateUrl: '../../themes/_active/cred/timeline.component.html',
  styleUrls: ['../../themes/_active/cred/timeline.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  providers: [{provide: LOCALE_ID, useValue: 'en-US'}],
})
export class CredSetTimelineComponent implements OnInit, OnDestroy {
  protected _topicId: number;
  private _range;
  private _rows = [];
  private _dateFormat: DateFormatPipe;

  private _loader: Fetch.ModelListLoader<Model.CredentialSet>;

  constructor(
    private _dataService: GeneralDataService,
    private _localize: LocalizeRouterService,
    @Inject(LOCALE_ID) _locale: string,
  ) {
    this._dateFormat = new DateFormatPipe(_locale);
  }

  ngOnInit() {
    this._loader = new Fetch.ModelListLoader(Model.CredentialSet);
    this._loader.stream.subscribe(this.updateRows.bind(this));
    this.load();
  }

  ngOnDestroy() {
    this._loader.complete();
  }

  get result$() {
    return this._loader.stream;
  }

  get topicId(): number {
    return this._topicId;
  }

  @Input() set topicId(newId: number) {
    this._topicId = newId;
    this.load();
  }

  get timelineRows() {
    return this._rows;
  }

  get timelineRange() {
    return this._range;
  }

  updateRows(result) {

/*
{"id":6,"effective_date":"2018-01-01T00:00:00Z","inactive":false,"latest":true,"revoked":false,
"revoked_date":null,"wallet_id":"8fbfbfd3-927f-406b-9097-a7c5d25fb923",
"credential_type":{"id":1,"issuer":{"id":1,"has_logo":true,
"create_timestamp":"2018-10-25T20:37:18.223961Z",
"update_timestamp":"2018-10-29T18:32:56.294364Z","did":"6qnvgJtqwK44D8LFYnV5Yf",
"name":"BC Corporate Registry","abbreviation":"BCReg","email":"bcregistries@gov.bc.ca",
"url":"https://www2.gov.bc.ca/gov/content/governments/organizational-structure/ministries-organizations/ministries/citizens-services/bc-registries-online-services"},
"has_logo":true,"create_timestamp":"2018-10-25T20:37:18.296796Z","update_timestamp":"2018-10-29T18:32:56.317809Z",
"description":"Registration","credential_def_id":"6qnvgJtqwK44D8LFYnV5Yf:3:CL:8:tag",
"schema":{"id":1,"create_timestamp":"2018-10-25T20:37:18.259216Z","update_timestamp":
"2018-10-29T18:32:56.312447Z","name":"registration.bc_registries","version":"1.0.36",
"origin_did":"6qnvgJtqwK44D8LFYnV5Yf"}},"addresses":[],"_attributes":[{"id":15554,"type":"registration_date","format":"datetime","value":"2018-01-01","credential_id":6},{"id":15555,"type":"entity_name_effective","format":"datetime","value":"2018-01-01T00:00:00Z","credential_id":6},{"id":15556,"type":"entity_name_assumed_effective","format":"datetime","value":"2018-01-01T00:00:00Z","credential_id":6},{"id":15557,"type":"entity_status","format":"category","value":"ACT","credential_id":6},{"id":15558,"type":"entity_status_effective","format":"datetime","value":"2018-01-01T00:00:00Z","credential_id":6},{"id":15559,"type":"entity_type","format":"category","value":"BC Company","credential_id":6},{"id":15560,"type":"registered_jurisdiction","format":"jurisdiction","value":"BC","credential_id":6},{"id":15561,"type":"home_jurisdiction","format":"jurisdiction","value":"BC","credential_id":6}],"_attribute_map":{"registration_date":{"id":15554,"type":"registration_date","format":"datetime","value":"2018-01-01","credential_id":6},"entity_name_effective":{"id":15555,"type":"entity_name_effective","format":"datetime","value":"2018-01-01T00:00:00Z","credential_id":6},"entity_name_assumed_effective":{"id":15556,"type":"entity_name_assumed_effective","format":"datetime","value":"2018-01-01T00:00:00Z","credential_id":6},"entity_status":{"id":15557,"type":"entity_status","format":"category","value":"ACT","credential_id":6},"entity_status_effective":{"id":15558,"type":"entity_status_effective","format":"datetime","value":"2018-01-01T00:00:00Z","credential_id":6},"entity_type":{"id":15559,"type":"entity_type","format":"category","value":"BC Company","credential_id":6},"registered_jurisdiction":{"id":15560,"type":"registered_jurisdiction","format":"jurisdiction","value":"BC","credential_id":6},"home_jurisdiction":{"id":15561,"type":"home_jurisdiction","format":"jurisdiction","value":"BC","credential_id":6}},"names":[{"id":1974,"text":"Wells Inc","language":null,"credential_id":6}],"topic":{"id":6,"create_timestamp":"2018-10-25T20:39:31.056281Z","update_timestamp":"2018-10-25T20:39:31.056327Z","source_id":"579139962e8fd","type":"registration","addresses":[],"_attributes":[{"id":15554,"type":"registration_date","format":"datetime","value":"2018-01-01","credential_id":6},{"id":15555,"type":"entity_name_effective","format":"datetime","value":"2018-01-01T00:00:00Z","credential_id":6},{"id":15556,"type":"entity_name_assumed_effective","format":"datetime","value":"2018-01-01T00:00:00Z","credential_id":6},{"id":15557,"type":"entity_status","format":"category","value":"ACT","credential_id":6},{"id":15558,"type":"entity_status_effective","format":"datetime","value":"2018-01-01T00:00:00Z","credential_id":6},{"id":15559,"type":"entity_type","format":"category","value":"BC Company","credential_id":6},{"id":15560,"type":"registered_jurisdiction","format":"jurisdiction","value":"BC","credential_id":6},{"id":15561,"type":"home_jurisdiction","format":"jurisdiction","value":"BC","credential_id":6}],"_attribute_map":{"registration_date":{"id":15554,"type":"registration_date","format":"datetime","value":"2018-01-01","credential_id":6},"entity_name_effective":{"id":15555,"type":"entity_name_effective","format":"datetime","value":"2018-01-01T00:00:00Z","credential_id":6},"entity_name_assumed_effective":{"id":15556,"type":"entity_name_assumed_effective","format":"datetime","value":"2018-01-01T00:00:00Z","credential_id":6},"entity_status":{"id":15557,"type":"entity_status","format":"category","value":"ACT","credential_id":6},"entity_status_effective":{"id":15558,"type":"entity_status_effective","format":"datetime","value":"2018-01-01T00:00:00Z","credential_id":6},"entity_type":{"id":15559,"type":"entity_type","format":"category","value":"BC Company","credential_id":6},"registered_jurisdiction":{"id":15560,"type":"registered_jurisdiction","format":"jurisdiction","value":"BC","credential_id":6},"home_jurisdiction":{"id":15561,"type":"home_jurisdiction","format":"jurisdiction","value":"BC","credential_id":6}},"names":[{"id":1974,"text":"Wells Inc","language":null,"credential_id":6}]}}
*/

    if(result.loaded) {
      let rows = [];
      let start = new Date();
      start.setFullYear(start.getFullYear() - 1);
      let end = new Date();
      end.setFullYear(end.getFullYear() + 1);
      let range = {start: start.toISOString(), end: end.toISOString()};
      for(let credset of result.data) {
        if(! credset.credentials) continue;
        if(credset.first_effective_date && credset.first_effective_date < range.start) {
          range.start = credset.first_effective_date;
        }
        if(credset.last_effective_date && credset.last_effective_date > range.end) {
          range.end = credset.last_effective_date;
        }
        let row = {
          id: `set-${credset.id}`,
          slots: []
        };
        for(let cred of credset.credentials) {
          let url = <string[]>this._localize.translateRoute(['/topic', cred.topic.id, 'cred', cred.id]);
          row.slots.push(
            {
              id: `cred-${cred.id}`,
              groups: [],
              htmlContent: this.htmlFormatCred(cred),
              start: cred.effective_date,
              end: cred.revoked_date,
              classNames: [cred.inactive ? 'slot-secondary' : 'slot-primary'],
              url: url.join('/'),
            }
          );
        }
        rows.push(row);
      }
      this._range = range;
      this._rows = rows;
    } else {
      this._rows = [];
    }
  }

  htmlFormatCred(cred): string {
    if(! cred) return '';
    let html = escapeHtml(cred.credential_type.description);
    if(cred.names && cred.names.length) {
      html += ' <nobr><strong><span class="fa fa-tag"></span> </nobr>' + escapeHtml(cred.names[0].text) + '</strong>';
      html += '<br>' + this._dateFormat.transform(cred.effective_date);
    }
    return html;
  }

  load() {
    if(this._loader && this._topicId) {
      this._dataService.loadList(this._loader, {parentId: this._topicId});
    }
  }
}
