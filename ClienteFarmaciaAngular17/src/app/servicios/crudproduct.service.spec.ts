import { TestBed } from '@angular/core/testing';

import { CrudproductService } from './crudproduct.service';

describe('CrudproductService', () => {
  let service: CrudproductService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CrudproductService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
