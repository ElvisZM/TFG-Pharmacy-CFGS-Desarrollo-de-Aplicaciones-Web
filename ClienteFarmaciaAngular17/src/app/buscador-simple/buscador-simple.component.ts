import { Component, OnInit } from '@angular/core';
import { DatosService } from '../servicios/datos.service';

@Component({
  selector: 'app-buscador-simple',
  standalone: true,
  imports: [],
  templateUrl: './buscador-simple.component.html',
  styleUrl: './buscador-simple.component.scss'
})
export class BuscadorSimpleComponent implements OnInit {

  palabraBuscada: any;

  producto: Array<any> = [];

  constructor(private datosService: DatosService) { }

  ngOnInit(): void {
      this.palabraBuscada = this.datosService.getPalabraBuscada();
      this.datosService.simpleSearchProduct(this.palabraBuscada).subscribe(
        response => {
          console.log(response)
          this.producto = response
        }
      )

  }


}
