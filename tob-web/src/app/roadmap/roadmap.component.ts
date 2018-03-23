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
      if(regTypes) {
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
      }

      if(typesBySchema['incorporation.bc_registries']) {
        this.registerLink = typesBySchema['incorporation.bc_registries'].issuerURL;
      }

      let ctypes = data['claimTypes'] || [];
      let ctype;
      let dependsMap = {};
      data['claimTypes'] = [];
      ctypes.forEach((ctype_spec, idx) => {
        ctype = Object.assign({}, ctype_spec);
        ctype.cert = null;
        if(! ctype.schemaName || ! typesBySchema[ctype.schemaName]) return;
        ctype.regType = typesBySchema[ctype.schemaName];
        if(! ctype.regLink) ctype.regLink = ctype.regType.issuerURL;
        dependsMap[ctype.schemaName] = ctype.depends || [];
        ctype.oldIdx = idx;
        data['claimTypes'].push(ctype);
      });
      this.expandDepends(dependsMap);

      data['claimTypes'].sort(this.cmpDependClaims(dependsMap));
      let dependIndex = {};
      data['claimTypes'].forEach( (ctype, idx) => {
        dependIndex[ctype['schemaName']] = idx;
      });

      // expand dependency information
      data['claimTypes'].forEach(ctype => {
        let claimDeps = [];
        if(ctype.schemaName in dependsMap) {
          dependsMap[ctype.schemaName].forEach(schema => {
            if(schema in dependIndex)
              claimDeps.push(dependIndex[schema]);
          });
        }
        claimDeps.sort();
        ctype['depends'] = claimDeps.length ? claimDeps : null;
      });

      let dependsMapIdx = {};
      for(let schema in dependsMap) {
        dependsMapIdx[dependIndex[schema]] = dependsMap[schema].map(schema => ''+dependIndex[schema]);
      }
      try {
        let tree = this.makeDependsTree(Object.keys(dependsMapIdx), dependsMapIdx);
        console.log('tree', tree);
        if(! tree[1].length) {
          // no remaining, tree should be good
          data['tree'] = tree[0];
        }
      } catch(e) {
        console.error(e);
      }
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

  cmpDependClaims(dependsMap) {
    return (a, b) => {
      let schemaA = a.schemaName;
      let schemaB = b.schemaName;
      if(schemaA in dependsMap && ~dependsMap[schemaA].indexOf(schemaB)) return 1;
      if(schemaB in dependsMap && ~dependsMap[schemaB].indexOf(schemaA)) return -1;
      return (a.oldIdx == b.oldIdx ? 0 : (a.oldIdx < b.oldIdx ? 1 : -1));
    }
  }

  makeDependsTree(claims, allDepends, remainDepends?, parents?, depth?) {
    let topClaims = [];
    let remain = [];
    if(! remainDepends) {
      remainDepends = new Set(Object.keys(allDepends));
    }
    let nextDepends = new Set(remainDepends);
    let idx = 0;
    if(! depth) depth = 0;
    if(! parents) parents = [];
    // identify claims with no unsatisfied dependencies
    for(; idx < claims.length; idx++) {
      let claim = claims[idx];
      let noRemain = true;
      let depends = allDepends[claim];
      if(depends) {
        for(let dep of depends) {
          if(remainDepends.has(dep)) {
            noRemain = false;
            break;
          }
        }
      }
      if(noRemain) {
        topClaims.push(claim);
        nextDepends.delete(claim);
      } else {
        remain.push(claim);
      }
    }
    if(! topClaims.length) {
      return [[], remain];
    }
    // initialize buckets for each parent of this level
    let buckets = [];
    // split top level claims into buckets
    topClaims.forEach(claim => {
      let parentClaims = [];
      if(parents.length) {
        parents.forEach(parentClaim => {
          if(~allDepends[claim].indexOf(parentClaim))
            parentClaims.push(parentClaim);
        });
      }
      let key = parentClaims.join(',');
      let found = null;
      for(let idx = 0; idx < buckets.length; idx++) {
        if(buckets[idx]['key'] === key) {
          found = idx;
          break;
        }
      }
      if(found === null) {
        found = buckets.length;
        buckets.push({'key': key, 'parents': parentClaims, 'nodes': [], 'next': []});
      }
      let node = {'id': claim, 'children': [], 'descends': []};
      if(remain.length) {
        let nodeDepends = new Set(remainDepends);
        nodeDepends.delete(claim);
        let nodeNext = this.makeDependsTree(remain, allDepends, nodeDepends, [claim], depth+1);
        node['children'] = nodeNext[0];
        remain.forEach(claim => {
          if(! ~nodeNext[1].indexOf(claim)) {
            node['descends'].push(claim);
            nextDepends.delete(claim);
          }
        });
        remain = nodeNext[1];
      }
      buckets[found]['nodes'].push(node);
    });
    // add additional levels to each bucket if needed
    buckets.forEach(bucket => {
      if(! remain.length) return;
      let bucketDepends = new Set(remainDepends);
      let nodeIds = bucket['nodes'].map(node => node['id']);
      nodeIds.forEach(id => bucketDepends.delete(id));
      let bucketNext = this.makeDependsTree(remain, allDepends, bucketDepends, nodeIds, depth+1);
      bucket['next'] = bucketNext[0];
      remain = bucketNext[1];
    });
    // assign remaining claims to additional levels
    let bottom = this.lastChildren(buckets);
    let levels = [buckets];
    if(0 && buckets.length == 1) {
      // promote to top level (flatten hierarchy)
      levels = levels.concat(buckets[0]['next']);
      buckets[0]['next'] = [];
    }
    if(remain.length) {
      let nextLevels = this.makeDependsTree(remain, allDepends, nextDepends, bottom, depth+1);
      levels = levels.concat(nextLevels[0]);
      remain = nextLevels[1];
    }
    return [levels, remain];
  }

  lastChildren(buckets) {
    let bottom = [];
    buckets.forEach(bucket => {
      bucket['nodes'].forEach(node => {
        let lvlCount = node['children'].length;
        if(lvlCount) {
          bottom = bottom.concat(this.lastChildren(node['children'][lvlCount - 1]));
        } else {
          bottom.push(node['id']);
        }
      });
    });
    return bottom;
  }

  expandDepends(all_deps) {
    let found = true;
    while(found) {
      found = false;
      for(let dep in all_deps) {
        let deps = all_deps[dep];
        let ndeps = new Set();
        for(let extdep of deps) {
          if(! (extdep in all_deps)) continue;
          let extall = all_deps[extdep];
          for(let extext of extall) {
            if(extext !== dep && extext !== extdep && ! ~deps.indexOf(extext)) {
              ndeps.add(extext);
            }
          }
        }
        if(ndeps.size) {
          all_deps[dep] = deps.concat(Array.from(ndeps));
          found = true;
        }
      }
    }
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
