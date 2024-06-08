import { Component, DoCheck, OnInit, ViewChild, ElementRef, AfterViewInit, ChangeDetectorRef } from '@angular/core';
import { Router, ActivatedRoute, RouterLink, NavigationEnd } from '@angular/router';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { FormBuilder,FormControl,FormGroup,Validators } from '@angular/forms';
import { CrudproductService } from '../servicios/crudproduct.service';
import { CommonModule, DatePipe, ViewportScroller } from '@angular/common';
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

  direccion_completa!: string;

  @ViewChild('paymentPayPal') paymentPayPal!: ElementRef;

  showPayPal: boolean = false;
  total_price: string="";
  PayPalData: boolean = false;
  PayPalIdTransaction: string = "";
  PayPalEmailTransaction: string = "";
  PayPalClientName: string = "";
  PayPalShippingAddress: string = "";
  PayPalMunicipioProvincia: string= "";

  constructor(private router: Router, private route:ActivatedRoute, private crudProduct: CrudproductService, public fb: FormBuilder, private titleService: Title, private savePayment: SavepaymentService, private authService: AuthService, private datePipe: DatePipe, private cartInfo: CartInfoService, private changeDetector: ChangeDetectorRef, private viewportScroller: ViewportScroller) { }

  ngOnInit() {

    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.viewportScroller.scrollToPosition([0, 0]);
      }
    });
    

    this.titleService.setTitle('Metodo de Pago');
    this.cartInfo.getCartInfo().subscribe(response => {

      this.carrito = response;
      this.total_price = (this.carrito.total_carrito + this.getCosteEnvio()).toFixed(2).toString()
    });

    this.initializeForm();

  }

  ngAfterViewInit() {
    if (this.paymentPayPal) {
      window.paypal.Buttons(
        {
          style: {
            layout: 'horizontal',
            color: 'blue',
            shape: 'rect',
            label: 'paypal'
          },
          createOrder: (data: any, actions: any) => {
            return actions.order.create({
              purchase_units: [
                {
                  amount: {
                    value: this.total_price,
                    currency_code: "EUR"
                  }
                }
              ]
            })
          },
          onApprove: (data: any, actions: any) => {
            return actions.order.capture().then((details: any) => {
              this.PayPalData = true;
              console.log(details);
              this.PayPalIdTransaction = details.id
              this.savePayment.idTransactionPayPal = this.PayPalIdTransaction
              this.PayPalEmailTransaction = details.payer.email_address
              this.savePayment.paypalEmailTransaccion = this.PayPalEmailTransaction
              this.PayPalClientName = details.payer.name.given_name + " " + details.payer.name.surname
              this.PayPalShippingAddress = details.purchase_units[0].shipping.address.address_line_1 + ", " + details.purchase_units[0].shipping.address.postal_code
              this.PayPalMunicipioProvincia = details.purchase_units[0].shipping.address.admin_area_1 + ", " + details.purchase_units[0].shipping.address.admin_area_2

              this.changeDetector.detectChanges();
              this.buyProductPayPal();
              
            });
          },
          onError: (error: any) => {
            console.error(error);
          }
        }
      ).render(this.paymentPayPal.nativeElement);
    } else {
      console.error('paymentPayPal is undefined');
    }
  }

  ngDoCheck(){
    if(this.FormPaymentProduct){
      this.emptyFieldsFunction();
    }
    
  }


  initializeForm(): void {
    this.FormPaymentProduct = this.fb.group({
      payment_nombre_titular:['', Validators.required],
      payment_numero_tarjeta:['', Validators.required],
      payment_expiration:['', Validators.required],
      payment_codigo_seguridad:['', Validators.required],
      payment_direccion_envio:['', Validators.required],
      payment_codigo_postal:['', Validators.required],
      payment_municipio:['', Validators.required],
      payment_provincia:[''],
    }, {validator: this.formValidator});
  }
  
  formValidator = (formGroup: FormGroup) => {
    const titular = formGroup.get('payment_nombre_titular')?.value;
    const numeroTarjeta = formGroup.get('payment_numero_tarjeta')?.value;
    const expiration = formGroup.get('payment_expiration')?.value;
    const cvv = formGroup.get('payment_codigo_seguridad')?.value;
    const codigo_postal = formGroup.get('payment_codigo_postal')?.value
    const municipio = formGroup.get('payment_municipio')?.value

    if (!/^[a-zA-Z\s]+$/.test(titular)) {
        formGroup.get('payment_nombre_titular')?.setErrors({ invalidTitularName: true });
    } else {
        formGroup.get('payment_nombre_titular')?.setErrors(null);
    }

    if (numeroTarjeta.length == 16){
      const cardType = this.getCardType(numeroTarjeta);
      if (cardType === 'Unknown') {
          formGroup.get('payment_numero_tarjeta')?.setErrors({ invalidCardType: true });
      } else {
          formGroup.get('payment_numero_tarjeta')?.setErrors(null);
      }
  
    }else{
      formGroup.get('payment_numero_tarjeta')?.setErrors({invalidCardType: true});
    }
    

    const [mes, año] = expiration.split('/');
    if (!mes || !año || isNaN(+mes) || isNaN(+año) || mes.length !== 2 || año.length !== 2) {
      formGroup.get('payment_expiration')?.setErrors({fechaCaducidadInvalida: true});
    } else {
      const mesNum = parseInt(mes, 10);
      if (mesNum > 12 || mesNum < 1) {
        formGroup.get('payment_expiration')?.setErrors({fechaCaducidadInvalida: true});
      }else{
        const añoNum = parseInt(`20${año}`, 10);
        const fechaActual = new Date();
        const fechaTarjeta = new Date(añoNum, mesNum - 1);
        if (fechaTarjeta < fechaActual) {
          formGroup.get('payment_expiration')?.setErrors({fechaCaducidadInvalida: true});
        }else{
          formGroup.get('payment_expiration')?.setErrors(null);
        }
      }
    }

    if (!/^\d{3}$/.test(cvv)) {
      formGroup.get('payment_codigo_seguridad')?.setErrors({cvvInvalido: true});
    }else{
      formGroup.get('payment_codigo_seguridad')?.setErrors(null);
    }


    if (!/^\d{5}$/.test(codigo_postal)) {
      formGroup.get('payment_codigo_postal')?.setErrors({cpInvalido: true});
    }else{
      formGroup.get('payment_codigo_postal')?.setErrors(null);
    }

    if (!/^[a-zA-Z\s]+$/.test(municipio)) {
      formGroup.get('payment_municipio')?.setErrors({ municipioInvalido: true });
  } else {
      formGroup.get('payment_municipio')?.setErrors(null);
  }

  }




  buyProductPayPal(): void{
    this.savePayment.nombre_cli = this.PayPalClientName
    this.savePayment.id_pedido = this.carrito.codigo_compra
    this.savePayment.metodo_pago = 'paypal'
    this.savePayment.tipo_tarjeta = 'PayPal'
    this.savePayment.direccion_envio = this.PayPalShippingAddress
    this.savePayment.municipio_provincia = this.PayPalMunicipioProvincia
    this.savePayment.telefono_farm = this.getPharmaInfo().telefono
    const data = document.getElementById('pdfContent');
    data!.style.display = 'block';
    this.generateAndSendPDF(data);
    data!.style.display = 'none';
    this.savePayment.savingData(this.carrito.usuario.id);
    this.router.navigate(['/confirmacion/pago'])

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
    this.savePayment.total_compra = +((this.carrito.total_carrito + this.getCosteEnvio()).toFixed(2));
    return this.savePayment.total_compra
  }
  getPharmaInfo() {
    if (this.carrito && this.carrito.productos && this.carrito.productos.length > 0) {
        return {
            "nombre": this.carrito.productos[0].producto_id.farmacia_id.nombre_farm,
            "direccion": this.carrito.productos[0].producto_id.farmacia_id.direccion_farm,
            "telefono": this.carrito.productos[0].producto_id.farmacia_id.telefono_farm
        };
    } else {
        return {};
    }
}
    
  getCardNumberMasked(cardNumber: string): string {
    const cleanedCardNumber = cardNumber.replace(/\s/g, '');
    this.savePayment.cardNumber = cleanedCardNumber;
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
    };

    for (const [cardType, pattern] of Object.entries(cardPatterns)) {
      if (pattern.test(cleanedCardNumber)) {
        this.savePayment.tipo_tarjeta = cardType
        return cardType;
      }
    }
    return 'Unknown';
  }

  getAdressComplete(){
    let direccion = this.FormPaymentProduct.get('payment_direccion_envio')?.value.toString();
    let codigo_postal = this.FormPaymentProduct.get('payment_codigo_postal')?.value.toString();
    let adress = `${direccion}, ${codigo_postal}`;
    this.savePayment.direccion_envio = adress;

    return adress;
  }

  getPostalCode(){
    return this.FormPaymentProduct.get('payment_codigo_postal')?.value.toString();
  }

  getMunicipioProvincia(){
    let municipio = this.FormPaymentProduct.get('payment_municipio')?.value.toString()
    let provincia = this.FormPaymentProduct.get('payment_provincia')?.value.toString()
    let muni_prov = `${municipio}, ${provincia}`;
    this.savePayment.municipio_provincia = muni_prov;
    return muni_prov;
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

    const parts = expirationDateInput.split('/');
    let beforeSlash = parts[0].slice(0, 2);
    let afterSlash = parts.length > 1 ? parts[1].slice(0, 2) : '';
    
    expirationDateInput = beforeSlash + (afterSlash ? '/' + afterSlash : ''); 

    if (expirationDateInput.length === 2 && expirationDateInput.charAt(1) !== '/') {
      expirationDateInput += '/';
    }

    this.FormPaymentProduct.patchValue({ 'payment_expiration': expirationDateInput }); 

    this.expirationDate = expirationDateInput;
  }

  onCardTitularInput(event: any): void {
    let cardTitularInput = event.target.value;
    this.savePayment.titular_card = cardTitularInput;
    this.cardTitular = cardTitularInput;
  }

  onCardCvvInput(event: any): void {
    let cvvInput = event.target.value;

    this.cvv = cvvInput;
  }

  showCreditCardMethod(){
    let pp = document.getElementById('pp')
    pp?.setAttribute('class', 'd-none')
    this.showPayPal = false;
  }

  showPayPalMethod(){
    let pp = document.getElementById('pp')
    pp?.setAttribute('class', 'd-block')
    this.showPayPal = true;
  }

  buyProductCreditCard() {
    
    let num_tarjeta = this.FormPaymentProduct.get('payment_numero_tarjeta')?.value


    this.savePayment.nombre_cli = this.carrito.cliente.usuario.first_name + ' ' + this.carrito.cliente.usuario.last_name
    this.savePayment.id_pedido = this.carrito.codigo_compra
    this.savePayment.metodo_pago = "creditcard"
    this.savePayment.telefono_farm = this.getPharmaInfo().telefono
    const data = document.getElementById('pdfContent');
    data!.style.display = 'block';
    this.generateAndSendPDF(data);
    data!.style.display = 'none';
    this.savePayment.savingData(this.carrito.usuario.id);
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

      const pdfOutput = pdf.output('arraybuffer');
      const pdfBlob = new Blob([pdfOutput], { type: 'application/pdf' });
      const reader = new FileReader();
      reader.readAsDataURL(pdfBlob);
      reader.onloadend = () => {
          const base64data = reader.result as string;
          // this.savePayment.sendToPowerAutomate(base64data, this.carrito, this.PayPalData);
      };

      this.savePayment.pdfStored = pdfBlob;
    });
  }

}