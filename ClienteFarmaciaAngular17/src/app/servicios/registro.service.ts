import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})

export class RegistroService {

  private urlPath = environment.apiUrlAuthUsers;

  constructor(private http: HttpClient) { }

  registerUser(dataSignUp: any): Observable<any>{ 
    return this.http.post<any>(this.urlPath+'registrar/usuario', dataSignUp)
      .pipe(
        catchError(error => {
          throw error;
        })
      );
  }

  registerGoogleDataToServer(dataGoogle: any): Observable<any>{
    return this.http.post<any>(this.urlPath+'registrar/usuario/google', dataGoogle)
      .pipe(
        catchError(error => {
          throw error;
        })
      );
  }

  registerFacebookDataToServer(dataFacebook: any): Observable<any>{
    return this.http.post<any>(this.urlPath+'registrar/usuario/facebook', dataFacebook)
      .pipe(
        catchError(error => {
          throw error;
        })
      );
  }
}