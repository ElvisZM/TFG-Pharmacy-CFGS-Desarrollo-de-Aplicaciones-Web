import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import '../../assets/js/top-ventas.js';
import { DatosService } from '../servicios/datos.service.js';
import { environment } from '../../environments/environment.js';

@Component({
  selector: 'app-top-ventas',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './top-ventas.component.html',
  styleUrl: './top-ventas.component.scss'
})
export class TopVentasComponent implements OnInit {

  topVentaProducts: Array<any> = [];

  public urlPicture = environment.apiImageUrl

  constructor(private datosService: DatosService){}


  ngOnInit(): void {
      this.getTopVentas();
  }

  getTopVentas(){
    this.datosService.getProductsList().subscribe(data => {
      this.topVentaProducts = data;
      this.topVentaProducts = this.topVentaProducts.slice(0, 8);

    })
  }

}
