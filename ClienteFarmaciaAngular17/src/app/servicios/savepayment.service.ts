import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { DatePipe } from '@angular/common';
import { AuthService } from './auth.service';


@Injectable({
  providedIn: 'root',
})
export class SavepaymentService {

  pdfStored: any;

  nombre_cli: string = ""
  fecha_compra = new Date()
  date_compra = this.datePipe.transform(this.fecha_compra, 'yyyy-MM-dd')
  id_pedido: string = ""
  metodo_pago: string = ""
  total_compra: number = 0;
  direccion_envio: string = '';
  municipio_provincia: string = '';
  telefono_farm: string = ''


  constructor(private http:HttpClient, private datePipe: DatePipe, private authService: AuthService) { }




  sendToPowerAutomate(base64data: string, carrito: any, paypal: boolean) {
    const httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'application/json',
        })
    };

    let info_compra = carrito
    let paypal_payment: boolean = paypal

    // if (!paypal_payment){
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
    
    // }else{
    //   const body = {
    //     cliente: this.nombre_cli,
    //     correo_cliente: info_compra.usuario.email,
    //     fecha_compra: this.date_compra,
    //     numero_factura: info_compra.codigo_compra,
    //     cantidad_pagar: this.total_compra,
    //     direccion_envio: this.direccion_envio,
    //     municipio_provincia: this.municipio_provincia,
    //     nombre_farmacia: info_compra.productos[0].producto_id.farmacia_id.nombre_farm,
    //     direccion_farmacia: info_compra.productos[0].producto_id.farmacia_id.direccion_farm,
    //     telefono_farmacia: info_compra.productos[0].producto_id.farmacia_id.telefono_farm,
    //     pdf: base64data.split(',')[1]
    //   };

    //   return this.http.post('https://prod-96.westeurope.logic.azure.com/workflows/0c01bdb7788042218fdb91f60e2b3e4e/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=Dnz5oElTqQ6j6u4LcmuY5M_eaaQSI3cHWVO7KPxtRKU', body, httpOptions).subscribe(response => {
    //     console.log('PDF enviado a Power Automate');
    //   }, error => {
    //     console.error('Error al enviar el PDF a Power Automate', error);
    //   });

    // }

    
  }


  savingData(compra: any){
    const headers = this.authService.getHeadersApiRequest();
    const body = {
      "fecha_compra": this.date_compra,
      "direccion_envio": this.direccion_envio,
      "codigo_postal": this.codigo_postal,
      "municipio": this.municipio_provincia,
      "provincia": this.provincia,
      "total_pagar": this.total_compra,
      "cliente": compra.usuario.id,
      "carrito": this.id_pedido
    }
  }



}
