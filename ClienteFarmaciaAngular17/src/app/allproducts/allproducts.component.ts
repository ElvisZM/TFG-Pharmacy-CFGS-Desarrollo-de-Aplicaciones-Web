import { ChangeDetectorRef, Component, DoCheck, OnInit } from '@angular/core';
import { DatosService } from '../servicios/datos.service';
import { environment } from '../../environments/environment';
import { CommonModule, ViewportScroller } from '@angular/common';
import { CartInfoService } from '../servicios/cart-info.service';
import { NavigationEnd, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../servicios/auth.service';
import { ReviewsService } from '../servicios/reviews.service';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-allproducts',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './allproducts.component.html',
  styleUrl: './allproducts.component.scss'
})
export class AllproductsComponent implements OnInit, DoCheck {

  AllProducts: Array<any> = [];

  productosAnadidos: Set<number> = new Set<number>();

  public url = environment.apiImageUrl

  valorOrden: number = 0;

  constructor(private datosService: DatosService, private cartInfo: CartInfoService, private router:Router, private viewportScroller: ViewportScroller, private authService: AuthService, private reviewsService: ReviewsService, private cdRef: ChangeDetectorRef, private titleService: Title){}

  ngOnInit(): void {
    this.getAllProducts();
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.viewportScroller.scrollToPosition([0, 0]);
      }
    });      
    this.titleService.setTitle('Nuestros productos');

  }

  ngDoCheck(){
  }

  getAllProducts(): void {
    this.datosService.getProductsList().subscribe(
      response => {
          this.AllProducts = response

      }, error=>{
        console.log(error)
      }
    )
  }


  getAverageProductReview(reviews: any){
    let total = 0;
    reviews.forEach((review: any) => {
      total += review.puntuacion
    })
    let average = total / reviews.length;
    return average
  }

  
  async getOrden() {
    if (+this.valorOrden === 0) {
      this.getAllProducts();
    } else if (+this.valorOrden === 1) {

      const reviewPromises = this.AllProducts.map(async (product: any) => {
        const reviews = await this.reviewsService.getProductReviews(product.id).toPromise();
        product.averageRating = reviews.length ? this.getAverageProductReview(reviews) : 0;
      });

      await Promise.all(reviewPromises);

      this.AllProducts.sort((a: any, b: any) => b.averageRating - a.averageRating); 

      this.cdRef.detectChanges();
    } else if (+this.valorOrden === 2) {
      this.AllProducts = this.AllProducts.sort((a: any, b: any) => parseFloat(a.precio) - parseFloat(b.precio));
    } else if (+this.valorOrden === 3) {
      this.AllProducts = this.AllProducts.sort((a: any, b: any) => parseFloat(b.precio) - parseFloat(a.precio));
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
