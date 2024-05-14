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
  ],
  providers: [ CsvproductosService],
  bootstrap: [AppComponent]
})
export class AppModule { }
