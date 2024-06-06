import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';
import { AuthService } from './auth.service';
import { Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class ReviewsService {

  private urlPath = environment.apiSellsSubs

  constructor(private http: HttpClient, private authService: AuthService) { }

  createReview(reviewData: Object): Observable<any> {
  const headers = this.authService.getHeadersApiRequest();
  return this.http.post(this.urlPath + 'create/review' , reviewData, headers)
  }

  getProductReviews(product_id: number): Observable<any> {
    const headers = this.authService.getHeadersInfoAPI();
    return this.http.get(this.urlPath + 'product/review/'+product_id, headers)
  }



}
