import { Component, OnInit, DoCheck } from '@angular/core';
import { Router } from '@angular/router';
import { DatosService } from './servicios/datos.service';
import { AuthService } from './servicios/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, DoCheck {
  palabraBusqueda: string = '';
  token: boolean = false; 

  googleUser: any;

  constructor(private datosService: DatosService, private router: Router, private authService: AuthService, ) { }

  ngOnInit(){
    if (this.authService.getTokenCookie()){
      this.token = true;
    }else{
      this.token = false;
    }

    this.googleUserInfo();
    // console.log(this.googleUser)
    // console.log(this.googleUser.email)

  }

  ngDoCheck(){
    if (this.authService.getTokenCookie()){
      this.token = true;
    }else{
      this.token = false;
    }
  }

  buscar(){
    this.datosService.setPalabraBuscada(this.palabraBusqueda);
    this.router.navigate(['/buscador/query', this.palabraBusqueda]);
  }

  logoutAccount(){
    this.authService.logout();
    this.token = false;
  }

  googleUserInfo(){
    if (this.authService.getGoogleUserCookie()){
      this.googleUser= JSON.parse(this.authService.getGoogleUserCookie());
    }
  }

}

