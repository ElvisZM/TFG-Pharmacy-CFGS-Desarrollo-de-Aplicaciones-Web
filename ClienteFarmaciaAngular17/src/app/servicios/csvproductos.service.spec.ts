import { TestBed } from '@angular/core/testing';

import { CsvproductosService } from './csvproductos.service';

describe('CsvproductosService', () => {
  let service: CsvproductosService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CsvproductosService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
