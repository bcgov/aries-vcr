import { Injectable } from '@angular/core';
import { RowSpec, MarkerSpec } from 'app/timeline/models/i-timeline';
import { parseDate } from 'app/timeline/models/timeline-utils';

@Injectable({
  providedIn: 'root'
})
export class TimelineService {

  genShortDateMarkers(rows: RowSpec[]): MarkerSpec[] {
    const markers = []
    for (const row of rows) {
      row.slots.forEach((itm) => {
        if (itm.end == null) return;
        const diff = parseDate(itm.end).getTime() - parseDate(itm.start).getTime()
        const monthCount = diff / 2592000000;
        if (monthCount > 1 && monthCount < 12) {

          markers.push({
            date: parseDate(itm.start),
            label: this.genLabel(itm.htmlContent.toString()),
            link: itm.url,
        })
      }
    })
    return markers;
    }
  }

  genLabel(html: string) {
    let label = html.slice(html.indexOf('>') + 1, html.indexOf('</strong>'));
    if (label.length > 20) label = label.slice(0, 20) + '...'
    return label
  }

  constructor() { }
}
