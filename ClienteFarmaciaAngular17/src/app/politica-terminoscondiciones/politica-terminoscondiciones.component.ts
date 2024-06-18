import { ViewportScroller } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-politica-terminoscondiciones',
  standalone: true,
  imports: [],
  templateUrl: './politica-terminoscondiciones.component.html',
  styleUrl: './politica-terminoscondiciones.component.scss'
})
export class PoliticaTerminoscondicionesComponent implements OnInit{


  constructor(private titleService: Title, private router: Router, private viewportScroller: ViewportScroller){}

  ngOnInit() {
    this.titleService.setTitle('Términos y Condiciones');
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.viewportScroller.scrollToPosition([0, 0]);
      }
    });
  }

}
