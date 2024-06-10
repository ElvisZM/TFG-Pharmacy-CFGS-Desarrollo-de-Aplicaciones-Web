import { TestBed } from '@angular/core/testing';
import { CanActivateFn } from '@angular/router';

import { confirmationpaymentGuard } from './confirmationpayment.guard';

describe('confirmationpaymentGuard', () => {
  const executeGuard: CanActivateFn = (...guardParameters) => 
      TestBed.runInInjectionContext(() => confirmationpaymentGuard(...guardParameters));

  beforeEach(() => {
    TestBed.configureTestingModule({});
  });

  it('should be created', () => {
    expect(executeGuard).toBeTruthy();
  });
});
