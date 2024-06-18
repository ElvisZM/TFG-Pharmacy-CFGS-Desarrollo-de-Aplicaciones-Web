import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PoliticaTerminoscondicionesComponent } from './politica-terminoscondiciones.component';

describe('PoliticaTerminoscondicionesComponent', () => {
  let component: PoliticaTerminoscondicionesComponent;
  let fixture: ComponentFixture<PoliticaTerminoscondicionesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PoliticaTerminoscondicionesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PoliticaTerminoscondicionesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
