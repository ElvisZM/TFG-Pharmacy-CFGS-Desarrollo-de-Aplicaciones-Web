import { TestBed } from '@angular/core/testing';

import { CartInfoService } from './cart-info.service';

describe('CartInfoService', () => {
  let service: CartInfoService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CartInfoService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
