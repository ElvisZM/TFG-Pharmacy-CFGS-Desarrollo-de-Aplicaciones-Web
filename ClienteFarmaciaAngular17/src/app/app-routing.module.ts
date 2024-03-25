import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginRegisterComponent } from './login-register/login-register.component';
import { NosotrosComponent } from './nosotros/nosotros.component';
import { PoliticacookiesComponent } from './politicacookies/politicacookies.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login-register', component: LoginRegisterComponent },
  { path: 'nosotros', component: NosotrosComponent },
  { path: 'politica/cookies', component: PoliticacookiesComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
