import { Component, OnInit, OnDestroy } from '@angular/core';
import { GeneralDataService } from 'app/general-data.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-business',
  templateUrl: './business.component.html',
  styleUrls: ['./business.component.scss']
})
export class BusinessComponent implements OnInit, OnDestroy {
  id: number;
  loaded: boolean;
  record: any;
  error: string;
  sub: any;

  constructor(
    private dataService: GeneralDataService,
    private route: ActivatedRoute) { }

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
       this.id = +params['recordId'];
        this.dataService.loadVerifiedOrg(this.id).subscribe(record => {
          this.record = record;
          console.log('verified org:', record);
          this.loaded = !!record;
          if(! record) this.error = 'Record not found';
          else {
            this.dataService.loadRecord('voorgtypes', record.orgTypeId)
              .subscribe((res: any) => {
                this.record.typeName = res.theType;
                console.log(res);
              });
          }
        }, err => {
          this.error = err;
        });
    });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }
}
