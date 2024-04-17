import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DatosService } from './servicios/datos.service';
import { AuthService } from './servicios/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  palabraBusqueda: string = '';
  token = this.authService.getTokenCookie()

  constructor(private datosService: DatosService, private router: Router, private authService: AuthService) { }

  buscar(){
    this.datosService.setPalabraBuscada(this.palabraBusqueda);
    this.router.navigate(['/buscador/query', this.palabraBusqueda]);
  }

  logoutAccount(){
    this.authService.logout();
  }

}

