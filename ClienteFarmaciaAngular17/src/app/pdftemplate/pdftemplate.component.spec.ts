import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PdftemplateComponent } from './pdftemplate.component';

describe('PdftemplateComponent', () => {
  let component: PdftemplateComponent;
  let fixture: ComponentFixture<PdftemplateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PdftemplateComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PdftemplateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
