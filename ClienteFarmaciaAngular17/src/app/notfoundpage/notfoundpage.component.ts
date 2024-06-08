import { ViewportScroller } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-notfoundpage',
  standalone: true,
  imports: [],
  templateUrl: './notfoundpage.component.html',
  styleUrl: './notfoundpage.component.scss'
})
export class NotfoundpageComponent implements OnInit{

  constructor(private router: Router, private viewportScroller: ViewportScroller){}


  ngOnInit() {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.viewportScroller.scrollToPosition([0, 0]);
      }
    });
  }

  backToIndex(){
    this.router.navigate([''])
  }

}
