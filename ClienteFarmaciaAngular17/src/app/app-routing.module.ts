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


import { CatAnalgesicosComponent } from './cat-analgesicos/cat-analgesicos.component';
import { CatAntiacidosComponent } from './cat-antiacidos/cat-antiacidos.component';
import { CatAntialergicosComponent } from './cat-antialergicos/cat-antialergicos.component';
import { CatAntisepticosComponent } from './cat-antisepticos/cat-antisepticos.component';
import { CatBroncodilatadoresComponent } from './cat-broncodilatadores/cat-broncodilatadores.component';
import { CatCorticosteroidesComponent } from './cat-corticosteroides/cat-corticosteroides.component';
import { CatHipolipemiantesComponent } from './cat-hipolipemiantes/cat-hipolipemiantes.component';
import { CatSuplementosComponent } from './cat-suplementos/cat-suplementos.component';

import { authGuard } from './auth.guard';
import { adminGuard } from './admin.guard';
import { confirmationpaymentGuard } from './confirmationpayment.guard';
import { paymentGuard } from './payment.guard';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login-register', component: LoginRegisterComponent },
  { path: 'nosotros', component: NosotrosComponent },
  { path: 'politica/cookies', component: PoliticacookiesComponent },
  { path: 'admin/panel', component: AdminPanelComponent, canActivate: [adminGuard]},
  { path: 'admin/panel/create/product', component: FormproductComponent},
  { path: 'admin/panel/update/product/:cn_prod/:cif_farm', component: FormproductupdateComponent},
  { path: 'productos/buscador/query/:palabra', component: BuscadorSimpleComponent},
  { path: 'productos/lista/completa', component: AllproductsComponent},
  { path: 'carrito/productos/lista', component: ShoppingCartComponent, canActivate: [authGuard]},
  { path: 'tipo/pago', component: PaymentComponent, canActivate: [paymentGuard]},
  { path: 'confirmacion/pago', component: ConfirmationPaymentComponent, canActivate: [confirmationpaymentGuard] },
  { path: 'detalles/producto/:cn_prod/:cif_farm', component: ProductDetailsComponent},
  { path: 'categoria/analgesicos', component: CatAnalgesicosComponent},
  { path: 'categoria/antiacidos', component: CatAntiacidosComponent},
  { path: 'categoria/antialergicos', component: CatAntialergicosComponent},
  { path: 'categoria/antisepticos', component: CatAntisepticosComponent},
  { path: 'categoria/broncodilatadores', component: CatBroncodilatadoresComponent},
  { path: 'categoria/corticosteroides', component: CatCorticosteroidesComponent},
  { path: 'categoria/hipolipemiantes', component: CatHipolipemiantesComponent},
  { path: 'categoria/suplementos', component: CatSuplementosComponent},


  { path: '**', component: NotfoundpageComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
