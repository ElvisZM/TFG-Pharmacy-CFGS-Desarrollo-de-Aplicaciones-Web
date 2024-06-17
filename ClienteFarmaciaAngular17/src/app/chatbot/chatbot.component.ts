import { CommonModule } from '@angular/common';
import { Component, DoCheck, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../servicios/auth.service';
import { environment } from '../../environments/environment';
import { BotService } from '../servicios/bot.service';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';



interface Message {
  text: string;
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

  public url: string = environment.apiImageUrl

  token: boolean = false;
  name: string = '';
  picture: string = '';
  rol: string = '';
  source: string = '';


  datetime : Date = new Date();
  time_now = this.datetime.getHours() + ":" + this.datetime.getMinutes() + ":" + this.datetime.getSeconds();

  messageText: string = '';
  messages: Message[] = [
    { text: '¡Hola! Me llamo Doc, y... ¡vengo del futuro!', author: 'bot', time: this.time_now },
    { text: 'Puedo ayudarte con información sobre nuestros productos, servicios o cualquier otra pregunta que tengas. ¿En que necesitas de mi ayuda?', author: 'bot', time: this.time_now }
  ];


  constructor(private authService: AuthService, private botService: BotService, private router: Router){}

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

      this.datetime = new Date;
      this.time_now = this.datetime.getHours() + ":" + this.datetime.getMinutes() + ":" + this.datetime.getSeconds();
      
      this.messages.push({ text: this.messageText, author: 'user', time: this.time_now });
      this.botService.sendMessageToServer(this.messageText, 'user').pipe(
        catchError(error => {
          console.log(error)
          return throwError(error)
        })
        ).subscribe(response => {
          const respuesta_bot = response.respuesta_bot
          const datetime_bot = new Date
          const time_bot_now = datetime_bot.getHours() + ":" + datetime_bot.getMinutes() + ":" + datetime_bot.getSeconds();
          this.messages.push({ text: respuesta_bot, author: 'bot', time: time_bot_now });
          console.log(response)
        });
      
        
      
      console.log('Mensaje enviado:', this.messageText);
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
