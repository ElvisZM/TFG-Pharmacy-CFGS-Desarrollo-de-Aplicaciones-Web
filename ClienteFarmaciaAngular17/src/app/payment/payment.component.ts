import { Component, ViewChild, ElementRef } from '@angular/core';
import IMask from 'imask';


@Component({
  selector: 'app-payment',
  standalone: true,
  imports: [],
  templateUrl: './payment.component.html',
  styleUrl: './payment.component.scss'
})
export class PaymentComponent {
  @ViewChild('name') nameInput: ElementRef;
  @ViewChild('cardnumber') cardNumberInput: ElementRef;
  @ViewChild('expirationdate') expirationDateInput: ElementRef;
  @ViewChild('securitycode') securityCodeInput: ElementRef;
  @ViewChild('ccicon') ccIcon: ElementRef;
  @ViewChild('ccsingle') ccSingle: ElementRef;

  ngOnInit() {
    // Tu código de inicialización aquí
  }

  ngAfterViewInit() {
    // Inicializa las máscaras de los campos de entrada
    this.initInputMasks();
  }

  initInputMasks() {
    // Inicializa las máscaras de los campos de entrada usando IMask
    const cardNumberMask = IMask(this.cardNumberInput.nativeElement, {
      mask: '0000 0000 0000 0000'
      // Otras configuraciones...
    });

    const expirationDateMask = IMask(this.expirationDateInput.nativeElement, {
      mask: 'MM{/}YY'
      // Otras configuraciones...
    });

    const securityCodeMask = IMask(this.securityCodeInput.nativeElement, {
      mask: '0000'
    });

    // Continúa con las máscaras para otros campos...
  }

  onFocusSecurityCode() {
    // Agrega la clase 'flipped' al contenedor de la tarjeta cuando el campo 'Security Code' está enfocado
    this.ccIcon.nativeElement.classList.add('flipped');
    this.ccSingle.nativeElement.classList.add('flipped');
  }

  onBlurSecurityCode() {
    // Elimina la clase 'flipped' del contenedor de la tarjeta cuando el campo 'Security Code' pierde el foco
    this.ccIcon.nativeElement.classList.remove('flipped');
    this.ccSingle.nativeElement.classList.remove('flipped');
  }

  // Implementa otras funciones de manejo de eventos y lógica aquí...
}