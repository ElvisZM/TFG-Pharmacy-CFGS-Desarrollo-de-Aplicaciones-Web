import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';


@Injectable({
  providedIn: 'root'
})

export class DatosService {
  palabraBusqueda: string = '';
  // idCuenta: string = '20862103';

  apiURL: string = 'http://127.0.0.1:8000/service/';


  successProductMessage: string = '';
  createProductMessage: boolean = false;

  errorProductMessage: string = '';
  errorCreateProductMessage: boolean = false;

  productCN!: number;

  constructor(private http: HttpClient, private authService: AuthService) { }

  // getPopularMovies() {
  //   return this.http.get(`https://api.themoviedb.org/3/movie/popular?api_key=665eddc29536d1ffc4e5fdace47ae8c7`);
  // }

  // getTopRatedMovies(){
  //   return this.http.get('https://api.themoviedb.org/3/movie/top_rated?api_key=665eddc29536d1ffc4e5fdace47ae8c7');
  // }

  // getFilm(movie_id: number) {
  //   return this.http.get(`https://api.themoviedb.org/3/movie/${movie_id}?api_key=665eddc29536d1ffc4e5fdace47ae8c7`);
  // }

  setPalabraBuscada(palabraObtenida: string) {
    this.palabraBusqueda = palabraObtenida;
  }

  getPalabraBuscada() {
    return this.palabraBusqueda;
  }

  // getMovies(query: string) {
  //   const options = {
  //     method: 'GET',
  //     headers: {
  //       'Accept': 'application/json',
  //       'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NjVlZGRjMjk1MzZkMWZmYzRlNWZkYWNlNDdhZThjNyIsInN1YiI6IjY1OGFiMzFiYjdiNjlkMDk2MjZkZTczOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Rufsppd2z4JY3JZaxJZDpC3FBWVswXCeqYoRkFl09ss'
  //     }
  //   }

  //   return this.http.get<any>(`https://api.themoviedb.org/3/search/movie?query=${query}`, options)
  // }

  // movieDetail(idMovie: number) {
  //   return this.http.get<any>('https://api.themoviedb.org/3/movie/' + idMovie + '?api_key=665eddc29536d1ffc4e5fdace47ae8c7&append_to_response=credits,reviews,recommendations');
  // }


  // getMyWatchlist(): Observable<any> {
  //   const options = {
  //     headers: {
  //       accept: 'application/json',
  //       Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NjVlZGRjMjk1MzZkMWZmYzRlNWZkYWNlNDdhZThjNyIsInN1YiI6IjY1OGFiMzFiYjdiNjlkMDk2MjZkZTczOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Rufsppd2z4JY3JZaxJZDpC3FBWVswXCeqYoRkFl09ss'
  //     }
  //   };

  //   return this.http.get<any>('https://api.themoviedb.org/3/account/' + this.idCuenta + '/watchlist/movies?language=en-US&page=1&sort_by=created_at.asc', options)
  // }


  // addWatchlist(movieId: number): Observable<any> {
  //   const options = {
  //     headers: {
  //       accept: 'application/json',
  //       'content-type': 'application/json',
  //       Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NjVlZGRjMjk1MzZkMWZmYzRlNWZkYWNlNDdhZThjNyIsInN1YiI6IjY1OGFiMzFiYjdiNjlkMDk2MjZkZTczOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Rufsppd2z4JY3JZaxJZDpC3FBWVswXCeqYoRkFl09ss'
  //     }
  //   };
  //   const body = JSON.stringify({ media_type: 'movie', media_id: movieId, watchlist: true })


  //   return this.http.post<any>(`https://api.themoviedb.org/3/account/${this.idCuenta}/watchlist`, body, options)
  // }


  // deleteFromWatchlist(movieId: number): Observable<any> {
  //   const options = {
  //     headers: {
  //       accept: 'application/json',
  //       'content-type': 'application/json',
  //       Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NjVlZGRjMjk1MzZkMWZmYzRlNWZkYWNlNDdhZThjNyIsInN1YiI6IjY1OGFiMzFiYjdiNjlkMDk2MjZkZTczOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Rufsppd2z4JY3JZaxJZDpC3FBWVswXCeqYoRkFl09ss'
  //     }
  //   };

  //   const body = JSON.stringify({ media_type: 'movie', media_id: movieId, watchlist: false })

  //   return this.http.post<any>(`https://api.themoviedb.org/3/account/${this.idCuenta}/watchlist`, body, options)
  // }

  getProductsList(): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.apiURL+'product/provider/productos/list', headers)
  }

  getPharmaciesList(): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.apiURL+'product/provider/farmacias/list', headers)
  }

  getProvidersList(): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.apiURL+'product/provider/proveedores/list', headers)
  }

  getCategoriesList(): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.apiURL+'product/provider/categorias/list', headers)
  }

  getProduct(cn_prod: number ): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.apiURL+'product/provider/producto/'+cn_prod, headers)
  }

  getProvider(cn_prod: number): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.apiURL+'product/provider/proveedor/'+cn_prod, headers)
  }

  helperGetCategoryIdbyName(cat_name: string): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.apiURL+'product/provider/categoria/'+cat_name, headers)
  }

  helperGetCifProviderbyName(name: string): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.apiURL+'product/provider/proveedor/'+name, headers)
  }

  helperGetCifPharmacybyName(name: string): Observable<any> {
    const headers = this.authService.getHeadersUserInfo()
    return this.http.get<any>(this.apiURL+'product/provider/farmacia/'+name, headers)
  }


}
