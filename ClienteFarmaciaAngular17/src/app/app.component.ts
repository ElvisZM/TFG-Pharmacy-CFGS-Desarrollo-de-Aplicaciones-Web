import { Component, OnInit, DoCheck, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { DatosService } from './servicios/datos.service';
import { AuthService } from './servicios/auth.service';
import { FacebookLoginProvider} from '@abacritt/angularx-social-login';
import { CartInfoService } from './servicios/cart-info.service';
import { environment } from '../environments/environment';
import { BotService } from './servicios/bot.service';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, DoCheck, OnDestroy {
  palabraBusqueda: string = '';
  token: boolean = false; 
  name: string = '';
  picture: string = '';
  rol: string = '';
  source: string = '';

  googleUser: any;

  public url = environment.apiImageUrl

  showChatbot!: boolean;
  userMessage = '';
  messages = [
    { text: 'Hola, ¿cómo puedo ayudarte?', sender: 'bot' }
  ];

  chatEnded: boolean = false;
  constructor(private datosService: DatosService, private router: Router, private authService: AuthService, private cartInfo: CartInfoService, private botService: BotService) { }

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

  ngOnDestroy(): void {
      this.endChat()
  }

  buscar(){
    this.datosService.setPalabraBuscada(this.palabraBusqueda);
    this.router.navigate(['/productos/buscador/query', this.palabraBusqueda]);
  }

  logoutAccount(){
    this.endChat()
    this.authService.logout();
    this.token = false;     
    
  }

  products(){
    this.router.navigate(['productos/lista/completa']);
    setTimeout(() => 
      window.location.reload()
    );
  }

  analgesicosProducts(){
    this.router.navigate(['categoria/analgesicos']);
  }

  antiacidosProducts(){
    this.router.navigate(['categoria/antiacidos']);
  }

  antialergicosProducts(){
    this.router.navigate(['categoria/antialergicos']);
  }

  antisepticosProducts(){
    this.router.navigate(['categoria/antisepticos']);
  }

  broncodilatadoresProducts(){
    this.router.navigate(['categoria/broncodilatadores']);
  }

  corticosteroidesProducts(){
    this.router.navigate(['categoria/corticosteroides']);
  }

  hipolipemiantesProducts(){
    this.router.navigate(['categoria/hipolipemiantes']);
  }

  suplementosProducts(){
    this.router.navigate(['categoria/suplementos']);
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

  
  openChatbot() {
    this.botService.chatOpen = true
    this.showChatbot = this.botService.chatOpen;
  }

  closeChatbot() {
    this.botService.chatOpen = false
    this.showChatbot = this.botService.chatOpen;
  }

  endChat(){
    this.botService.endChatwithBot().subscribe(
      response => {
        console.log(response);
      }
    )
  }


}

