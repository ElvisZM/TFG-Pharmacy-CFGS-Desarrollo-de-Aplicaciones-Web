import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})

export class LoginService {
  private token_url = 'http://127.0.0.1:8000/oauth2/token/';

  constructor(private http:HttpClient) { }

  loginToken(dataLogIn: any): Observable<any> {
    const dataGetToken = new HttpParams()
    .set('grant_type', 'password')
    .set('username', dataLogIn['username'])
    .set('password', dataLogIn['password'])
    .set('client_id', 'mi_aplicacion')
    .set('client_secret', 'mi_clave_secreta');
    
    const cabecera = {
      'Content-Type': 'application/x-www-form-urlencoded',
    }

    return this.http.post<any>(this.token_url, dataGetToken.toString(),{headers:cabecera})
      .pipe(
        catchError(error => {
          throw error;
        })
      );
  }
}
