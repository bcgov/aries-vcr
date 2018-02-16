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
  currentLang : string;
  inited = false;
  // to be moved into external JSON loaded by localize-router
  supportedLanguages = [
    {
      name: 'en',
      label: 'English'
    },
    {
      name: 'fr',
      label: 'Français'
    }
  ];
  altLang : string;
  altLangLabel : string;
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
    if(lang && lang !== this.currentLang) {
      console.log('Language:', lang);
      this.currentLang = lang;
      // need to add some functionality to localize-router to handle this properly
      let alt = this.altLanguageInfo();
      this.altLang = alt ? alt.name : 'en';
      this.altLangLabel = alt ? alt.label : '';
      // set the lang attribute on the html element
      this.el.nativeElement.parentElement.parentElement.setAttribute('lang', lang);
      this.setTitleLabel(this.titleLabel);
      this.checkInit();
    }
  }

  checkInit() {
    if(this.currentLang) {
      this.inited = true;
    }
  }

  altLanguageInfo() {
    for(let lang of this.supportedLanguages) {
      if(lang.name !== this.currentLang)
        return lang;
    }
  }

  public changeLanguage(lang: string) {
    this.localize.changeLanguage(lang);
  }

  public switchLanguage(evt) {
    if(this.altLang) {
      this.localize.changeLanguage(this.altLang);
    }
    if(evt) {
      evt.preventDefault();
    }
  }

  /**
   * Returns the current lang for the application
   * using the existing base path
   * or the browser lang if there is no base path
   * @returns {string}
   */
  public guessLanguage(): string | null {
    let ret = this.supportedLanguages[0]['name'];
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
      for(let check of this.supportedLanguages) {
        if(check.name === lang) {
          ret = lang;
          break;
        }
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

