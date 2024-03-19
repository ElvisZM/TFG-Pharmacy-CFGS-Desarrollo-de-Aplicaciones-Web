import { TestBed } from '@angular/core/testing';

import { RegistroLogService } from './registro-log.service';

describe('RegistroLogService', () => {
  let service: RegistroLogService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RegistroLogService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
