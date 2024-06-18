import { ViewportScroller } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-politica-avisolegal',
  standalone: true,
  imports: [],
  templateUrl: './politica-avisolegal.component.html',
  styleUrl: './politica-avisolegal.component.scss'
})
export class PoliticaAvisolegalComponent implements OnInit {

  constructor(private titleService: Title, private router:Router, private viewportScroller: ViewportScroller){}

  ngOnInit() {
    this.titleService.setTitle('Aviso Legal');
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.viewportScroller.scrollToPosition([0, 0]);
      }
    });
  }


}
