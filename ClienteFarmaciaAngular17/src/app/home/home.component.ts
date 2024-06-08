import { Component, ChangeDetectionStrategy, inject, OnInit, DoCheck, ViewEncapsulation } from '@angular/core';
import { TopVentasComponent } from '../top-ventas/top-ventas.component';
import { TypewriterService} from '../servicios/typewriter.service';
import { Title, bootstrapApplication } from '@angular/platform-browser';
import 'zone.js';
import { isEmpty, map } from 'rxjs';
import { AsyncPipe, ViewportScroller } from '@angular/common';
import { AuthService } from '../servicios/auth.service';
import { NavigationEnd, Router } from '@angular/router';


@Component({
  selector: 'app-home',
  standalone: true,
  imports: [TopVentasComponent, AsyncPipe
    ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
  encapsulation: ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HomeComponent implements OnInit, DoCheck{
  
  private typewriterService = inject(TypewriterService);
  username!: string;
  userPicture!: string;
  typedText$!: any;
  titles!: Array<string>;

  constructor(private authService: AuthService, private titleService: Title, private router: Router, private viewportScroller: ViewportScroller){ }

  ngOnInit(): void {  
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.viewportScroller.scrollToPosition([0, 0]);
      }
    });

    this.usernameTitleAnimated();
    this.authService.getUserRol()
    this.titleService.setTitle('P.Sur Pharmacy | Farmacia online');

  }

  ngDoCheck(): void {
  }
  usernameTitleAnimated(){
    this.titles = [', hoy y siempre.', ', cada paso del camino.']
    if (this.authService.getTokenCookie()){
      const user_name = this.authService.getNamePicture().name;
      this.titles = [`, ${user_name}.`,', hoy y siempre.', ', cada paso del camino.']
    }
    this.typedText$ = this.typewriterService
    .getTypewriterEffect(this.titles)
    .pipe(map((text) => text));
    
  }

}

