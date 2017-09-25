import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, NavigationEnd } from '@angular/router';
import 'rxjs/add/operator/filter';

@Component({
  selector: 'breadcrumb',
  templateUrl: './breadcrumb.component.html',
  styleUrls: ['./breadcrumb.component.scss']
})
export class BreadcrumbComponent implements OnInit {
  public breadcrumbs: Array<{}> = [];

  constructor (
    private router:Router,
    private route:ActivatedRoute
  ) { }

  ngOnInit() {
    const ROUTE_DATA_BREADCRUMB: string = 'breadcrumb';
    const PRIMARY_OUTLET: string = 'primary';

    this.router.events
      .filter( event => event instanceof NavigationEnd)
      .subscribe( event => {

        //reset breadcrumbs
        this.breadcrumbs = [];

        let currentRoute = this.route.root;
        let childrenRoutes = currentRoute.children;
        currentRoute = null;

        childrenRoutes.forEach( route => {

          // Verify this is the primary route
          if (route.outlet !== PRIMARY_OUTLET) {
            return;
          }

          // Verify the custom data property "breadcrumb" is specified on the route
          if (!route.snapshot.data.hasOwnProperty(ROUTE_DATA_BREADCRUMB)) {
            return;
          }

          //get the route's URL segment
          let routeURL: string = route.snapshot.url
              .map(segment => segment.path)
              .join('/');

          console.log('Url segment', routeURL);

          //add breadcrumb
          this.breadcrumbs.push({
            label: route.snapshot.data[ROUTE_DATA_BREADCRUMB],
            url: routeURL
          });
        });
    })
  }

}
