import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { CartInfoService } from './servicios/cart-info.service';
import { AuthService } from './servicios/auth.service';
import { catchError, map, of } from 'rxjs';

export const paymentGuard: CanActivateFn = (route, state) => {
  const cartInfo = inject(CartInfoService);
  const router = inject(Router);
  const authService = inject(AuthService);


  if (!authService.getTokenCookie()) {
    router.navigate(['not-found'])
    return false;
  }

  return cartInfo.getCartInfo().pipe(
    map(response => {
      if (response.total_carrito === 0) {
        console.log(response.total_carrito);
        router.navigate(['/not-found']);
        return false;
      }
      console.log("hola");
      console.log(response.total_carrito);
      return true;
    }),
    catchError(err => {
      console.error(err);
      router.navigate(['/not-found']);
      return of(false);
    })
  );
  
};
