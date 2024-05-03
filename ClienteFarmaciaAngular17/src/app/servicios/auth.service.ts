declare var google: any;
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
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

  setGoogleUserCookie(googleUser:any){
    this.cookies.set("googleUser", JSON.stringify(googleUser))
  }

  getGoogleUserCookie(){
    return this.cookies.get("googleUser")
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
    this.cookies.delete("googleUser");
    google.accounts.id.disableAutoSelect();
  }

  getHeaders(): Observable <any> {
    let headers: any = {}
    if (this.getGoogleUserCookie().length > 0) {
      headers = {
        'Authorization': `Bearer ${this.getGoogleUserCookie()}`,
        'Content-Type': 'application/json'
      }
      return headers;
    }else if(this.getTokenCookie().length > 0) {
      headers = {
        'Authorization': `Bearer ${this.getTokenCookie()}`,
        'Content-Type': 'application/json'
      };
      return headers;
    }
    return headers;
    }


}
