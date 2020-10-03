import { inject, InjectionToken } from '@angular/core';

import { environment } from '../../../environments/environment';
import { AppConfigService } from '../../app-config.service';

export const API_URL = new InjectionToken<string>('API URL for Verifiable Credential Registry', {
  providedIn: 'root',
  factory: () => {
    const apiService = new ApiService(inject(AppConfigService));
    return apiService.baseUrl;
  }
});

export class ApiService {

  constructor(private appConfigService: AppConfigService) { }

  private get _config(): any {
    return this.appConfigService.getConfig();
  }

  public get baseUrl(): string {
    return this._config.API_URL || environment.API_URL;
  }
}
