import { Component } from '@angular/core';
import { RouterModule, RouterLink, Router, Routes } from '@angular/router';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.scss'
})

export class FooterComponent {

  constructor(private router: Router){}

}
