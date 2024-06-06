import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';
import { environment } from '../../environments/environment';
import { DatePipe } from '@angular/common';

@Injectable({
  providedIn: 'root'
})

export class DatosService {
  palabraBusqueda: string = '';

  private urlPath = environment.apiUrlProductProviders

  successProductMessage: string = '';
  createProductMessage: boolean = false;

  errorProductMessage: string = '';
  errorCreateProductMessage: boolean = false;

  productCN!: number;

  fecha = new Date()
  date_today = this.datePipe.transform(this.fecha, 'yyyy-MM-dd')


  constructor(private http: HttpClient, private authService: AuthService, private datePipe: DatePipe) { }

  setPalabraBuscada(palabraObtenida: string) {
    this.palabraBusqueda = palabraObtenida;
  }

  getPalabraBuscada() {
    return this.palabraBusqueda;
  }

  getProductsList(): Observable<any> {
    const headers = this.authService.getHeadersInfoAPI()
    return this.http.get<any>(this.urlPath+'productos/list', headers)
  }

  getPharmaciesList(): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.urlPath+'farmacias/list', headers)
  }

  getProvidersList(): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.urlPath+'proveedores/list', headers)
  }

  getCategoriesList(): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.urlPath+'categorias/list', headers)
  }

  getProduct(cn_prod: number, cif_farm: string ): Observable<any> {
    const headers = this.authService.getHeadersInfoAPI()
    return this.http.get<any>(this.urlPath+'producto/'+cn_prod+'/'+cif_farm, headers)
  }

  getProductRecommended(cat_name: string): Observable<any> {
    const headers = this.authService.getHeadersInfoAPI()
    return this.http.get<any>(this.urlPath+'producto/recomendado/'+cat_name, headers)
  }

  simpleSearchProduct(palabraBuscada: string): Observable<any> {
    const headers = this.authService.getHeadersInfoAPI()
    return this.http.get<any>(this.urlPath+'productos/buscador/query/simple/'+palabraBuscada, headers)
  }

  getProvider(cn_prod: number): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.urlPath+'proveedor/'+cn_prod, headers)
  }

  helperGetCategoryIdbyName(cat_name: string): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.urlPath+'categoria/'+cat_name, headers)
  }

  helperGetCifProviderbyName(name: string): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.urlPath+'proveedor/'+name, headers)
  }

  helperGetCifPharmacybyName(name: string): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.urlPath+'farmacia/'+name, headers)
  }

}
