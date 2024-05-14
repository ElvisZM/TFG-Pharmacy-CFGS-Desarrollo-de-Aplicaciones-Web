import { Component, OnInit } from '@angular/core';
import { DatosService } from '../servicios/datos.service';
import { environment } from '../../environments/environment';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-buscador-simple',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './buscador-simple.component.html',
  styleUrl: './buscador-simple.component.scss'
})
export class BuscadorSimpleComponent implements OnInit {

  palabraBuscada: any;

  productos: Array<any> = [];

  public urlPath = environment.apiImageUrl

  constructor(private datosService: DatosService) { }

  ngOnInit(): void {
      this.palabraBuscada = this.datosService.getPalabraBuscada();
      this.datosService.simpleSearchProduct(this.palabraBuscada).subscribe(
        response => {
          console.log(response)
          this.productos = response
        }
      )
      console.log(this.palabraBuscada)
  }

  ngDoCheck(){
    if (this.palabraBuscada != this.datosService.getPalabraBuscada()){
      this.palabraBuscada = this.datosService.getPalabraBuscada();
      this.datosService.simpleSearchProduct(this.palabraBuscada)
      console.log(this.palabraBuscada)

    }

  }

}
