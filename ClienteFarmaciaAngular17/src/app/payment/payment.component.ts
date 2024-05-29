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

@Component({
  selector: 'app-payment',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  providers: [DatePipe],
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

  categories: any[] = [];
  pharmacies: any[] = [];
  providers: any[] = [];


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

  html_template: any;

  fecha_compra = new Date()

  constructor(private router: Router, private route:ActivatedRoute, private crudProduct: CrudproductService, public fb: FormBuilder, private titleService: Title, private savePayment: SavepaymentService, private authService: AuthService, private datePipe: DatePipe) { }

  ngOnInit() {
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
    // this.html_template = document.getElementById('contentToConvert');
  }

  buyProduct(){
    // return this.savePayment.creditcardPayment()
  }

  backToCart(){
    this.router.navigate(['carrito/productos/lista']);
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



  export() {
    console.log('printing');
    const data = document.getElementById('pdfContent');
    data!.style.display = 'block';
    this.generatePDF(data);
    data!.style.display = 'none';
  }

  generatePDF(htmlContent: any) {
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
        let date_compra = this.datePipe.transform(this.fecha_compra, 'yyyy-MM-dd')
        pdf.save(`PSurPharmacy_${this.authService.getNamePicture().name}_${date_compra}.pdf`);
    });
  }

}