import { Component, DoCheck, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { CartInfoService } from '../servicios/cart-info.service';
import { environment } from '../../environments/environment';
import { tap } from 'rxjs';


@Component({
  selector: 'app-shopping-cart',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './shopping-cart.component.html',
  styleUrl: './shopping-cart.component.scss'
})
export class ShoppingCartComponent implements OnInit {

  carrito: any = {};
  public urlPicture = environment.apiImageUrl;
  empty: boolean = false;

  recommendedProducts: Array<any> = [];

  constructor(private cartInfo: CartInfoService){}

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

  getCosteEnvio(){
    return 2
  }

  getIVAimport(){
    return +(((this.carrito.total_carrito + 5) *21) / 121).toFixed(2)
  }

  getTotalPrice(){
    return (this.carrito.total_carrito + this.getCosteEnvio() + this.getIVAimport()).toFixed(2)  
  }


  addProductToCart(producto_id: number){
    this.cartInfo.addProduct(producto_id).subscribe(response => {
      this.cartInfo.getCartInfo().subscribe(response => {
        this.carrito = response;
        this.empty = this.carrito.productos.length === 0;
      })
    })
  }

}
