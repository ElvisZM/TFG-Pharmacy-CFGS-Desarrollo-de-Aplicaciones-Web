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

  textoInfo: string = 'Estos son los productos que hemos encontrado para ti con: '
  mostrarMensaje: boolean = false;
  mostrarImagen: boolean = false;
  public urlPath = environment.apiImageUrl

  constructor(private datosService: DatosService) { }

  ngOnInit(): void {
      this.palabraBuscada = this.datosService.getPalabraBuscada();
      this.searchProducts();
  }

  ngDoCheck(){
    if (this.palabraBuscada != this.datosService.getPalabraBuscada()){
      this.palabraBuscada = this.datosService.getPalabraBuscada();
      this.searchProducts();
    }
  }

  searchProducts() {
    if (this.palabraBuscada) {
      this.datosService.simpleSearchProduct(this.palabraBuscada).subscribe(
        response => {
          this.productos = response;
          if (this.productos.length > 0){
            this.mostrarMensaje = true;
            this.mostrarImagen = false;
          }else{
            this.mostrarMensaje = false
            this.mostrarImagen = true
          }
          
        }
      );
    } else {
      this.datosService.getProductsList().subscribe(
        response => {
          this.productos = response;
          if (this.productos.length > 0){
            this.mostrarMensaje = false;
            this.mostrarImagen = false
          }else{
            this.mostrarImagen = true
          }
        })
    }
  }
}
