import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})

export class RegistroService {
  private apiUrlRegistro = 'http://127.0.0.1:8000/service/auth/users/registrar/usuario';

  constructor(private http: HttpClient) { }

  registerUser(dataSignUp: any): Observable<any>{ 
    return this.http.post<any>(this.apiUrlRegistro, dataSignUp)
      .pipe(
        catchError(error => {
          throw error;
        })
      );
  }
}
