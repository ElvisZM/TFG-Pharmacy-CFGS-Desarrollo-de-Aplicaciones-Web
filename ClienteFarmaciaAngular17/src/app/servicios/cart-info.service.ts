import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';
import { Observable} from 'rxjs';



type pepe ={
  nombre : String,
  edad : number
}
enum jojo {
  LEFT = "Izquierda", RIGHT = "derecha"

}
@Injectable({
  providedIn: 'root'
})

export class CartInfoService {

  private urlPath = environment.apiCartPromos;

  userCart: any;

  constructor(private http: HttpClient, private router:Router, private authService: AuthService) { }



  getCartInfo(): Observable<any> {
    const headers = this.authService.getHeadersApiRequest()
    return this.http.get(this.urlPath + 'carrito/usuario', headers)
  }

  addProduct(producto_id: number){
    const headers = this.authService.getHeadersApiRequest()
    return this.http.post(this.urlPath + 'carrito/usuario/agregar/producto/'+producto_id, {}, headers)
  }


  
}
