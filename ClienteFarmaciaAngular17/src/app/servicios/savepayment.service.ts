import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { DatePipe } from '@angular/common';
import { AuthService } from './auth.service';
import { environment } from '../../environments/environment';


@Injectable({
  providedIn: 'root',
})
export class SavepaymentService {

  pdfStored: any;

  metodo_pago: string ="";

  nombre_cli: string = ""
  fecha_compra = new Date()
  date_compra = this.datePipe.transform(this.fecha_compra, 'yyyy-MM-dd')
  id_pedido: string = ""
  tipo_tarjeta: string = ""
  total_compra: number = 0;
  direccion_envio: string = '';
  municipio_provincia: string = '';
  telefono_farm: string = ''
  titular_card: string = '';
  cardNumber: string = '';

  idTransactionPayPal: string = ""
  paypalEmailTransaccion: string = ""

  private urlPowerAutomate = environment.powerAutomateFlujoEmail
  private urlPath = environment.apiSellsSubs

  private canAccessConfirmationPage = false;


  constructor(private http:HttpClient, private datePipe: DatePipe, private authService: AuthService) { }




  sendToPowerAutomate(base64data: string, carrito: any, paypal: boolean) {
    const httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'application/json',
        })
    };

    let info_compra = carrito

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

    return this.http.post(this.urlPowerAutomate, body, httpOptions).subscribe(response => {
      console.log('PDF enviado a Power Automate');
    }, error => {
      console.error('Error al enviar el PDF a Power Automate', error);
    });

  }


  savingData(usuario_id: number){
    const headers = this.authService.getHeadersApiRequest();

    if (this.metodo_pago === 'creditcard'){
      const body = {
        "fecha_compra": this.date_compra,
        "direccion_envio": this.direccion_envio.split(",")[0],
        "codigo_postal": this.direccion_envio.split(",")[this.direccion_envio.split(",").length-1],
        "municipio": this.municipio_provincia.split(",")[0],
        "provincia": this.municipio_provincia.split(",")[this.municipio_provincia.split(",").length-1],
        "total_pago": this.total_compra,
        "cliente": usuario_id,
        "carrito": this.id_pedido,
        "tipo_pago": this.metodo_pago,
        "titular_tarjeta": this.titular_card,
        "numero_tarjeta": this.cardNumber,
        "tipo_tarjeta": this.tipo_tarjeta,
        "fecha_pago": this.date_compra

      }
      return this.http.post(this.urlPath + 'save/payment', body, headers).subscribe(response =>{
        console.log(response)
      }, error => {
        console.log(error)
      })
  

    }else if (this.metodo_pago === 'paypal'){
      const body = {
        "fecha_compra": this.date_compra,
        "direccion_envio": this.direccion_envio.split(",")[0],
        "codigo_postal": this.direccion_envio.split(",")[this.direccion_envio.split(",").length-1],
        "municipio": this.municipio_provincia.split(",")[0],
        "provincia": this.municipio_provincia.split(",")[this.municipio_provincia.split(",").length-1],
        "total_pago": this.total_compra,
        "cliente": usuario_id,
        "carrito": this.id_pedido,
        "tipo_pago": this.metodo_pago,
        "id_transaccion": this.idTransactionPayPal,
        "email_transaccion": this.paypalEmailTransaccion,
        "fecha_pago": this.date_compra


      }

      return this.http.post(this.urlPath + 'save/payment', body, headers).subscribe(response =>{
        console.log(response)
      }, error => {
        console.log(error)
      })
  
    }else{
      console.log('Metodo de pago incorrecto')
      return ("error")
    }
    
  }


  allowAccessToConfirmationPage() {
    this.canAccessConfirmationPage = true;
  }

  clearAccessToConfirmationPage(){
    this.canAccessConfirmationPage = false;
  }

  getAccessToConfirmationPage(){
    return this.canAccessConfirmationPage;
  }

}
