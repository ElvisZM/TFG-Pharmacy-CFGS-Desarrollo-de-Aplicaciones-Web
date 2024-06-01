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
  total_compra: number = 0;
  direccion_envio: string = '';
  municipio_provincia: string = '';

  constructor(private http:HttpClient, private datePipe: DatePipe) { }




  sendToPowerAutomate(base64data: string, carrito: any) {
    const httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'application/json',
        })
    };

    let info_compra = carrito
  //   "cliente": {
  //     "type": "string"
  // },
  // "fecha_compra": {
  //     "type": "string"
  // },
  // "numero_factura": {
  //     "type": "string"
  // },
  // "cantidad_pagar": {
  //     "type": "number"
  // },
  // "direccion_envio": {
  //     "type": "string"
  // },
  // "nombre_farmacia": {
  //     "type": "string"
  // },
  // "direccion_farmacia": {
  //     "type": "string"
  // },
  // "telefono_farmacia": {
  //     "type": "number"
  // },
  // "pdf": {
  //     "type": "string"
  // }


    const body = {
        cliente: info_compra.usuario.first_name + " " + info_compra.usuario.last_name,
        correo_cliente: info_compra.usuario.email,
        fecha_compra: this.date_compra,
        numero_factura: info_compra.codigo_compra,
        cantidad_pagar: this.total_compra,
        direccion_envio: this.direccion_envio,
        municipio_provincia: this.municipio_provincia,
        nombre_farmacia: info_compra.productos[0].producto_id.farmacia_id.nombre_farm,
        direccion_farmacia: info_compra.productos[0].producto_id.farmacia_id.direccion_farm,
        telefono_farmacia: info_compra.productos[0].producto_id.farmacia_id.telefono_farm,
        pdf: base64data.split(',')[1]
    };

    return this.http.post('https://prod-96.westeurope.logic.azure.com/workflows/0c01bdb7788042218fdb91f60e2b3e4e/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=Dnz5oElTqQ6j6u4LcmuY5M_eaaQSI3cHWVO7KPxtRKU', body, httpOptions).subscribe(response => {
        console.log('PDF enviado a Power Automate');
    }, error => {
        console.error('Error al enviar el PDF a Power Automate', error);
    });
  }





}
