declare var google: any;
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})


export class AuthService {

  private urlPath = environment.apiUrlAuthUsers;

  constructor(private http: HttpClient, private cookies: CookieService, private router: Router) { }


  setTokenCookie(token:string){
    this.cookies.set("token",token);
  }

  getTokenCookie(){
    return this.cookies.get("token");
  }

  setNamePicture(name:string, picture_url?:string){
    this.cookies.set("name",name);
    if (picture_url){
      this.cookies.set("picture_url", picture_url);
    }
  }

  getNamePicture(){
    const name = this.cookies.get("name");
    const picture = this.cookies.get("picture_url");
    return {name, picture};
  }

  setUserRol(rol: string){
    this.cookies.set("user_rol", rol)
  }

  getUserRol(){
    return this.cookies.get("user_rol")
  }

  logout() {
    this.cookies.delete("token");
    this.cookies.delete("name");
    this.cookies.delete("picture_url");
    this.cookies.delete("user_rol");
    this.router.navigate(['/']);
    setTimeout(() => {
      window.location.reload();
    },400);
    google.accounts.id.disableAutoSelect();
  }

  getHeadersApiRequest() {
    let headers: any = {}
   
    if(this.getTokenCookie().length > 0) {
      return {
        headers : new HttpHeaders({
        'Authorization': `Bearer ${this.getTokenCookie()}`,
        'Content-Type': 'application/json'
        })
      };
    }
    return headers;
    }

    getHeadersUserInfo(){
      return {
        headers: new HttpHeaders({
          'Authorization': `Bearer ${this.getTokenCookie()}`
        })}
    }

    getUserInfo(){
      const headers = this.getHeadersUserInfo();
      return this.http.get<any>(this.urlPath+'usuario/token/'+this.getTokenCookie(), headers).subscribe(
        response => {
          this.setNamePicture(response.usuario.first_name, response.profile_picture)
          const rol = response.usuario.rol.toString();
          this.setUserRol(rol.toString())
        },error => {
          console.log(error)
        }
      )
    }

    getFacebookUserProfile(accessToken: string){
      const fields = 'id,email,name,picture';
      const url = `https://graph.facebook.com/me?fields=${fields}&access_token=${accessToken}`;
      return this.http.get<any>(url);
    }

    exchangeFacebookToken(facebookToken: string) {
      const body = { facebookToken };
      const headers = new HttpHeaders().set('Content-Type', 'application/json');

      return this.http.post(this.urlPath+'auth/facebook', body, { headers });
    }

    loginWithFacebook(accessToken: string): Observable<any> {
      const headers = new HttpHeaders().set('Content-Type', 'application/json');
      const body = { access_token: accessToken };
      return this.http.post<any>(`${this.urlPath}login/facebook`, body, { headers });
    }




}
