import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BuscadorSimpleComponent } from './buscador-simple.component';

describe('BuscadorSimpleComponent', () => {
  let component: BuscadorSimpleComponent;
  let fixture: ComponentFixture<BuscadorSimpleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BuscadorSimpleComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(BuscadorSimpleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
