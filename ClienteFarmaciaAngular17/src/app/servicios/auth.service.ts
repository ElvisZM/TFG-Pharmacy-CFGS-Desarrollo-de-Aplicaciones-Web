import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})


export class AuthService {

  private apiTokenUrl = 'http://127.0.0.1:8000/service/auth/users/usuario/token/';

  constructor(private http: HttpClient, private cookies: CookieService) { }


  setTokenCookie(token:string){
    this.cookies.set("token",token);
  }


  getTokenCookie(){
    return this.cookies.get("token");
  }


  getUserLogged(): Observable<any> {
    const token = this.getTokenCookie();
    const headers = new HttpHeaders({
      'Authorization': 'Bearer ' + token
    });

    return this.http.get<any>(`${this.apiTokenUrl}`+`${token}`, {headers})
    .pipe(
      catchError(error => {
        throw error;
      })
    );
  }


  logout() {
    this.cookies.delete("token");
  }

}
