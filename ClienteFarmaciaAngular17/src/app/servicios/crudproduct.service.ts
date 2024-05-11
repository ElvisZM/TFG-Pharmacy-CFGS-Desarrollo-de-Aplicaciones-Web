import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class CrudproductService {

  baseUrlProducts: string = 'http://127.0.0.1:8000/service/product/provider/'

  constructor(private http: HttpClient, private authService: AuthService ) {}

  saveProduct(formProductData: any){
    return this.http.post(this.baseUrlProducts + 'registrar/producto/formulario', formProductData, this.authService.getHeadersApiRequest()).
    pipe(
      catchError(error => {
        throw error;
      })
    );
  }

}
