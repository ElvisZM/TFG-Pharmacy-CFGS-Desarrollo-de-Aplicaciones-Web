import { CommonModule } from '@angular/common';
import { Component, DoCheck, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../servicios/auth.service';
import { environment } from '../../environments/environment';
import { BotService } from '../servicios/bot.service';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';



interface Message {
  text: string | SafeHtml;
  author: 'user' | 'bot';
  time: string;
}

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.scss'
})
export class ChatbotComponent implements OnInit, DoCheck{
  public safeHtmlContent: SafeHtml = '';


  public url: string = environment.apiImageUrl

  token: boolean = false;
  name: string = '';
  picture: string = '';
  rol: string = '';
  source: string = '';


  datetime_default : Date = new Date();

  hora_default = this.datetime_default.getHours().toString().padStart(2, '0');
  minutos_default = this.datetime_default.getMinutes().toString().padStart(2, '0');
  segundos_default = this.datetime_default.getSeconds().toString().padStart(2, '0');

  time_now_default = this.hora_default + ":" + this.minutos_default + ":" + this.segundos_default;

  messageText: string = '';
  messages: Message[] = [
    { text: '¡Hola! Me llamo Doc, y... ¡vengo del futuro!', author: 'bot', time: this.time_now_default },
    { text: 'Puedo ayudarte con información sobre nuestros productos, servicios o cualquier otra pregunta que tengas. ¿En que necesitas de mi ayuda?', author: 'bot', time: this.time_now_default }
  ];



  constructor(private authService: AuthService, private botService: BotService, private router: Router, private sanitizer: DomSanitizer){}

  ngOnInit(): void {
      if (this.authService.getTokenCookie()){
        this.token = true;
        this.name = this.authService.getNamePicture().name;
        this.picture = this.authService.getNamePicture().picture;
        this.rol = this.authService.getUserRol();
        this.source = this.authService.getSource()
      }else{
        this.token = false;
      }
      
  }

  ngDoCheck(){
    if (this.authService.getTokenCookie()){
      this.token = true;
      this.name = this.authService.getNamePicture().name;
      this.picture = this.authService.getNamePicture().picture;
      this.rol = this.authService.getUserRol();
      this.source = this.authService.getSource();
    }else{
      this.token = false;
    }
  }

  sendMessage(event: Event) {
    if (!this.token){
      return;

    }else if (!this.messageText) {
      return;

    }else{

      const datetime_user = new Date;


      let hora_user = datetime_user.getHours().toString().padStart(2, '0');
      let minutos_user = datetime_user.getMinutes().toString().padStart(2, '0');
      let segundos_user = datetime_user.getSeconds().toString().padStart(2, '0');

      const time_now_user = hora_user + ":" + minutos_user + ":" + segundos_user;
      
      this.messages.push({ text: this.messageText, author: 'user', time: time_now_user });
      this.botService.sendMessageToServer(this.messageText, 'user').pipe(
        catchError(error => {
          return throwError(error)
        })
        ).subscribe(response => {
          const respuesta_bot = response.respuesta_bot
          const datetime_bot = new Date


          let hora_bot = datetime_bot.getHours().toString().padStart(2, '0');
          let minutos_bot = datetime_bot.getMinutes().toString().padStart(2, '0');
          let segundos_bot = datetime_bot.getSeconds().toString().padStart(2, '0');

          const time_now_bot = hora_bot + ":" + minutos_bot + ":" + segundos_bot;
          this.safeHtmlContent = this.sanitizer.bypassSecurityTrustHtml(respuesta_bot);

          this.messages.push({ text: this.safeHtmlContent, author: 'bot', time: time_now_bot });
        });
      
      this.messageText = '';
    }

  }

  login(){
    this.botService.chatOpen = false;
    this.router.navigate(['login-register']).then(
      () => window.location.reload()
    );
  }

}
