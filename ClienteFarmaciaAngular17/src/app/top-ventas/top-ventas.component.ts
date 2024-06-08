import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import '../../assets/js/top-ventas.js';
import { DatosService } from '../servicios/datos.service.js';
import { environment } from '../../environments/environment.js';
import { CartInfoService } from '../servicios/cart-info.service.js';
import { Router } from '@angular/router';
import { AuthService } from '../servicios/auth.service.js';

@Component({
  selector: 'app-top-ventas',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './top-ventas.component.html',
  styleUrl: './top-ventas.component.scss'
})
export class TopVentasComponent implements OnInit {

  topVentaProducts: Array<any> = [];

  public url = environment.apiImageUrl

  productosAnadidos: Set<number> = new Set<number>();

  constructor(private datosService: DatosService, private cartInfo: CartInfoService, private router: Router, private authService: AuthService){}


  ngOnInit(): void {
      this.getTopVentas();
  }

  getTopVentas(){
    this.datosService.getProductsList().subscribe(data => {
      this.topVentaProducts = data.sort((a:any, b:any) => b.ventas - a.ventas);
      this.topVentaProducts = this.topVentaProducts.slice(0, 8);

    })
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
