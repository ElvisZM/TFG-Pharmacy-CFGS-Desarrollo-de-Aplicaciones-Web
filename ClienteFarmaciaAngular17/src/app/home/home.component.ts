import { Component } from '@angular/core';
import { TopVentasComponent } from '../top-ventas/top-ventas.component';


@Component({
  selector: 'app-home',
  standalone: true,
  imports: [TopVentasComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {

}
