import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginRegisterComponent } from './login-register/login-register.component';
import { NosotrosComponent } from './nosotros/nosotros.component';
import { PoliticacookiesComponent } from './politicacookies/politicacookies.component';
import { AdminPanelComponent } from './admin-panel/admin-panel.component';

import { NotfoundpageComponent } from './notfoundpage/notfoundpage.component';
import { FormproductComponent } from './formproduct/formproduct.component';
import { FormproductupdateComponent } from './formproductupdate/formproductupdate.component';
import { BuscadorSimpleComponent } from './buscador-simple/buscador-simple.component';
import { AllproductsComponent } from './allproducts/allproducts.component';
import { ShoppingCartComponent } from './shopping-cart/shopping-cart.component';
import { PaymentComponent } from './payment/payment.component';
import { ConfirmationPaymentComponent } from './confirmation-payment/confirmation-payment.component';
import { ProductDetailsComponent } from './product-details/product-details.component';


const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login-register', component: LoginRegisterComponent },
  { path: 'nosotros', component: NosotrosComponent },
  { path: 'politica/cookies', component: PoliticacookiesComponent },
  { path: 'admin/panel', component: AdminPanelComponent},
  { path: 'admin/panel/create/product', component: FormproductComponent},
  { path: 'admin/panel/update/product/:cn_prod/:cif_farm', component: FormproductupdateComponent},
  { path: 'productos/buscador/query/:palabra', component: BuscadorSimpleComponent},
  { path: 'productos/lista/completa', component: AllproductsComponent},
  { path: 'carrito/productos/lista', component: ShoppingCartComponent},
  { path: 'tipo/pago', component: PaymentComponent},
  { path: 'confirmacion/pago', component: ConfirmationPaymentComponent },
  { path: 'detalles/producto/:cn_prod/:cif_farm', component: ProductDetailsComponent},

  { path: '**', component: NotfoundpageComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
