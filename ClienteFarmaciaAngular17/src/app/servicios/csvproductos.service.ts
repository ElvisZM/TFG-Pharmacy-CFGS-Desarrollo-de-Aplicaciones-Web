import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs';
import { AuthService } from './auth.service';
import * as Papa from 'papaparse';
import { map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class CsvproductosService {

  name: string = '';
  email: string = '';
  city: string = '';

  urlSaveDataBackend: string = 'http://127.0.0.1:8000/service/product/provider/registrar/producto/csv'


  constructor(private http:HttpClient, private authService: AuthService){}

  public saveDataInCSV(data: Array<any>): string {
    if (data.length == 0) {
      return '';
    }

    let propertyNames = Object.keys(data[0]);
    let rowWithPropertyNames = propertyNames.join(',') + '\n';

    let csvContent = rowWithPropertyNames;

    let rows: string[] = [];

    data.forEach((item) => {
      let values: string[] = [];

      propertyNames.forEach((key) => {
        let val: any = item[key];

        if (val !== undefined && val !== null) {
          val = new String(val);
        } else {
          val = '';
        }
        values.push(val);
      });
      rows.push(values.join(','));
    });
    csvContent += rows.join('\n');

    return csvContent;
  }

  public importDataFromCSV(csvText: string): Array<any> {
    const parsedData = Papa.parse(csvText, { header: true });
    return parsedData.data;
    // const propertyNames = csvText.slice(0, csvText.indexOf('\n')).split(',');
    // const dataRows = csvText.slice(csvText.indexOf('\n') + 1).split('\n');

    // let dataArray: any[] = [];
    // dataRows.forEach((row) => {
    //   let values = row.split(',');

    //   let obj: any = new Object();

    //   for (let index = 0; index < propertyNames.length; index++) {
    //     const propertyName: string = propertyNames[index];

    //     let val: any = values[index];
    //     if (val === '') {
    //       val = null;
    //     }

    //     obj[propertyName] = val;
    //   }

    //   dataArray.push(obj);
    // });

    // return dataArray;
  }

  saveDataBackend(data: any): Observable<any> {
    return this.http.post<any>(this.urlSaveDataBackend, data, this.authService.getHeadersApiRequest())
    .pipe(
      map(response => {
        const server_response = response
        if (server_response.toString() === 'Producto CREADO'){;
          console.log(response);
          console.log("HOLA")
        }else{
          console.log(response);
        }
      }),
        catchError(error => {
          throw error;
        })
      );
  }     

}
