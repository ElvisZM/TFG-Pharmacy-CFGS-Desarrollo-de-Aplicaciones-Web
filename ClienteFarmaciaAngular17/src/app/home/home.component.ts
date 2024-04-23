import { Component, ChangeDetectionStrategy, inject } from '@angular/core';
import { TopVentasComponent } from '../top-ventas/top-ventas.component';
import { TypewriterService} from '../servicios/typewriter.service';
import { bootstrapApplication } from '@angular/platform-browser';
import 'zone.js';
import { map } from 'rxjs';
import { AsyncPipe } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [TopVentasComponent, AsyncPipe],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HomeComponent {

  titles = [', .', ', hoy y siempre.', ', cada paso del camino.'];

  private typewriterService = inject(TypewriterService);

  typedText$ = this.typewriterService
    .getTypewriterEffect(this.titles)
    .pipe(map((text) => text));

}

