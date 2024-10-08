import { Component, OnDestroy, OnInit } from '@angular/core';
import { SavepaymentService } from '../servicios/savepayment.service';
import { AuthService } from '../servicios/auth.service';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-confirmation-payment',
  standalone: true,
  imports: [],
  templateUrl: './confirmation-payment.component.html',
  styleUrl: './confirmation-payment.component.scss'
})
export class ConfirmationPaymentComponent implements OnInit, OnDestroy {

  nombre_cliente: string = "";
  fecha_compra: any;
  numero_pedido: string = "";
  tipo_tarjeta: string = "";
  address: string = "";
  telefono: string = "";

  constructor(private savePayment:SavepaymentService, private authService: AuthService, private titleService: Title){}

  ngOnInit(): void {
    this.getData();
    this.titleService.setTitle('Confirmación de pago');

  }

  ngOnDestroy(): void {
    this.savePayment.clearAccessToConfirmationPage();

  }

  getData(){
    this.nombre_cliente = this.savePayment.nombre_cli
    this.fecha_compra = this.savePayment.date_compra
    this.numero_pedido = this.savePayment.id_pedido
    this.tipo_tarjeta = this.savePayment.tipo_tarjeta
    this.address = this.savePayment.direccion_envio + ", " + this.savePayment.municipio_provincia
    this.telefono = this.savePayment.telefono_farm
  }

  downloadPDF() {
    if (this.savePayment.pdfStored) {
        const pdfUrl = URL.createObjectURL(this.savePayment.pdfStored);
        const link = document.createElement('a');
        link.href = pdfUrl;
        link.download = `PSurPharmacy_${this.authService.getNamePicture().name}_${this.savePayment.date_compra}.pdf`;
        link.click();
        
    } else {
        console.error('No PDF available for download');
    }
  }


}
