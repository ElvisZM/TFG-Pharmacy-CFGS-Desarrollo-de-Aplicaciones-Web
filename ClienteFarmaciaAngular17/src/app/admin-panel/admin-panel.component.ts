import { Component } from '@angular/core';
import { CsvproductosService } from '../servicios/csvproductos.service';
import { AuthService } from '../servicios/auth.service';
import { UserslistComponent } from '../userslist/userslist.component';
import { TransactionsComponent } from '../transactions/transactions.component';
import { DashboardComponent } from '../dashboard/dashboard.component';
import { MessagesComponent } from '../messages/messages.component';
import { SettingsComponent } from '../settings/settings.component';
import { TablesComponent } from '../tables/tables.component';

@Component({
  selector: 'app-admin-panel',
  standalone: true,
  imports: [DashboardComponent, MessagesComponent, UserslistComponent, TransactionsComponent, SettingsComponent, TablesComponent],
  templateUrl: './admin-panel.component.html',
  styleUrl: './admin-panel.component.scss'
})
export class AdminPanelComponent {

  constructor(private _csvService: CsvproductosService, private authService: AuthService) {}



  

}
