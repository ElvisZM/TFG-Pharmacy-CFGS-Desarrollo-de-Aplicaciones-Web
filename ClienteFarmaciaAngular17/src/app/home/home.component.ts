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
export class HomeComponent implements OnInit{
  
  private typewriterService = inject(TypewriterService);
  
  username!: string;
  userPicture!: string;
  typedText$!: any;
  titles!: Array<string>;

  constructor(private authService: AuthService){ }

  ngOnInit(): void {  
    this.usernameTitleAnimated();
  }

  usernameTitleAnimated(){
    this.titles = [', hoy y siempre.', ', cada paso del camino.']
    if (this.checkUsernameGoogle()!= undefined){
      this.titles = [`, ${this.username}`,', hoy y siempre.', ', cada paso del camino.']
    }
    this.typedText$ = this.typewriterService
    .getTypewriterEffect(this.titles)
    .pipe(map((text) => text));
    
  }
  checkUsernameGoogle():string | undefined {  
    if(this.authService.getGoogleUserCookie().length > 0){
      this.username = JSON.parse(this.authService.getGoogleUserCookie()).given_name;
      return this.username;
    }
    return undefined;
  }


}

