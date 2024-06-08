import { Component, OnInit, DoCheck } from '@angular/core';
import { Router } from '@angular/router';
import { DatosService } from './servicios/datos.service';
import { AuthService } from './servicios/auth.service';
import { FacebookLoginProvider} from '@abacritt/angularx-social-login';
import { CartInfoService } from './servicios/cart-info.service';
import { environment } from '../environments/environment';

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
  source: string = '';

  googleUser: any;

  public url = environment.apiImageUrl


  constructor(private datosService: DatosService, private router: Router, private authService: AuthService, private cartInfo: CartInfoService) { }

  ngOnInit(){
    if (this.authService.getTokenCookie()){
      this.token = true;
      this.name = this.authService.getNamePicture().name;
      this.picture = this.authService.getNamePicture().picture;
      this.rol = this.authService.getUserRol();
      this.source = this.authService.getSource()
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
      this.source = this.authService.getSource();
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

  products(){
    this.router.navigate(['productos/lista/completa']);
    setTimeout(() => 
      window.location.reload()
    );
  }

  adminPanel(){
    this.router.navigate(['/admin/panel']);
  }

  carritoCompra(){
    this.cartInfo.getCartInfo().subscribe(
      response => {
        this.router.navigate(['/carrito/productos/lista'])

      }, error=>{
        console.log(error);
      }

    )
  }

  actualizarPalabra(){
    this.datosService.setPalabraBuscada(this.palabraBusqueda);
  }

}

