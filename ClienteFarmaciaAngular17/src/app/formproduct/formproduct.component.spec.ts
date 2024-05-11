import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormproductComponent } from './formproduct.component';

describe('FormproductComponent', () => {
  let component: FormproductComponent;
  let fixture: ComponentFixture<FormproductComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FormproductComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(FormproductComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
