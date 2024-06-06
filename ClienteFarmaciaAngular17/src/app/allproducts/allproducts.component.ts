import { Component, OnInit } from '@angular/core';
import { DatosService } from '../servicios/datos.service';
import { environment } from '../../environments/environment';
import { CommonModule } from '@angular/common';
import { CartInfoService } from '../servicios/cart-info.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-allproducts',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './allproducts.component.html',
  styleUrl: './allproducts.component.scss'
})
export class AllproductsComponent implements OnInit {

  AllProducts: Array<any> = [];

  public url = environment.apiImageUrl

  productoAnadido: boolean = false

  constructor(private datosService: DatosService, private cartInfo: CartInfoService, private router:Router){}

  ngOnInit(): void {
      this.getAllProducts();      
  }

  getAllProducts(): void {
    this.datosService.getProductsList().subscribe(
      response => {
        this.AllProducts = response
      }
    )

  }

  addProductToCart(producto_id: number){
    this.cartInfo.addProduct(producto_id).subscribe(response => {
      this.productoAnadido = true
      setTimeout(() => {
        this.productoAnadido = false
      }, 3000)
      console.log(response)
    }, error => {
      console.log(error)
    })
  }

  getProductInfo(cn_prod: number, cif_farm:string){
    this.router.navigate(['/detalles/producto', cn_prod, cif_farm])
  }


}
