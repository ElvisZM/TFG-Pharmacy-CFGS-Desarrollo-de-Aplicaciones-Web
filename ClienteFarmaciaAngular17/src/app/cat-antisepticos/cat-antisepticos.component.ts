import { ChangeDetectorRef, Component } from '@angular/core';
import { environment } from '../../environments/environment';
import { NavigationEnd, Router } from '@angular/router';
import { DatosService } from '../servicios/datos.service';
import { ReviewsService } from '../servicios/reviews.service';
import { CartInfoService } from '../servicios/cart-info.service';
import { Title } from '@angular/platform-browser';
import { CommonModule, ViewportScroller } from '@angular/common';
import { AuthService } from '../servicios/auth.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-cat-antisepticos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './cat-antisepticos.component.html',
  styleUrl: './cat-antisepticos.component.scss'
})
export class CatAntisepticosComponent {


  AllProducts: Array<any> = [];

  valorOrden: any;

  productosAnadidos: Set<number> = new Set<number>();

  public url: string = environment.apiImageUrl

  constructor(private router:Router, private datosService:DatosService, private cdRef: ChangeDetectorRef, private reviewsService: ReviewsService, private authService: AuthService, private cartInfo: CartInfoService, private viewportScroller: ViewportScroller, private titleService:Title) {}

  ngOnInit(): void {
    this.getAllProducts();
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.viewportScroller.scrollToPosition([0, 0]);
      }
    });      
    this.titleService.setTitle('Antisépticos');
  }


  getAllProducts(): void {
    this.datosService.getProductsAntisepticos().subscribe(
      response => {
          this.AllProducts = response

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
    console.log(this.valorOrden);
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

  goIndex(){
    this.router.navigate(['/'])
  }

}
