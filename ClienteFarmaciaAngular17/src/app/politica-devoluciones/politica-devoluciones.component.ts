import { ViewportScroller } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-politica-devoluciones',
  standalone: true,
  imports: [],
  templateUrl: './politica-devoluciones.component.html',
  styleUrl: './politica-devoluciones.component.scss'
})
export class PoliticaDevolucionesComponent implements OnInit{

  constructor(private router: Router, private viewportScroller: ViewportScroller, private titleService:Title){}


  ngOnInit() {
    this.titleService.setTitle('Política de Devoluciones');

    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.viewportScroller.scrollToPosition([0, 0]);
      }
    })
  }


}
