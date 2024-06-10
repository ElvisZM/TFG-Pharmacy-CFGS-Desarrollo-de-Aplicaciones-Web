import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms'; 
  

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { FooterComponent } from './footer/footer.component';
import { TopVentasComponent } from './top-ventas/top-ventas.component';
import { LoginRegisterComponent } from './login-register/login-register.component';
import { NosotrosComponent } from './nosotros/nosotros.component';
import { PoliticacookiesComponent } from './politicacookies/politicacookies.component';
import { CsvproductosService } from './servicios/csvproductos.service';
import { DashboardComponent } from './dashboard/dashboard.component';
import { MessagesComponent } from './messages/messages.component';
import { UserslistComponent } from './userslist/userslist.component';
import { TransactionsComponent } from './transactions/transactions.component';
import { SettingsComponent } from './settings/settings.component';
import { TablesComponent } from './tables/tables.component';
import { FacebookLoginProvider, SocialAuthServiceConfig, SocialLoginModule } from '@abacritt/angularx-social-login';
import { BuscadorSimpleComponent } from './buscador-simple/buscador-simple.component';
import { ShoppingCartComponent } from './shopping-cart/shopping-cart.component';
import { PaymentComponent } from './payment/payment.component';
import { ConfirmationPaymentComponent } from './confirmation-payment/confirmation-payment.component';
import { DatePipe } from '@angular/common';
import { ProductDetailsComponent } from './product-details/product-details.component';

import { CatAnalgesicosComponent } from './cat-analgesicos/cat-analgesicos.component';
import { CatAntiacidosComponent } from './cat-antiacidos/cat-antiacidos.component';
import { CatAntialergicosComponent } from './cat-antialergicos/cat-antialergicos.component';
import { CatAntisepticosComponent } from './cat-antisepticos/cat-antisepticos.component';
import { CatBroncodilatadoresComponent } from './cat-broncodilatadores/cat-broncodilatadores.component';
import { CatCorticosteroidesComponent } from './cat-corticosteroides/cat-corticosteroides.component';
import { CatHipolipemiantesComponent } from './cat-hipolipemiantes/cat-hipolipemiantes.component';
import { CatSuplementosComponent } from './cat-suplementos/cat-suplementos.component';

@NgModule({
  declarations: [
    AppComponent,
    
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HomeComponent,
    FooterComponent,
    TopVentasComponent,
    LoginRegisterComponent,
    NosotrosComponent,
    PoliticacookiesComponent,
    DashboardComponent,
    MessagesComponent,
    UserslistComponent,
    TransactionsComponent,
    SettingsComponent,
    TablesComponent,
    SocialLoginModule,
    BuscadorSimpleComponent,
    ShoppingCartComponent,
    PaymentComponent,
    ConfirmationPaymentComponent,
    ProductDetailsComponent,
    CatAnalgesicosComponent,
    CatAntiacidosComponent,
    CatAntialergicosComponent,
    CatAntisepticosComponent,
    CatBroncodilatadoresComponent,
    CatCorticosteroidesComponent,
    CatHipolipemiantesComponent,
    CatSuplementosComponent
  ],
  providers: [ CsvproductosService, DatePipe],
  bootstrap: [AppComponent]
})
export class AppModule { }
