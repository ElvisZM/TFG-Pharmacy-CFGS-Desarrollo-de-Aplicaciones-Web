import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})

export class RegistroService {
  private apiUrlRegistro = 'http://elviszm12.pythonanywhere.com/api/v1/registrar/usuario';

  constructor(private http: HttpClient) { }

  registroUsuario(dataSignUp: any): Observable<any>{ 
    return this.http.post<any>(this.apiUrlRegistro, dataSignUp)
      .pipe(
        catchError(error => {
          throw error;
        })
      );
  }
}
