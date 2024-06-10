import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CatAntiacidosComponent } from './cat-antiacidos.component';

describe('CatAntiacidosComponent', () => {
  let component: CatAntiacidosComponent;
  let fixture: ComponentFixture<CatAntiacidosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CatAntiacidosComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CatAntiacidosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
