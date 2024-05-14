import { Component, OnInit, DoCheck } from '@angular/core';
import { Router } from '@angular/router';
import { DatosService } from './servicios/datos.service';
import { AuthService } from './servicios/auth.service';
import { FacebookLoginProvider} from '@abacritt/angularx-social-login';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, DoCheck {
  palabraBusqueda: string = '';
  token: boolean = false; 
  name: string = '';
  picture: string = '';
  rol: string = '';

  googleUser: any;


  constructor(private datosService: DatosService, private router: Router, private authService: AuthService) { }

  ngOnInit(){
    if (this.authService.getTokenCookie()){
      this.token = true;
      this.name = this.authService.getNamePicture().name;
      this.picture = this.authService.getNamePicture().picture;
      this.rol = this.authService.getUserRol();
    }else{
      this.token = false;
    }


  }

  ngDoCheck(){
    if (this.authService.getTokenCookie()){
      this.token = true;
      this.name = this.authService.getNamePicture().name;
      this.picture = this.authService.getNamePicture().picture;
      this.rol = this.authService.getUserRol();
    }else{
      this.token = false;
    }
  }

  buscar(){
    this.datosService.setPalabraBuscada(this.palabraBusqueda);
    this.router.navigate(['/productos/buscador/query', this.palabraBusqueda]);
  }

  logoutAccount(){
    this.authService.logout();
    this.token = false; 
  }

  adminPanel(){
    this.router.navigate(['/admin/panel']);
  }


}

