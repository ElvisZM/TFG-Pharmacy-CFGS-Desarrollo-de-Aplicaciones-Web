import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PoliticaDevolucionesComponent } from './politica-devoluciones.component';

describe('PoliticaDevolucionesComponent', () => {
  let component: PoliticaDevolucionesComponent;
  let fixture: ComponentFixture<PoliticaDevolucionesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PoliticaDevolucionesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PoliticaDevolucionesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
