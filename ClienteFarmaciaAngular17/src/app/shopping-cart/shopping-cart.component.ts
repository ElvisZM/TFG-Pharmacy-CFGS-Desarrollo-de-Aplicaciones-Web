import { Component, DoCheck, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { CartInfoService } from '../servicios/cart-info.service';
import { environment } from '../../environments/environment';
import { tap } from 'rxjs';
import { FormsModule } from '@angular/forms';



@Component({
  selector: 'app-shopping-cart',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './shopping-cart.component.html',
  styleUrl: './shopping-cart.component.scss'
})
export class ShoppingCartComponent implements OnInit {

  carrito: any = {};
  public urlPicture = environment.apiImageUrl;
  empty: boolean = false;

  recommendedProducts: Array<any> = [];

  quantityOptions: Array<number> = [1,2,3,4,5,6,7,8,9,10]

  constructor(private cartInfo: CartInfoService, private router: Router){}

  ngOnInit() {
    this.loadCartInfo();
  }

  ngDoCheck(): void {
  }


  loadCartInfo() {
    this.cartInfo.getCartInfo().subscribe(response => {
      this.carrito = response;
      
      this.empty = this.carrito.productos.length === 0;
    });
  }

  getSubTotal(){
    return +((this.carrito.total_carrito / 1.21)).toFixed(2)
  }

  getCosteEnvio(){
    return 2
  }

  getIVAimport(){
    return +((this.carrito.total_carrito / 1.21)*0.21).toFixed(2)
  }

  getTotalPrice(){
    return (this.carrito.total_carrito + this.getCosteEnvio()).toFixed(2)  
  }


  addProductToCart(producto_id: number){
    this.cartInfo.addProduct(producto_id).subscribe(response => {
      this.cartInfo.getCartInfo().subscribe(response => {
        this.carrito = response;
        this.empty = this.carrito.productos.length === 0;
      })
    })
  }

  backToHome(){
    this.router.navigate(['/'])
  }

  redirectToPayment(){
    this.router.navigate(['/tipo/pago']);
  }

  deleteProductFromCart(producto_id: number){
    this.cartInfo.deleteProduct(producto_id).subscribe(response => {
      this.cartInfo.getCartInfo().subscribe(response => {
        this.carrito = response;
        this.empty = this.carrito.productos.length === 0;
      })
    })
  }

  updateProductUnits(producto_id: number, quantity: any){
    this.cartInfo.updateProductQuantity(producto_id, quantity).subscribe(response => {
      this.cartInfo.getCartInfo().subscribe(response => {
        this.carrito = response;
        this.empty = this.carrito.productos.length === 0;
      })
    })
    console.log("evento activado")
  }

}
