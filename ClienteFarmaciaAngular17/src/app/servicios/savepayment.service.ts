import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { DatePipe } from '@angular/common';


@Injectable({
  providedIn: 'root',
})
export class SavepaymentService {

  pdfStored: any;

  fecha_compra = new Date()
  date_compra = this.datePipe.transform(this.fecha_compra, 'yyyy-MM-dd')


  constructor(private http:HttpClient, private datePipe: DatePipe) { }




  sendToPowerAutomate(base64data: string) {
    const httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'application/json',
        })
    };

    const body = {
        pdf: base64data.split(',')[1]
    };

    return this.http.post('https://prod-96.westeurope.logic.azure.com/workflows/0c01bdb7788042218fdb91f60e2b3e4e/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=Dnz5oElTqQ6j6u4LcmuY5M_eaaQSI3cHWVO7KPxtRKU', body, httpOptions).subscribe(response => {
        console.log('PDF enviado a Power Automate');
    }, error => {
        console.error('Error al enviar el PDF a Power Automate', error);
    });
  }





}
