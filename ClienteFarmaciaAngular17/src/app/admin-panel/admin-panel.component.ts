import { Component, OnInit } from '@angular/core';
import { CsvproductosService } from '../servicios/csvproductos.service';
import { AuthService } from '../servicios/auth.service';
import { UserslistComponent } from '../userslist/userslist.component';
import { TransactionsComponent } from '../transactions/transactions.component';
import { DashboardComponent } from '../dashboard/dashboard.component';
import { MessagesComponent } from '../messages/messages.component';
import { SettingsComponent } from '../settings/settings.component';
import { TablesComponent } from '../tables/tables.component';
import { DatosService } from '../servicios/datos.service';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-admin-panel',
  standalone: true,
  imports: [DashboardComponent, MessagesComponent, UserslistComponent, TransactionsComponent, SettingsComponent, TablesComponent],
  templateUrl: './admin-panel.component.html',
  styleUrl: './admin-panel.component.scss'
})
export class AdminPanelComponent implements OnInit {

  constructor(private _csvService: CsvproductosService, private authService: AuthService, private datosService: DatosService, private titleService: Title) {}

  ngOnInit(): void {
    const activeTab = localStorage.getItem('activeTab');
    if (activeTab) {
      this.setActiveTab(activeTab);
      setTimeout(() => {
        localStorage.removeItem('activeTab');
      }, 5000);
    }

    const errorTab = localStorage.getItem('errorTab');
    const errorNum = localStorage.getItem('errorProd')
    if (errorTab) {
      this.errorTableTabReload(errorTab, errorNum!);
      setTimeout(() => {
        localStorage.removeItem('errorTab');
        localStorage.removeItem('errorProd');
        this.datosService.errorCreateProductMessage = false;
      }, 5000);
    }
    this.titleService.setTitle('Sitio Administrativo | Panel de Administrador');

  }

  
  setActiveTab(tabId: string) {
    const tabActiva = document.getElementById(tabId)
    const tabDefault = document.getElementById('dashboard')
    const navActiva = document.getElementById(`nav-${tabId}`)
    const navDefault = document.getElementById('nav-dashboard')
    if (tabActiva){
      if (tabId === 'tables'){
        tabDefault!.setAttribute('class', 'tab-pane fade')
        tabActiva.setAttribute('class', 'tab-pane fade active show')
        navDefault!.setAttribute('class', 'nav-link')
        navActiva!.setAttribute('class', 'nav-link active')
        this.datosService.successProductMessage = 'Productos insertados correctamente';
        this.datosService.createProductMessage = true;
        setTimeout(() =>{
          this.datosService.createProductMessage = false;
        }, 5000);
      }else{
        tabDefault!.setAttribute('class', 'tab-pane fade')
        tabActiva.setAttribute('class', 'tab-pane fade active show')
        navDefault!.setAttribute('class', 'nav-link')
        navActiva!.setAttribute('class', 'nav-link active')
      }
      
    }
  };

  errorTableTabReload(tabId: string, errorNum: string){
    const tabActiva = document.getElementById(tabId)
    const tabDefault = document.getElementById('dashboard')
    const navActiva = document.getElementById(`nav-${tabId}`)
    const navDefault = document.getElementById('nav-dashboard')
    tabDefault!.setAttribute('class', 'tab-pane fade')
    tabActiva!.setAttribute('class', 'tab-pane fade active show')
    navDefault!.setAttribute('class', 'nav-link')
    navActiva!.setAttribute('class', 'nav-link active')
    if(errorNum === '1'){
      this.datosService.errorProductMessage = 'CSV Error: Uno o más productos ya existen en esa farmacia o la farmacia no existe.'
      this.datosService.errorCreateProductMessage = true
    }else{
      this.datosService.errorProductMessage = 'File Error: El archivo no es válido'
      this.datosService.errorCreateProductMessage = true
    }
    
  }

}
