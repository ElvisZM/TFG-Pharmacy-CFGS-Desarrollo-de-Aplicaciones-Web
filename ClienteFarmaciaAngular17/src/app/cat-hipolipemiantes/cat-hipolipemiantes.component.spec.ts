import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CatHipolipemiantesComponent } from './cat-hipolipemiantes.component';

describe('CatHipolipemiantesComponent', () => {
  let component: CatHipolipemiantesComponent;
  let fixture: ComponentFixture<CatHipolipemiantesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CatHipolipemiantesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CatHipolipemiantesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
