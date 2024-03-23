import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TopVentasComponent } from './top-ventas.component';

describe('TopVentasComponent', () => {
  let component: TopVentasComponent;
  let fixture: ComponentFixture<TopVentasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TopVentasComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TopVentasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
