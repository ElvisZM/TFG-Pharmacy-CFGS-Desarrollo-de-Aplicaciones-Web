import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})

export class LoginService {

  private urlPath = environment.apiTokenUrl

  constructor(private http:HttpClient) { }

  loginToken(dataLogIn: any): Observable<any> {
    const dataGetToken = new HttpParams()
    .set('grant_type', 'password')
    .set('username', dataLogIn['username'])
    .set('password', dataLogIn['password'])
    .set('client_id', 'mi_aplicacion_tfg_psur')
    .set('client_secret', 'mi_clave_secreta_tfg_psur');
    
    const cabecera = {
      'Content-Type': 'application/x-www-form-urlencoded',
    }

    return this.http.post<any>(this.urlPath, dataGetToken.toString(),{headers:cabecera})
      .pipe(
        catchError(error => {
          throw error;
        })
      );
  }
}
