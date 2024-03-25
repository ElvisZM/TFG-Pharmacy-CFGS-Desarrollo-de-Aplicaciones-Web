import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})

export class DatosService {
  palabraBusqueda: string = '';
  idCuenta: string = '20862103';

  constructor(private http: HttpClient) { }

  getPopularMovies() {
    return this.http.get(`https://api.themoviedb.org/3/movie/popular?api_key=665eddc29536d1ffc4e5fdace47ae8c7`);
  }

  getTopRatedMovies(){
    return this.http.get('https://api.themoviedb.org/3/movie/top_rated?api_key=665eddc29536d1ffc4e5fdace47ae8c7');
  }

  getFilm(movie_id: number) {
    return this.http.get(`https://api.themoviedb.org/3/movie/${movie_id}?api_key=665eddc29536d1ffc4e5fdace47ae8c7`);
  }

  setPalabraBuscada(palabraObtenida: string) {
    this.palabraBusqueda = palabraObtenida;
  }

  getPalabraBuscada() {
    return this.palabraBusqueda;
  }

  getMovies(query: string) {
    const options = {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NjVlZGRjMjk1MzZkMWZmYzRlNWZkYWNlNDdhZThjNyIsInN1YiI6IjY1OGFiMzFiYjdiNjlkMDk2MjZkZTczOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Rufsppd2z4JY3JZaxJZDpC3FBWVswXCeqYoRkFl09ss'
      }
    }

    return this.http.get<any>(`https://api.themoviedb.org/3/search/movie?query=${query}`, options)
  }

  movieDetail(idMovie: number) {
    return this.http.get<any>('https://api.themoviedb.org/3/movie/' + idMovie + '?api_key=665eddc29536d1ffc4e5fdace47ae8c7&append_to_response=credits,reviews,recommendations');
  }


  getMyWatchlist(): Observable<any> {
    const options = {
      headers: {
        accept: 'application/json',
        Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NjVlZGRjMjk1MzZkMWZmYzRlNWZkYWNlNDdhZThjNyIsInN1YiI6IjY1OGFiMzFiYjdiNjlkMDk2MjZkZTczOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Rufsppd2z4JY3JZaxJZDpC3FBWVswXCeqYoRkFl09ss'
      }
    };

    return this.http.get<any>('https://api.themoviedb.org/3/account/' + this.idCuenta + '/watchlist/movies?language=en-US&page=1&sort_by=created_at.asc', options)
  }


  addWatchlist(movieId: number): Observable<any> {
    const options = {
      headers: {
        accept: 'application/json',
        'content-type': 'application/json',
        Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NjVlZGRjMjk1MzZkMWZmYzRlNWZkYWNlNDdhZThjNyIsInN1YiI6IjY1OGFiMzFiYjdiNjlkMDk2MjZkZTczOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Rufsppd2z4JY3JZaxJZDpC3FBWVswXCeqYoRkFl09ss'
      }
    };
    const body = JSON.stringify({ media_type: 'movie', media_id: movieId, watchlist: true })


    return this.http.post<any>(`https://api.themoviedb.org/3/account/${this.idCuenta}/watchlist`, body, options)
  }


  deleteFromWatchlist(movieId: number): Observable<any> {
    const options = {
      headers: {
        accept: 'application/json',
        'content-type': 'application/json',
        Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NjVlZGRjMjk1MzZkMWZmYzRlNWZkYWNlNDdhZThjNyIsInN1YiI6IjY1OGFiMzFiYjdiNjlkMDk2MjZkZTczOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Rufsppd2z4JY3JZaxJZDpC3FBWVswXCeqYoRkFl09ss'
      }
    };

    const body = JSON.stringify({ media_type: 'movie', media_id: movieId, watchlist: false })

    return this.http.post<any>(`https://api.themoviedb.org/3/account/${this.idCuenta}/watchlist`, body, options)
  }


}
