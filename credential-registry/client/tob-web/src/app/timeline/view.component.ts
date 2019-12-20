import { Component, Input, AfterViewInit, OnDestroy, NgZone, ElementRef, Renderer2, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { Timeline } from './models/timeline';
import { RowSpec, MarkerSpec } from './models/i-timeline';
import { timelineScale } from './models/scale.model';
import { parseDate } from './models//timeline-utils';
import { TimelineService } from './services/timeline.service';

@Component({
  selector: 'timeline-view',
  template: `
    <div #outer></div>
  `,
  styleUrls: ['../../themes/_active/timeline/timeline.scss'],
  /*host: {
    '(window:resize)': 'onResize($event)',
  },*/
})
export class TimelineViewComponent implements AfterViewInit, OnDestroy {
  @ViewChild('outer') private _outer: ElementRef;

  @Input() set range(rng: { start: string | Date; end: string | Date }) {
    if (rng.start && rng.end) {
      // expand range
      const start = Timeline.parseDate(rng.start);
      const end = Timeline.parseDate(rng.end);
      const diff = end.getTime() - start.getTime();
      const offs = diff * 0.1;
      start.setTime(start.getTime() - offs);
      end.setTime(end.getTime() + offs);
      rng.start = start.toISOString();
      rng.end = end.toISOString();
    }
    this._range = rng;
    if (this._timeline) this._timeline.setRange(this.rangeStart, this.rangeEnd);
  }

  private _timeline: Timeline.TimelineView;
  private _range: { start: string | Date; end: string | Date };
  private _resizeHook: null;
  private _rows: RowSpec[] = [];

  constructor(
    // private _cd: ChangeDetectorRef,
    private _renderer: Renderer2,
    private _router: Router,
    private _zone: NgZone,
    private timelineSvc: TimelineService,
  ) {}

  ngAfterViewInit() {
    this._timeline = new Timeline.TimelineView(this._outer.nativeElement, null, this._renderer);
    this._timeline.setRange(this.rangeStart, this.rangeEnd);
    /*
    this.rows[0].slots.push(
      {
        groups: ['all'],
        htmlContent: '<strong>This is a really long slot</strong>,<br>testing',
        start: parseDate('1953-06-01T00:00:00Z'),
        end: parseDate('2019-05-01T00:00:00Z'),
        classNames: ['slot-primary'],
        url: 'http://localhost:4300/en/organization/1a16336c-d880-4568-8e3b-306a263d83a4/cred/1',
      },
      {
        groups: ['all'],
        htmlContent: '<strong>This is a really short slot</strong>,<br>testing',
        start: parseDate('2019-05-31T00:00:00Z'),
        end: parseDate('2019-08-31T00:00:00Z'),
        classNames: ['slot-secondary'],
        url: 'http://localhost:4300/en/organization/1a16336c-d880-4568-8e3b-306a263d83a4/cred/1',
      },
    );
    */
    this._timeline.setRows(this.rows);
    const markers = [{ date: new Date(), label: 'Today' }] as MarkerSpec[];
    const scale = timelineScale(parseDate(this.rangeStart), parseDate(this.rangeEnd));
    markers.push(...this.timelineSvc.genShortDateMarkers(this.rows));
    this._timeline.setMarkers(markers);

    this._renderer.listen(this._timeline.container, 'slotclick', this.click.bind(this));
    this._zone.runOutsideAngular(() => {
      this._timeline.render();
      this._resizeHook = this.onResize.bind(this);
      window.addEventListener('resize', this._resizeHook, { passive: true });
    });
  }

  ngOnDestroy() {
    this._zone.runOutsideAngular(() => {
      if (this._resizeHook) {
        window.removeEventListener('resize', this._resizeHook);
      }
    });
  }

  click(evt) {
    this._router.navigate([evt.detail.spec.url]);
  }

  get rangeStart() {
    if (!this._range || !this._range.start) {
      const d = new Date();
      d.setFullYear(d.getFullYear() - 1);
      return d.toISOString();
    }
    return this._range.start;
  }

  get rangeEnd() {
    if (!this._range || !this._range.end) {
      const d = new Date();
      d.setFullYear(d.getFullYear() + 1);
      return d.toISOString();
    }
    return this._range.end;
  }

  get range() {
    return { start: this.rangeStart, end: this.rangeEnd };
  }

  get rows() {
    return this._rows;
  }

  @Input() set rows(vals: RowSpec[]) {
    this._rows = vals;
    if (this._timeline) this._timeline.setRows(this.rows);
  }

  onResize(evt?) {
    return this._timeline ? this._timeline.update() : null;
  }

  get testdata(): RowSpec[] {
    const rows = [];
    rows.push({
      id: 'set-1',
      slots: [
        {
          id: 'slot-1a',
          groups: ['all'],
          htmlContent: '<strong>Testing</strong>,<br>testing',
          start: '2018-06-01T00:00:00Z',
          end: '2020-05-31T00:00:00Z',
          classNames: ['slot-primary'],
        },
        {
          id: 'slot-1b',
          groups: ['all'],
          htmlContent: '<strong>Testing</strong>,<br>testing',
          start: '2020-05-31T00:00:00Z',
          end: '2021-05-31T00:00:00Z',
          classNames: ['slot-secondary'],
        },
      ],
    });
    rows.push({
      id: 'set-2',
      slots: [
        {
          id: 'slot-2',
          groups: ['all'],
          htmlContent: 'Hello there',
          start: '2020-03-15T00:00:00Z',
          end: '2030-05-31T00:00:00Z',
          classNames: ['slot-primary'],
        },
      ],
    });
    return rows;
  }
}
