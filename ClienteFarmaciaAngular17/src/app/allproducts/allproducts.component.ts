import { Component, OnInit } from '@angular/core';
import { DatosService } from '../servicios/datos.service';
import { environment } from '../../environments/environment';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-allproducts',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './allproducts.component.html',
  styleUrl: './allproducts.component.scss'
})
export class AllproductsComponent implements OnInit {

  AllProducts: Array<any> = [];

  public urlPicture = environment.apiImageUrl

  constructor(private datosService: DatosService){}

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


}
