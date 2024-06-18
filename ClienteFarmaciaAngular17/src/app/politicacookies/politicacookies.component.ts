import { ViewportScroller } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-politicacookies',
  standalone: true,
  imports: [],
  templateUrl: './politicacookies.component.html',
  styleUrl: './politicacookies.component.scss'
})
export class PoliticacookiesComponent implements OnInit{

  constructor(private router: Router, private viewportScroller: ViewportScroller, private titleService: Title) { }


  ngOnInit() {
    this.titleService.setTitle('Política de Cookies');

    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.viewportScroller.scrollToPosition([0, 0]);
      }
    });
  }

}
