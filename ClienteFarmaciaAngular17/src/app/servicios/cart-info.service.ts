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

  productoAddedCart: boolean = false;

  constructor(private http: HttpClient, private router:Router, private authService: AuthService) { }



  getCartInfo(): Observable<any> {
    const headers = this.authService.getHeadersApiRequest()
    return this.http.get(this.urlPath + 'carrito/usuario', headers)
  }

  addProduct(producto_id: number){
    const headers = this.authService.getHeadersApiRequest()
    return this.http.post(this.urlPath + 'carrito/usuario/agregar/producto/'+producto_id, {}, headers)
  }

  deleteProduct(producto_id: number){
    const headers = this.authService.getHeadersApiRequest()
    return this.http.delete(this.urlPath + 'carrito/eliminar/producto/'+producto_id, headers)
  }

  updateProductQuantity(producto_id: number, quantity: any){
    const headers = this.authService.getHeadersApiRequest()
    return this.http.put(this.urlPath + 'carrito/actualizar/cantidad/producto/'+producto_id,{"cantidad":quantity} ,headers)
  }
  
  addProductFromDetails(producto_id: number, quantity: any){
    const headers = this.authService.getHeadersApiRequest()
    return this.http.post(this.urlPath + 'carrito/agregar/productos/detalles/'+producto_id, {"cantidad":quantity}, headers)
  }

  

}
