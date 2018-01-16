import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router} from '@angular/router';
import { GeneralDataService } from 'app/general-data.service';
import { Location, LocationType, VerifiableOrg, VerifiableOrgType, IssuerService, VerifiableClaim, VerifiableClaimType, DoingBusinessAs,
  blankLocation, blankOrgType, blankLocationType, blankIssuerService, blankClaimType } from '../data-types';

@Component({
  selector: 'app-roadmap',
  templateUrl: './roadmap.component.html',
  styleUrls: ['../dashboard/dashboard.component.scss', './roadmap.component.scss']
})
export class RoadmapComponent implements OnInit {

  public recordId : string = '';
  public query : string = '';
  public error : string = '';
  public orgRecord;
  public allResults;
  public results = [];
  public searchType = 'name';
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

  public claimTypes = [
    {
      title: 'Registration',
      issuerTLA: 'BCReg',
      altText: 'Certificate not found',
      linkText: 'View registration record',
      regLink: 'https://bc-registries-devex-von-permitify-dev.pathfinder.gov.bc.ca/',
      regText: 'Enroll with BC Registries',
      cert: null
    },
    {
      title: 'Restaurant Clearance Letter',
      issuerTLA: 'WorkSafe',
      altText: 'Certificate not found',
      linkText: 'View registration record',
      regLink: 'https://worksafe-bc-devex-von-permitify-dev.pathfinder.gov.bc.ca/',
      regText: 'Register with WorkSafe BC',
      cert: null
    },
    {
      title: 'PST Number',
      issuerTLA: 'Ministry of Finance',
      altText: 'Certificate not found',
      linkText: 'View registration record',
      regLink: 'https://ministry-of-finance-devex-von-permitify-dev.pathfinder.gov.bc.ca/',
      regText: 'Register with the BC Ministry of Finance',
      cert: null
    },
    {
      title: 'Operating Permit',
      issuerTLA: 'Health Authority',
      altText: 'Certificate not found',
      linkText: 'View registration record',
      regLink: 'https://fraser-valley-health-authority-devex-von-permitify-dev.pathfinder.gov.bc.ca/',
      regText: 'Register with the Fraser Valley Health Authority',
      cert: null
    },
    {
      title: 'Business License',
      issuerTLA: 'Surrey',
      altText: 'Certificate not found',
      linkText: 'View registration record',
      regLink: 'https://city-of-surrey-devex-von-permitify-dev.pathfinder.gov.bc.ca/',
      regText: 'Register with the City of Surrey',
      cert: null
    },
    {
      title: 'Liquor License',
      issuerTLA: 'Liquor Licensing',
      altText: 'Certificate not found',
      linkText: 'View registration record',
      regLink: 'https://liquor-control-and-licensing-branch-devex-von-permitify-dev.pathfinder.gov.bc.ca/',
      regText: 'Register with the BC Liquor Control and Licensing Branch',
      cert: null
    }
  ];

  constructor(
    private dataService: GeneralDataService,
    private $route: ActivatedRoute,
    private $router: Router
  ) { }

  ngOnInit() {
    this.preload = this.dataService.preloadData(['locations', 'locationtypes', 'verifiableorgtypes']);
    this.$route.queryParams.subscribe(params => {
      this.setParams(params.record, params.query);
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
        for(let i = 0; i < this.claimTypes.length; i++) {
          certPos[this.claimTypes[i].issuerTLA] = i;
          this.claimTypes[i].cert = null;
        }
        for(let i = 0; i < this.certs.length; i++) {
          let cert = <VerifiableClaim>this.certs[i].top;
          let tla = cert.issuer && cert.issuer.issuerOrgTLA;
          if(tla in certPos) {
            this.claimTypes[certPos[tla]].cert = cert;
          }
        }

        /*this.dataService.loadFromApi('verifiableorgs/' + this.id + '/voclaims')
          .subscribe((res: any) => {
            let certs = [];
            let seen = {};
            for(var i = 0; i < res.length; i++) {
              let cert = res[i];
              if(! seen[cert.voClaimType]) {
                cert.type = this.dataService.findOrgData('verifiableclaimtypes', cert.voClaimType);
                cert.color = ['green', 'orange', 'blue', 'purple'][cert.voClaimType % 4];
                certs.push(cert);
                seen[cert.voClaimType] = 1;
              }
            }
            this.certs = certs;
            console.log('claims', res);
          });*/
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
