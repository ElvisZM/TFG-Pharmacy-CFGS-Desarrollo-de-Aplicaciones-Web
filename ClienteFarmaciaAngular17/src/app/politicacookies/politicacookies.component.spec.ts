import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PoliticacookiesComponent } from './politicacookies.component';

describe('PoliticacookiesComponent', () => {
  let component: PoliticacookiesComponent;
  let fixture: ComponentFixture<PoliticacookiesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PoliticacookiesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PoliticacookiesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
