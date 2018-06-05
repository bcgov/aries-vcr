import { Component, AfterViewInit, ViewChild } from '@angular/core';
import { SearchInputComponent } from '../search/input.component';

@Component({
  selector: 'app-home',
  templateUrl: '../../themes/_active/home/home.component.html',
  styleUrls: ['../../themes/_active/home/home.component.scss']
})
export class HomeComponent implements AfterViewInit {

  @ViewChild('searchInput') search : SearchInputComponent;
  public inited = true;
  public recordCounts = {orgs: 100, certs: 900};
  public searching = false;

  updateQuery(value: string) {
    console.log('got query:', value);
  }

  ngAfterViewInit() {
    this.search.focus();
  }

}
