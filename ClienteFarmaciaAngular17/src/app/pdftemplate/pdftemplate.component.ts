import { Component, ElementRef } from '@angular/core';

@Component({
  selector: 'app-pdftemplate',
  standalone: true,
  imports: [],
  templateUrl: './pdftemplate.component.html',
  styleUrl: './pdftemplate.component.scss'
})
export class PdftemplateComponent {
  pdfContentElement!: ElementRef;

}
