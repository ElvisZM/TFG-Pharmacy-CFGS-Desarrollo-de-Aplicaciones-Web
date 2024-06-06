import { Component, DoCheck, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { environment } from '../../environments/environment';
import { DatosService } from '../servicios/datos.service';
import { CommonModule } from '@angular/common';
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

  constructor(private titleService: Title, private route: ActivatedRoute, private datosService: DatosService, private router: Router, private fb: FormBuilder, private authService: AuthService, private cartInfo: CartInfoService, private reviewService: ReviewsService) { }

  ngOnInit(): void {
    
    this.route.paramMap.subscribe(params => {
      const cn_prod = +params.get('cn_prod')!;
      const cif_farm = params.get('cif_farm')!;
      this.datosService.getProduct(cn_prod, cif_farm).subscribe(
        response => {
          this.product = response
          this.titleService.setTitle(`${this.product.nombre_prod}`);
          this.getProductRecommended(this.product.categoria_id.nombre_cat)

          if(this.product.imagen_prod){
            this.api_imagen_url = this.url + this.product.imagen_prod
            this.api_imagen_existe = true;
          }

          this.FormReviewProduct = this.fb.group({
            review_titulo:['', Validators.required],
            review_texto:['', Validators.required],
            review_votacion:[0, Validators.required],
            review_producto:[this.product.id, Validators.required],
            review_fecha:[this.datosService.date_today, Validators.required],
          });

          this.reviewService.getProductReviews(this.product.id).subscribe(response =>{
            this.product_reviews = response
            console.log(this.product_reviews)

          }, error =>{
            console.log(error)
          })

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

  getProductReviews(product_id: number){
    
  }

  decodeProfilePicUrl(encodedUrl: string) {
    if (encodedUrl) {
        console.log('Encoded URL:', encodedUrl);

        const urlWithoutMedia = encodedUrl.replace('/media/', '');
        let decodedUrl = decodeURIComponent(urlWithoutMedia);

        // Correct the URL format by ensuring 'https://' is present
        if (decodedUrl.startsWith('https:/') && !decodedUrl.startsWith('https://')) {
            decodedUrl = decodedUrl.replace('https:/', 'https://');
        }

        console.log('Decoded URL:', decodedUrl);
        return decodedUrl;
    } else {
        console.log("URL está vacía");
        return '';
    }
  }


  getProductRecommended(categoria: string){
    this.datosService.getProductRecommended(categoria).subscribe(response => {
      this.productos_recomendados = response
    })
  }


  addProductToCart(producto_id: number, quantity: number){
    if (this.authService.getTokenCookie()){
      console.log(producto_id)
      this.cartInfo.addProductExistFromDetails(producto_id, quantity).subscribe(response => {
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


      this.reviewService.createReview(reviewData).subscribe(response => {
        console.log(response)
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
    }
  }


}
