import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TranslateService } from '@ngx-translate/core';
import { GeneralDataService } from 'app/general-data.service';
import { Location, LocationType, VerifiableOrg, VerifiableOrgType, IssuerService, VerifiableClaim, VerifiableClaimType, DoingBusinessAs,
  blankLocation, blankOrgType, blankLocationType, blankIssuerService, blankClaimType } from '../data-types';
import * as compareVersions from 'compare-versions';

@Component({
  selector: 'app-roadmap',
  templateUrl: '../../themes/_active/roadmap/roadmap.component.html',
  styleUrls: ['../../themes/_active/roadmap/roadmap.component.scss']
})
export class RoadmapComponent implements OnInit {

  public recipeId : string;
  public recordId : string = '';
  public query : string = '';
  public error : string = '';
  public orgRecord;
  public recipe;
  public allResults;
  public results = [];
  public searchType = 'name';
  public currentLang : string;
  public registerLink : string;
  private searchTimer;
  private sub;
  private page = 0;
  public more = false;
  public less = false;
  public none = false;
  public inited = false;
  public loading = false;
  public loaded = false;
  public dbas: DoingBusinessAs[];
  public certs: any[];
  public locations: Location[];
  private preload;


  constructor(
    private dataService: GeneralDataService,
    private translate: TranslateService,
    private $route: ActivatedRoute,
    private $router: Router
  ) { }

  ngOnInit() {
    this.currentLang = this.translate.currentLang;
    this.preload = this.dataService.preloadData(['locations', 'locationtypes', 'verifiableclaimtypes', 'verifiableorgtypes']);
    this.$route.params.subscribe(params => {
      this.preload.then(() => this.loadRecipe(params.recipeId));
    });
  }

  loadRecipe(recipe) {
    this.recipeId = recipe;
    this.dataService.loadJson('assets/recipes/' + recipe + '.json').subscribe((data) => {

      // pre-index claim types by schema name with latest schema version
      let regTypes = <VerifiableClaimType[]>this.dataService.getOrgData('verifiableclaimtypes');
      let typesBySchema = {};
      for(let regType of regTypes) {
        if(regType.schemaName && regType.schemaVersion) {
          let sname = regType.schemaName;
          let other = typesBySchema[sname];

          // if(other && compareVersions(regType.schemaVersion, other.schemaVersion) <= 0)
          if(other && other.id < regType.id)
            continue;

          typesBySchema[sname] = regType;
        }
      }

      if(typesBySchema['incorporation.bc_registries']) {
        this.registerLink = typesBySchema['incorporation.bc_registries'].issuerURL;
      }

      let ctypes = data['claimTypes'] || [];
      let ctype;
      let dependIndex = {};
      data['claimTypes'] = [];
      ctypes.forEach(ctype_spec => {
        ctype = Object.assign({}, ctype_spec);
        ctype.cert = null;
        if(! ctype.schemaName || ! typesBySchema[ctype.schemaName]) return;
        ctype.regType = typesBySchema[ctype.schemaName];
        if(! ctype.regLink) ctype.regLink = ctype.regType.issuerURL;
        dependIndex[ctype.schemaName] = data['claimTypes'].length;
        data['claimTypes'].push(ctype);
      });

      // expand dependency information
      data['claimTypes'].forEach(ctype => {
        let depend_schemas = ctype['depends'] || [];
        let depends = [];
        depend_schemas.forEach(schema => {
          let depIdx = dependIndex[schema];
          if(depIdx !== undefined) depends.push(depIdx);
        });
        depends.sort();
        ctype['depends'] = depends;
      });

      this.recipe = data;
      console.log('recipe', data);
      this.$route.queryParams.subscribe(params => {
        this.setParams(params.record, params.query);
      });
    }, (failed) => {
      console.log('failed');
      this.error = "An error occurred while loading the recipe.";
    });
  }

  setParams(record, q) {
    if(typeof q !== 'string') q = '';
    this.recordId = record;
    if(this.query !== q || ! this.inited) {
      this.query = q;
      var search = (<HTMLInputElement>document.getElementById('searchInput'));
      if(search) search.value = this.query;
      this.preload.then(data => this.search());
    }
  }

  initSearch() {
    var search = (<HTMLInputElement>document.getElementById('searchInput'));
    if(search) search.value = this.query;
    this.focusSearch();
  }

  focusSearch() {
    var search = (<HTMLInputElement>document.getElementById('searchInput'));
    if(search) search.select();
  }

  inputEvent(evt) {
    if(evt.type === 'focus') {
      evt.target.parentNode.classList.add('active');
    } else if(evt.type === 'blur') {
      evt.target.parentNode.classList.remove('active');
    } else if(evt.type === 'input') {
      this.updateSearch(evt);
    }
  }

  updateSearch(evt) {
    let q = evt.target.value;
    let navParams = { queryParams: {}, relativeTo: this.$route };
    if(q !== undefined && q !== null) {
      q = q.trim();
      if(q !== '') {
        navParams.queryParams['query'] = q;
      }
    }
    if (this.searchTimer) clearTimeout(this.searchTimer);
    this.searchTimer = setTimeout(() => {
      this.$router.navigate(['./'], navParams);
    }, 150);
  }

  search(setType? : string) {
    if(this.recordId) {
      this.loadRecord();
      return;
    }

    let q = this.query.trim();
    this.loading = true;
    if(setType) {
      this.searchType = setType;
    }
    if(q.length) {
      let srch;
      if(this.searchType === 'name') {
        srch = this.sub = this.dataService.searchOrgs(q);
      } else {
        srch = this.sub = this.dataService.searchLocs(q);
      }
      this.sub.then(data => this.returnSearch(data, srch));
      this.sub.catch(err => this.searchError(err));
    } else {
      this.sub = null;
      this.returnSearch([], this.sub);
    }
  }

  loadRecord() {
    this.dataService.loadVerifiableOrg(this.recordId).subscribe((record : VerifiableOrg) => {
      console.log('verified org:', record);
      this.loaded = !!record;
      if(! record) this.error = 'Record not found';
      else {
        let orgType = <VerifiableOrgType>this.dataService.findOrgData('verifiableorgtypes', record.orgTypeId);
        record.type = orgType || blankOrgType();
        record.typeName = orgType && orgType.description;

        let orgLocs = [];
        let claimLocs = {};
        if(record.locations) {
          for(var i = 0; i < record.locations.length; i++) {
            let loc = <Location>Object.assign({}, record.locations[i]);
            let locType = <LocationType>this.dataService.findOrgData('locationtypes', loc.locationTypeId);
            loc.type = locType || blankLocationType();
            loc.typeName = locType && locType.locType;
            if(loc.doingBusinessAsId) {
              let cid = loc.doingBusinessAsId;
              if(! claimLocs[cid]) claimLocs[cid] = [];
              claimLocs[cid].push(loc);
            } else {
              orgLocs.push(loc);
            }
          }
        }
        this.locations = orgLocs;
        console.log('locations', orgLocs);

        let dbas = [];
        if(Array.isArray(record.doingBusinessAs)) {
          for(var i = 0; i < record.doingBusinessAs.length; i++) {
            let dba = <DoingBusinessAs>Object.assign({}, record.doingBusinessAs[i]);
            dba.locations = claimLocs[dba.id] || [];
            dbas.push(dba);
          }
        }
        this.dbas = dbas;
        console.log('dbas', dbas);

        this.certs = this.dataService.formatClaims(record.claims);
        console.log('claims', this.certs);
        let certPos = {};
        this.recipe.claimTypes.forEach( (ctype, idx) => {
          certPos[ctype.regType.id] = idx;
        });
        for(let i = 0; i < this.certs.length; i++) {
          let cert = <VerifiableClaim>this.certs[i].top;
          if(cert.type.id in certPos) {
            this.recipe.claimTypes[certPos[cert.type.id]].cert = cert;
          }
        }
      }

      this.orgRecord = record;
      this.inited = true;
    }, err => {
      this.error = err;
    });
  }

  setSearchType(evt) {
    if(this.searchType !== evt.target.value) {
      this.search(evt.target.value);
    }
    if(! this.query.trim().length) {
      this.focusSearch();
    }
  }

  returnSearch(data, from) {
    this.orgRecord = null;
    if(from !== this.sub) return;
    this.page = 0;
    this.allResults = data;
    this.paginate();
    this.loading = false;
    if(! this.inited) {
      this.inited = true;
      setTimeout(() => this.initSearch(), 100);
    }
  }

  searchError(err) {
    console.error(err);
    this.returnSearch([], this.sub);
  }

  paginate() {
    let rows = this.allResults || [];
    this.results = rows.slice(this.page * 10, (this.page + 1) * 10);
    this.more = (rows.length > (this.page + 1) * 10);
    this.less = (this.page > 0);
    this.none = (rows.length == 0);
  }

  prev() {
    this.page --;
    this.paginate();
  }

  next() {
    this.page ++;
    this.paginate();
  }
}
