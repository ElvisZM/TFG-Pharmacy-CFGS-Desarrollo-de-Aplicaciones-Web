import { Component, ChangeDetectionStrategy, inject, OnInit, DoCheck } from '@angular/core';
import { TopVentasComponent } from '../top-ventas/top-ventas.component';
import { TypewriterService} from '../servicios/typewriter.service';
import { bootstrapApplication } from '@angular/platform-browser';
import 'zone.js';
import { isEmpty, map } from 'rxjs';
import { AsyncPipe } from '@angular/common';
import { AuthService } from '../servicios/auth.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [TopVentasComponent, AsyncPipe],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HomeComponent implements OnInit, DoCheck{
  
  private typewriterService = inject(TypewriterService);
  
  username!: string;
  userPicture!: string;
  typedText$!: any;
  titles!: Array<string>;

  constructor(private authService: AuthService){ }

  ngOnInit(): void {  
    this.usernameTitleAnimated();
    console.log(this.authService.getUserRol())
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

