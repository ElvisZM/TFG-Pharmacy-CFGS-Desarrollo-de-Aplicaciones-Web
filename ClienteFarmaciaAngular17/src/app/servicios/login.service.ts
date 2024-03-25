import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  private token_url = 'http://127.0.0.1:8000/api/v1/usuario/token/';

  constructor(private http:HttpClient) { }

  login(dataLogIn: any): Observable<any> {
    const dataGetToken = {
      grant_type: 'password',
      'username': dataLogIn['usuario'],
      'password': dataLogIn['password'],
      'client_id': 'mi_aplicacion',
      'client_secret': 'mi_clave_secreta'
    };

    return this.http.post<any>(this.token_url, dataLogIn)
      .pipe(
        catchError(error => {
          throw error;
        })
      );
  }
}
