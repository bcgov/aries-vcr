import { Component, ElementRef, OnDestroy, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { LocalizeRouterService } from 'localize-router';
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
  inited = false;
  supportedLanguages = ['en', 'fr'];
  private titleLabel = 'app.title';
  private onFetchTitle: Subscription;

  constructor(
    public el: ElementRef,
    public translate: TranslateService,
    private localize: LocalizeRouterService,
    private route: ActivatedRoute,
    private titleService: Title) {}

  ngOnInit() {
    // Initialize fallback and initial language
    // NOTE - currently superceded by localize-router
    // this.translate.setDefaultLang(this.supportedLanguages[0]);
    // this.translate.use(this.guessLanguage());

    this.onLangChange = this.translate.onLangChange.subscribe((event: LangChangeEvent) => {
      this.onUpdateLanguage(event.lang);
    });
    if(this.translate.currentLang) {
      // may already be initialized by localize-router
      this.onUpdateLanguage(this.translate.currentLang);
    }
  }

  ngOnDestroy() {
    if (this.onLangChange !== undefined) {
      this.onLangChange.unsubscribe();
    }
    if (this.onFetchTitle !== undefined) {
      this.onFetchTitle.unsubscribe();
    }
  }

  onUpdateLanguage(lang) {
    console.log('Language:', lang);
    this.currentLang = this.translate.currentLang;
    // set the lang attribute on the html element
    this.el.nativeElement.parentElement.parentElement.setAttribute('lang', lang);
    this.setTitleLabel(this.titleLabel);
    this.checkInit();
  }

  checkInit() {
    if(this.currentLang) {
      this.inited = true;
    }
  }

  public changeLanguage(lang: string) {
    this.localize.changeLanguage(lang);
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
    this.onFetchTitle = this.translate.stream(newLabel).subscribe((res: string) => {
      this.setTitle(res);
    });
  }

  public setTitle(newTitle: string) {
    this.titleService.setTitle(newTitle);
  }
}

