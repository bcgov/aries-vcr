import { Component, ElementRef, OnDestroy, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { BreadcrumbComponent } from './breadcrumb/breadcrumb.component';
import { LangChangeEvent, TranslateService } from '@ngx-translate/core';
import { Subscription } from 'rxjs/Subscription';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {
  onLangChange: Subscription;
  currentLang = 'en';
  supportedLanguages = ['en', 'fr'];
  private titleLabel = 'app.title';
  private onFetchTitle: Subscription;

  constructor(
    public el: ElementRef,
    public translate: TranslateService,
    private route:ActivatedRoute,
    private titleService: Title) {}

  ngOnInit() {
    /*
     * Fallback language for when a translation isn't found in the current language
     */
    this.translate.setDefaultLang(this.supportedLanguages[0]);

     /*
      * The primary language to use. If not yet available, it will use the
      * current loader to fetch it.
      */
    this.translate.use(this.guessLanguage());

    this.onLangChange = this.translate.onLangChange.subscribe((event: LangChangeEvent) => {
      this.onUpdateLanguage(event.lang);
    });
  }

  ngOnDestroy() {
    if (this.onLangChange !== undefined) {
      this.onLangChange.unsubscribe();
    }
  }

  onUpdateLanguage(lang): void {
    console.log('Language:', lang);
    this.currentLang = this.translate.currentLang;
    // set the lang attribute on the html element
    this.el.nativeElement.parentElement.parentElement.setAttribute('lang', lang);
    this.setTitleLabel(this.titleLabel);
  }

  /**
   * Returns the current lang for the application
   * using the existing base path
   * or the browser lang if there is no base path
   * @returns {string}
   */
  public guessLanguage(): string | null {
    let ret = this.supportedLanguages[0];
    if(typeof window !== 'undefined' && typeof window.navigator !== 'undefined') {
      let lang = (window.navigator['languages'] ? window.navigator['languages'][0] : null)
        || window.navigator.language
        || window.navigator['browserLanguage']
        || window.navigator['userLanguage']
        || '';
      if(lang.indexOf('-') !== -1) {
        lang = lang.split('-')[0];
      }
      if(lang.indexOf('_') !== -1) {
        lang = lang.split('_')[0];
      }
      lang = lang.toLowerCase();
      if(this.supportedLanguages.indexOf(lang) >= 0) {
        ret = lang;
      }
    }
    return ret;
  }

  public setTitleLabel(newLabel: string) {
    if (this.onFetchTitle !== undefined) {
      this.onFetchTitle.unsubscribe();
    }
    this.titleLabel = newLabel;
    this.onFetchTitle = this.translate.get(newLabel).subscribe((res: string) => {
      this.setTitle(res);
    });
  }

  public setTitle(newTitle: string) {
    this.titleService.setTitle(newTitle);
  }
}

