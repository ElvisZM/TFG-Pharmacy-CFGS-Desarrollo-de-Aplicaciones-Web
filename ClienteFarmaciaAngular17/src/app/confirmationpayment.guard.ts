import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { SavepaymentService } from './servicios/savepayment.service';
import { AuthService } from './servicios/auth.service';


export const confirmationpaymentGuard: CanActivateFn = (route, state) => {
  const savePaymentService = inject(SavepaymentService);
  const authService = inject(AuthService);
  const router = inject(Router);

  if (!savePaymentService.getAccessToConfirmationPage() || !authService.getTokenCookie()) {
    router.navigate(['/not-found']);
    return false;
  }
  return true;
};
