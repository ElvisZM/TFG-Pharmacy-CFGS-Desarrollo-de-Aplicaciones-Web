import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormproductupdateComponent } from './formproductupdate.component';

describe('FormproductupdateComponent', () => {
  let component: FormproductupdateComponent;
  let fixture: ComponentFixture<FormproductupdateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FormproductupdateComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(FormproductupdateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
