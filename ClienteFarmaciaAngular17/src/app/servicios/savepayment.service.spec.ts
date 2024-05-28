import { TestBed } from '@angular/core/testing';

import { SavepaymentService } from './savepayment.service';

describe('SavepaymentService', () => {
  let service: SavepaymentService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SavepaymentService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
