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
    },500);
    google.accounts.id.disableAutoSelect();
  }

  getHeadersApiRequest() {
    let headers_vacio: any = {}
    let token: string = this.getTokenCookie();
    if(token) {
      return {
        headers : new HttpHeaders({
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
        })
      };
    }
    return headers_vacio;
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
        const rol = response.usuario.rol.toString();
        this.setUserRol(rol.toString())
        if (response.administrador){
          this.setNamePicture(response.usuario.first_name, response.administrador.profile_pic)

        }
        else if (response.gerente){
          this.setNamePicture(response.usuario.first_name, response.gerente.profile_pic)

        }
        else if (response.empleado){
          this.setNamePicture(response.usuario.first_name, response.empleado.profile_pic)

        }
        else{
          this.setNamePicture(response.usuario.first_name, response.cliente.profile_pic)

        }
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




}
