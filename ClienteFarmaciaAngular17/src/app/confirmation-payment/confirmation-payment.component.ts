import { Component } from '@angular/core';
import { SavepaymentService } from '../servicios/savepayment.service';
import { AuthService } from '../servicios/auth.service';

@Component({
  selector: 'app-confirmation-payment',
  standalone: true,
  imports: [],
  templateUrl: './confirmation-payment.component.html',
  styleUrl: './confirmation-payment.component.scss'
})
export class ConfirmationPaymentComponent {

  constructor(private savePayment:SavepaymentService, private authService: AuthService){}


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
