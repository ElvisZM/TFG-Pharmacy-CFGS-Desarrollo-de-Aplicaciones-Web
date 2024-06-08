import { Component, OnInit } from '@angular/core';
import { DatosService } from '../servicios/datos.service';
import { environment } from '../../environments/environment';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../servicios/auth.service';
import { CartInfoService } from '../servicios/cart-info.service';

@Component({
  selector: 'app-buscador-simple',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './buscador-simple.component.html',
  styleUrl: './buscador-simple.component.scss'
})
export class BuscadorSimpleComponent implements OnInit {

  palabraBuscada: any;

  productos: Array<any> = [];

  textoInfo: string = 'Estos son los productos que hemos encontrado para ti con: '
  mostrarMensaje: boolean = false;
  mostrarImagen: boolean = false;
  public url = environment.apiImageUrl

  productosAnadidos: Set<number> = new Set<number>();

  constructor(private datosService: DatosService, private router: Router, private authService: AuthService, private cartInfo: CartInfoService) { }

  ngOnInit(): void {
      this.palabraBuscada = this.datosService.getPalabraBuscada();
      this.searchProducts();
  }

  ngDoCheck(){
    if (this.palabraBuscada != this.datosService.getPalabraBuscada()){
      this.palabraBuscada = this.datosService.getPalabraBuscada();
      this.searchProducts();
    }
  }

  searchProducts() {
    if (this.palabraBuscada) {
      this.datosService.simpleSearchProduct(this.palabraBuscada).subscribe(
        response => {
          this.productos = response;
          if (this.productos.length > 0){
            this.mostrarMensaje = true;
            this.mostrarImagen = false;
          }else{
            this.mostrarMensaje = false
            this.mostrarImagen = true
          }
          
        }
      );
    } else {
      this.datosService.getProductsList().subscribe(
        response => {
          this.productos = response;
          if (this.productos.length > 0){
            this.mostrarMensaje = false;
            this.mostrarImagen = false
          }else{
            this.mostrarImagen = true
          }
        })
    }
  }


  addProductToCart(producto_id: number){
    if(this.authService.getTokenCookie()){
      this.cartInfo.addProduct(producto_id).subscribe(response => {
        this.productosAnadidos.add(producto_id)
        setTimeout(() => {
          this.productosAnadidos.delete(producto_id)
        }, 3000)
        console.log(response)
      }, error => {
        console.log(error)
      })
    }else{
      this.router.navigate(['login-register'])
    }
  }


  getProductInfo(cn_prod: number, cif_farm:string){
    this.router.navigate(['/detalles/producto', cn_prod, cif_farm])
  }


}
