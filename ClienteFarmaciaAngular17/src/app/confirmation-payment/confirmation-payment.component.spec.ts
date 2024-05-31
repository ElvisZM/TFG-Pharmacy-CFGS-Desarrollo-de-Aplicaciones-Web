import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConfirmationPaymentComponent } from './confirmation-payment.component';

describe('ConfirmationPaymentComponent', () => {
  let component: ConfirmationPaymentComponent;
  let fixture: ComponentFixture<ConfirmationPaymentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConfirmationPaymentComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ConfirmationPaymentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
