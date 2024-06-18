import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';
import { Observable, catchError} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BotService {

  private urlPath = environment.apiChatbot;

  chatOpen: boolean = false;

  constructor(private http: HttpClient, private authService: AuthService) { }

  sendMessageToServer(message: string, author: string): Observable<any> {
    const headers = this.authService.getHeadersApiRequest()
    const body = {
      'texto': message,
      'author': author
    }
    console.log(headers)
    return this.http.post(this.urlPath + 'openai/api', body, headers).pipe(catchError(error=>{
      console.log('Error en el servicio de chatbot', error);
      return error;
    }))
  }

  endChatwithBot(): Observable<any>{
    const headers = this.authService.getHeadersApiRequest();
    console.log(headers)
    return this.http.post(this.urlPath + 'end/chat', {}, {headers: headers.headers}).pipe(catchError(error => {
      console.log('El error',error);
      return error
    }))
  }


}
