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
  ],
  providers: [ ],
  bootstrap: [AppComponent]
})
export class AppModule { }
