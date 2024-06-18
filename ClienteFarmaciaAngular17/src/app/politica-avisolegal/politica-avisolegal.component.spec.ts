import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PoliticaAvisolegalComponent } from './politica-avisolegal.component';

describe('PoliticaAvisolegalComponent', () => {
  let component: PoliticaAvisolegalComponent;
  let fixture: ComponentFixture<PoliticaAvisolegalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PoliticaAvisolegalComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PoliticaAvisolegalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
