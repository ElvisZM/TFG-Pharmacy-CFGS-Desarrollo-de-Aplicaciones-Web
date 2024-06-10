import { Component, DoCheck, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { environment } from '../../environments/environment';
import { DatosService } from '../servicios/datos.service';
import { CommonModule, ViewportScroller } from '@angular/common';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../servicios/auth.service';
import { CartInfoService } from '../servicios/cart-info.service';
import { ReviewsService } from '../servicios/reviews.service';

@Component({
  selector: 'app-product-details',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './product-details.component.html',
  styleUrl: './product-details.component.scss'
})
export class ProductDetailsComponent implements OnInit, DoCheck{

  product: any;
  product_reviews: any;
  
  public url = environment.apiImageUrl;

  user_picture: string = ""

  api_imagen_url: string = "";
  api_imagen_existe: boolean = false

  quantityOptions: Array<number> = [1,2,3,4,5,6,7,8,9,10]

  quantitySelected: number = 1

  productos_recomendados: any

  review: boolean = true

  public FormReviewProduct!: FormGroup
  currentRating = 0;

  userLoged: boolean = false

  campoFormVacio: boolean = false;

  source:string = '';

  productosAnadidos: Set<number> = new Set<number>();

  average: number = 0;

  reviews_totales: number = 0;

  constructor(private titleService: Title, private route: ActivatedRoute, private datosService: DatosService, private router: Router, private fb: FormBuilder, private authService: AuthService, private cartInfo: CartInfoService, private reviewService: ReviewsService, private viewportScroller: ViewportScroller) { }

  ngOnInit(): void {


    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.viewportScroller.scrollToPosition([0, 0]);
      }
    });
    
    this.route.paramMap.subscribe(params => {
      const cn_prod = +params.get('cn_prod')!;
      const cif_farm = params.get('cif_farm')!;
      this.datosService.getProduct(cn_prod, cif_farm).subscribe(
        response => {
          if (response === 'Producto no encontrado'){
            this.router.navigate(['not-found'])
          }else{
            this.getProductDetails(response);
          }
          }, error =>{
            console.log(error);
            this.router.navigate(['not-found'])
        }
      )

    })
    
    this.checkIfLoged()

    }

  ngDoCheck() {
    if (this.FormReviewProduct){
      this.checkEmptyFields()
    }
  }


  initializeForm(): void {
    this.FormReviewProduct = this.fb.group({
      review_titulo: ['', Validators.required],
      review_texto: ['', Validators.required],
      review_votacion: [0, Validators.required],
      review_producto: [this.product ? this.product.id : null, Validators.required],
      review_fecha: [this.datosService.date_today, Validators.required],
    });
  }

  getProductDetails(product: any): void{
    this.product = product;
    this.titleService.setTitle(`${this.product.nombre_prod}`);
    this.getProductRecommended(this.product.categoria_id.nombre_cat);

    if (this.product.imagen_prod) {
      this.api_imagen_url = this.url + this.product.imagen_prod;
      this.api_imagen_existe = true;
    }

    this.initializeForm();

    this.reviewService.getProductReviews(this.product.id).subscribe(
      response => {

        this.getProductReviews(response);
      },
      error => {
        console.error('Error al obtener las reseñas del producto:', error);
      }
    );
  }


  getProductReviews(reviews: any): void{
    reviews.sort((a: any, b: any) => b.id - a.id);
    this.reviews_totales = reviews.length;
    this.product_reviews = reviews.slice(0, 6);
    this.getAverageProductReview();
  }


  decodeProfilePicUrl(encodedUrl: string) {
    if (encodedUrl) {

        const urlWithoutMedia = encodedUrl.replace('/media/', '');
        let decodedUrl = decodeURIComponent(urlWithoutMedia);

        if (decodedUrl.startsWith('https:/') && !decodedUrl.startsWith('https://')) {
            decodedUrl = decodedUrl.replace('https:/', 'https://');
        }

        return decodedUrl;
    } else {
        return '';
    }
  }


  getProductRecommended(categoria: string){
    this.datosService.getProductRecommended(categoria).subscribe(response => {
      this.productos_recomendados = response
    })
  }

  addProductRecommendedToCart(producto_id:number){
    if(this.authService.getTokenCookie()){
      this.cartInfo.addProduct(producto_id).subscribe(response => {
        this.productosAnadidos.add(producto_id)
        setTimeout(() => {
          this.productosAnadidos.delete(producto_id)
        }, 2000);
        console.log(response)
      })
    }else{
      this.router.navigate(['/login-register'])
    }
  }


  addProductToCart(producto_id: number, quantity: number){
    if (this.authService.getTokenCookie()){
      this.cartInfo.addProductFromDetails(producto_id, quantity).subscribe(response => {
        this.cartInfo.productoAddedCart = true;
        this.router.navigate(['/carrito/productos/lista']);
        console.log(response)
      })
    }else{
      this.router.navigate(['/login-register'])
    }
    
  }


  showReviews(){
    this.review = true
  }

  showProspecto(){
    this.review = false
  }

  getProductInfo(cn_prod: number, cif_farm:string){
    this.router.navigate(['/detalles/producto', cn_prod, cif_farm])
  }


  setRating(star: number) {
    this.FormReviewProduct.patchValue({ review_votacion: star });
  }

  checkEmptyFields(){
    let emptyField = false;

    Object.keys(this.FormReviewProduct.controls).forEach(control => {
      if (this.FormReviewProduct.get(control)?.value === '' || this.FormReviewProduct.get(control)?.value === undefined || this.FormReviewProduct.get('review_votacion')?.value === 0){
        emptyField = true;
      }
    })
    this.campoFormVacio = emptyField

  }


  sendReview(){
    if (!this.authService.getTokenCookie()){
      this.router.navigate(['/login-register']);
    }else{
      const reviewForm = this.FormReviewProduct.value
    
      const reviewData = {
        titulo: reviewForm.review_titulo,
        puntuacion: reviewForm.review_votacion,
        fecha_votacion: reviewForm.review_fecha,
        comenta_votacion: reviewForm.review_texto,
        producto_id: reviewForm.review_producto,
      } 

      console.log(reviewData)
      this.reviewService.createReview(reviewData).subscribe(response => {
        this.reviewService.getProductReviews(reviewData.producto_id).subscribe(response => {
          this.FormReviewProduct.reset();
          this.initializeForm()
          this.getProductReviews(response)
        
        })
      })
    }
  }


  login(){
    this.router.navigate(['/login-register']);
  }


  checkIfLoged(){
    this.authService.getTokenCookie()?this.userLoged=true:this.userLoged=false;
    if (this.userLoged==true){
      this.user_picture=this.authService.getNamePicture().picture
      this.source=this.authService.getSource()
    }
  }

  getAverageProductReview(){
    let total = 0;
    this.product_reviews.forEach((review: any) => {
      total += review.puntuacion
    })
    this.average = total / this.product_reviews.length.toFixed(2);
    return this.average
  }

  getStarCounts(average: number) {
    if (average){
      const fullStars = Math.floor(average);
      const hasHalfStar = (average % 1) >= 0.5;
      const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
      return { fullStars, hasHalfStar, emptyStars };
    }
    return { fullStars: 0, hasHalfStar: false, emptyStars: 5 };
  
  }

  generateRange(stock: number): number[] {
    return Array.from({ length: stock }, (_, i) => i + 1);
  }

}
