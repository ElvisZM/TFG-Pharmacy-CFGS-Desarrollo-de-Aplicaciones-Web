import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginRegisterComponent } from './login-register/login-register.component';
import { NosotrosComponent } from './nosotros/nosotros.component';
import { PoliticacookiesComponent } from './politicacookies/politicacookies.component';
import { AdminPanelComponent } from './admin-panel/admin-panel.component';
import { UserslistComponent } from './userslist/userslist.component';
import { TransactionsComponent } from './transactions/transactions.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { MessagesComponent } from './messages/messages.component';
import { SettingsComponent } from './settings/settings.component';
import { TablesComponent } from './tables/tables.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login-register', component: LoginRegisterComponent },
  { path: 'nosotros', component: NosotrosComponent },
  { path: 'politica/cookies', component: PoliticacookiesComponent },
  { path: 'admin/panel', component: AdminPanelComponent},
  { path: 'admin/panel/dashboard', component: DashboardComponent },
  { path: 'admin/panel/messages', component: MessagesComponent},
  { path: 'admin/panel/users/list', component: UserslistComponent},
  { path: 'admin/panel/transactions', component: TransactionsComponent},
  { path: 'admin/panel/settings', component: SettingsComponent},
  { path: 'admin/panel/tables', component: TablesComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
