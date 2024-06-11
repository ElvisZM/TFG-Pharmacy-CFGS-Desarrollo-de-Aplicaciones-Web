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
  private APITokenNoLoggedIn = environment.APITokenNoLoggedIn

  private urlPath = environment.apiUrlAuthUsers;

  constructor(private http: HttpClient, private cookies: CookieService, private router: Router) { }


  setTokenCookie(token:string){
    this.cookies.set("token",token, {path: '/' });
  }

  getTokenCookie(){
    const token: string = this.cookies.get("token");
    return token;
  }

  setNamePicture(name:string, picture_url?:string){
    this.cookies.set("name",name, {path: '/' });
    if (picture_url){
      this.cookies.set("picture_url", picture_url, {path: '/' });
    }
  }

  getNamePicture(){
    const name:string = this.cookies.get("name");
    const picture:string = this.cookies.get("picture_url");
    return {name, picture};
  }

  setUserRol(rol: string){
    this.cookies.set("user_rol", rol, {path: '/' })
  }

  getUserRol(){
    const rol: string = this.cookies.get("user_rol");
    return rol
  }

  setSource(source:string){
    this.cookies.set("source", source, {path: '/' });
  }

  getSource(){
    const source = this.cookies.get("source");
    return source
  }


  logout() {
    function deleteCookie(name: string) {
      document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;';
    }
  
    const cookiesToDelete = ["token", "name", "picture_url", "user_rol", "source"];
  
    cookiesToDelete.forEach(cookie => deleteCookie(cookie));
  
    google.accounts.id.disableAutoSelect();
  
    this.router.navigate(['/']).then(() => {
      window.location.reload();
    });
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


  getHeadersInfoAPIProbando(){
    return this.APITokenNoLoggedIn
  }


  getHeadersInfoAPI(){
    return {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${this.APITokenNoLoggedIn}`
      })
    }
  }

  getUserInfo(){
    const headers = this.getHeadersUserInfo();
    return this.http.get<any>(this.urlPath+'usuario/token/'+this.getTokenCookie(), headers).subscribe(
      response => {
        const rol = response.usuario.rol.toString();
        this.setUserRol(rol.toString())
        
        if (response.administrador){
          console.log("hola admin")
          this.setNamePicture(response.usuario.first_name, response.administrador.profile_pic)
          this.setSource(response.administrador.source)
        }
        else if (response.gerente){
          this.setNamePicture(response.usuario.first_name, response.gerente.profile_pic)
          this.setSource(response.gerente.source)

        }
        else if (response.empleado){
          this.setNamePicture(response.usuario.first_name, response.empleado.profile_pic)
          this.setSource(response.empleado.source)

        }
        else{
          this.setNamePicture(response.usuario.first_name, response.cliente.profile_pic)
          this.setSource(response.cliente.source)

        }
      },error => {
        console.log("no hay usuario")
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
