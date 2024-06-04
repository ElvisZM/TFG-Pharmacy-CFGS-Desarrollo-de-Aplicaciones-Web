import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { environment } from '../../environments/environment';
import { DatosService } from '../servicios/datos.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-product-details',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './product-details.component.html',
  styleUrl: './product-details.component.scss'
})
export class ProductDetailsComponent implements OnInit{

  product: any;
  
  public url = environment.apiImageUrl;

  api_imagen_url: string = ""
  api_imagen_existe: boolean = false

  quantityOptions: Array<number> = [1,2,3,4,5,6,7,8,9,10]

  productos_recomendados: any

  review: boolean = true

  constructor(private titleService: Title, private route: ActivatedRoute, private datosService: DatosService, private router: Router) { }

  ngOnInit(): void {
    this.titleService.setTitle('Sitio Administrativo | Modificar producto');

    this.route.paramMap.subscribe(params => {
      const cn_prod = +params.get('cn_prod')!;
      const cif_farm = params.get('cif_farm')!;
      this.datosService.getProduct(cn_prod, cif_farm).subscribe(
        response => {
          this.product = response
          console.log(this.product)
          this.getProductRecommended(this.product.categoria_id.nombre_cat)

          if(this.product.imagen_prod){
            this.api_imagen_url = this.url + this.product.imagen_pro
            this.api_imagen_existe = true;
          }
        }
      )
    })
  }

  getProductRecommended(categoria: string){
    this.datosService.getProductRecommended(categoria).subscribe(response => {
      this.productos_recomendados = response
      console.log(this.productos_recomendados)
    })
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

}
