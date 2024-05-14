import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CrudproductService {

  private urlPath = environment.apiUrlProductProviders

  constructor(private http: HttpClient, private authService: AuthService ) {}

  saveProduct(formProductData: any){
    return this.http.post(this.urlPath + 'registrar/producto/formulario', formProductData, this.authService.getHeadersApiRequest()).
    pipe(
      catchError(error => {
        throw error;
      })
    );
  }


  updateProduct(formProductData: any, cn_prod: number){
    return this.http.put(this.urlPath + 'modificar/producto/'+cn_prod, formProductData, this.authService.getHeadersApiRequest()).
    pipe(
      catchError(error => {
        throw error;
      })
    );
  }

  deleteProduct(cn_prod: number, cif_farm: string){
    return this.http.delete(this.urlPath + 'eliminar/producto/'+cn_prod+'/'+cif_farm, this.authService.getHeadersApiRequest()).
    pipe(
      catchError(error => {
        throw error;
      })
    );
  }

}
