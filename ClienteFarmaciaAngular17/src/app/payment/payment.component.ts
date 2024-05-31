import { Component, DoCheck, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { FormBuilder,FormControl,FormGroup,Validators } from '@angular/forms';
import { CrudproductService } from '../servicios/crudproduct.service';
import { CommonModule, DatePipe } from '@angular/common';
import { Title } from '@angular/platform-browser';
import { SavepaymentService } from '../servicios/savepayment.service';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas'; 
import { AuthService } from '../servicios/auth.service';
import { CartInfoService } from '../servicios/cart-info.service';

@Component({
  selector: 'app-payment',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './payment.component.html',
  styleUrl: './payment.component.scss'
})
export class PaymentComponent implements OnInit{



  public FormPaymentProduct! : FormGroup;

  cardTitular: string = 'Nombre Titular'
  cardNumber: string = '0123 4567 8910 1112';
  expirationDate: string = '01/24';
  cvv: string = '123';


  payment_nombre_titular: string="";
  payment_numero_tarjeta: string="";
  payment_expiration: string="";
  payment_codigo_seguridad: string="";
  payment_direccion_envio: string="";
  payment_codigo_postal: string="";
  payment_municipio: string="";
  payment_provincia!: FormControl;

  selectedCiudadOption!: string;
  selectedProvinciaOption!: string;

  campoFormVacio: boolean = false;
  formVacioError: string = 'Por favor, rellene todos los campos.';

  carrito: any = {};

  provincias: Array<string> = [
  "Álava",
  "Albacete",
  "Alicante",
  "Almería",
  "Asturias",
  "Ávila",
  "Badajoz",
  "Baleares",
  "Barcelona",
  "Burgos",
  "Cáceres",
  "Cádiz",
  "Cantabria",
  "Castellón",
  "Ceuta",
  "Ciudad Real",
  "Córdoba",
  "Cuenca",
  "Gerona",
  "Granada",
  "Guadalajara",
  "Guipúzcoa",
  "Huelva",
  "Huesca",
  "Jaén",
  "La Coruña",
  "La Rioja",
  "Las Palmas",
  "León",
  "Lérida",
  "Lugo",
  "Madrid",
  "Málaga",
  "Melilla",
  "Murcia",
  "Navarra",
  "Orense",
  "Palencia",
  "Pontevedra",
  "Salamanca",
  "Segovia",
  "Sevilla",
  "Soria",
  "Tarragona",
  "Tenerife",
  "Teruel",
  "Toledo",
  "Valencia",
  "Valladolid",
  "Vizcaya",
  "Zamora",
  "Zaragoza"
  ]

  fecha_compra = new Date()
  date_compra = this.datePipe.transform(this.fecha_compra, 'yyyy-MM-dd')

  pdfStored: any;

  direccion_completa: string = '';

  constructor(private router: Router, private route:ActivatedRoute, private crudProduct: CrudproductService, public fb: FormBuilder, private titleService: Title, private savePayment: SavepaymentService, private authService: AuthService, private datePipe: DatePipe, private cartInfo: CartInfoService) { }

  ngOnInit() {
    this.loadCartInfo();
    this.titleService.setTitle('Confirmacion de Pago');



    this.FormPaymentProduct = this.fb.group({
      payment_nombre_titular:['', Validators.required],
      payment_numero_tarjeta:['', Validators.required],
      payment_expiration:['', Validators.required],
      payment_codigo_seguridad:['', Validators.required],
      payment_direccion_envio:['', Validators.required],
      payment_codigo_postal:['', Validators.required],
      payment_municipio:['', Validators.required],
      payment_provincia:[''],
    });

  }

  ngDoCheck(){
    if(this.FormPaymentProduct){
      this.emptyFieldsFunction();
    }
  }

  buyProduct(){
    // return this.savePayment.creditcardPayment()
  }


  loadCartInfo() {
    this.cartInfo.getCartInfo().subscribe(response => {
      this.carrito = response;

      console.log(this.carrito);      
    });
  }

  getSubTotal(){
    return +((this.carrito.total_carrito / 1.21)).toFixed(2)
  }

  getCosteEnvio(){
    return 2
  }

  getIVAimport(){
    return +((this.carrito.total_carrito / 1.21)*0.21).toFixed(2)
  }

  getTotalPrice(){
    return (this.carrito.total_carrito + this.getCosteEnvio()).toFixed(2)  
  }

  getPharmaInfo(){
    return {"nombre": this.carrito.productos[0].producto_id.farmacia_id.nombre_farm,
            "direccion": this.carrito.productos[0].producto_id.farmacia_id.direccion_farm,
            "telefono": this.carrito.productos[0].producto_id.farmacia_id.telefono_farm}
  }

  getCardNumberMasked(cardNumber: string): string {
    const cleanedCardNumber = cardNumber.replace(/\s/g, ''); // Elimina los espacios
    return cleanedCardNumber.slice(-4).padStart(cleanedCardNumber.length, '*');
  }

  getCardType(cardNumber: string): string {

    const cleanedCardNumber = cardNumber.replace(/[\s-]/g, '');

    const cardPatterns: { [key: string]: RegExp } = {
      'Amex': /^3[47][0-9]{13}$/,
      'MasterCard': /^5[1-5][0-9]{14}$/,
      'Visa': /^4[0-9]{12}(?:[0-9]{3})?$/,
      'Discover': /^6(?:011|5[0-9]{2})[0-9]{12}$/,
      'JCB': /^(?:2131|1800|35\d{3})\d{11}$/,
      'DinersClub': /^3(?:0[0-5]|[68][0-9])[0-9]{11}$/,
      'PayPal': /^99[0-9]{10}$/, // Número ficticio para PayPal, debes adaptar según tus necesidades
    };

    for (const [cardType, pattern] of Object.entries(cardPatterns)) {
      if (pattern.test(cleanedCardNumber)) {
        return cardType;
      }
    }
    return 'Unknown';
  }

  getAdressComplete(){
    let direccion = this.FormPaymentProduct.get('payment_direccion_envio')?.value.toString()
    let codigo_postal = this.FormPaymentProduct.get('payment_codigo_postal')?.value.toString()
    this.direccion_completa = `${direccion}, ${codigo_postal}`;
    return this.direccion_completa.toString();
  }

  getMunicipioProvincia(){
    let municipio = this.FormPaymentProduct.get('payment_municipio')?.value.toString()
    let provincia = this.FormPaymentProduct.get('payment_provincia')?.value.toString()
    return `${municipio}, ${provincia}`;
  }


  backToCart(){
    this.router.navigate(['carrito/productos/lista']);
  }



  emptyFieldsFunction(){
    let emptyField = false;

    if(this.FormPaymentProduct.get('payment_municipio')?.value === undefined ||
       this.FormPaymentProduct.get('payment_municipio')?.value === ""){
        emptyField=true;
    }

    Object.keys(this.FormPaymentProduct.controls).forEach(control => {
      if(this.FormPaymentProduct.get(control)?.value=== ''){
        emptyField = true;
      }else if(this.FormPaymentProduct.get(control)?.value=== null){
        emptyField = true;
      }
    })
    this.campoFormVacio = emptyField;
  }







  flipCard(){
    let card = document.getElementsByClassName('creditcard')[0]; 
    if (card) {
        if (card.classList.contains('flipped')) { 
            card.setAttribute('class', 'creditcard mt-4 ms-3');
        } else {
            card.setAttribute('class', 'creditcard flipped mt-4 ms-3'); 
        }
    }
  }

  onCardNumberInput(event: any): void {
    let cardNumberWithoutSpaces = event.target.value.replace(/\s/g, '');

    let formattedCardNumber = cardNumberWithoutSpaces.replace(/(\d{4})/g, '$1 ');

    this.cardNumber = formattedCardNumber;
  }

  onExpirationInput(event: any): void {
    let expirationDateInput = event.target.value;
    
    expirationDateInput = expirationDateInput.replace(/[^\d\/]/g, '');
    
    if (expirationDateInput.length === 2 && !expirationDateInput.includes('/')) {
        expirationDateInput += '/';
    }

    expirationDateInput = expirationDateInput.slice(0, 5);

    this.expirationDate = expirationDateInput;
  }

  addSlash(event: KeyboardEvent): void {
    let value = (event.target as HTMLInputElement).value;

    if (value.length === 2 && !isNaN(Number(event.key))) {
        value += '/';
        (event.target as HTMLInputElement).value = value;
        this.expirationDate = value;
        event.preventDefault();
    }
  }

  onCardTitularInput(event: any): void {
    let cardTitularInput = event.target.value;

    this.cardTitular = cardTitularInput;
  }

  onCardCvvInput(event: any): void {
    let cvvInput = event.target.value;

    this.cvv = cvvInput;
  }



  // export() {
  //   console.log('printing');
  //   const data = document.getElementById('pdfContent');
  //   data!.style.display = 'block';
  //   this.generatePDF(data);
  //   data!.style.display = 'none';
  // }

  // generatePDF(htmlContent: any) {
  //   html2canvas(htmlContent).then(canvas => {
  //       const imgWidth = 210;
  //       const pageHeight = 297;
  //       const imgHeight = canvas.height * imgWidth / canvas.width;
  //       let heightLeft = imgHeight;
  //       const pdf = new jsPDF('p', 'mm', 'a4');
  //       let position = 0;

  //       pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, position, imgWidth, imgHeight);
  //       heightLeft -= pageHeight;

  //       while (heightLeft >= 0) {
  //           position = heightLeft - imgHeight;
  //           pdf.addPage();
  //           pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, position, imgWidth, imgHeight);
  //           heightLeft -= pageHeight;
  //       }
  //       pdf.save(`PSurPharmacy_${this.authService.getNamePicture().name}_${this.date_compra}.pdf`);
  //   });
  // }


  export() {
    console.log('printing');
    this.getAdressComplete()
    const data = document.getElementById('pdfContent');
    data!.style.display = 'block';
    this.generateAndSendPDF(data);
    data!.style.display = 'none';
    this.router.navigate(['/confirmacion/pago'])
  }

  generateAndSendPDF(htmlContent: any) {
    html2canvas(htmlContent).then(canvas => {
      const imgWidth = 210;
      const pageHeight = 297;
      const imgHeight = canvas.height * imgWidth / canvas.width;
      let heightLeft = imgHeight;
      const pdf = new jsPDF('p', 'mm', 'a4');
      let position = 0;

      pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;

      while (heightLeft >= 0) {
          position = heightLeft - imgHeight;
          pdf.addPage();
          pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, position, imgWidth, imgHeight);
          heightLeft -= pageHeight;
      }

      // Convert the PDF to base64
      const pdfOutput = pdf.output('arraybuffer');
      const pdfBlob = new Blob([pdfOutput], { type: 'application/pdf' });
      const reader = new FileReader();
      reader.readAsDataURL(pdfBlob);
      reader.onloadend = () => {
          const base64data = reader.result as string;
          this.savePayment.sendToPowerAutomate(base64data);
      };

      this.savePayment.pdfStored = pdfBlob;
    });
  }

}