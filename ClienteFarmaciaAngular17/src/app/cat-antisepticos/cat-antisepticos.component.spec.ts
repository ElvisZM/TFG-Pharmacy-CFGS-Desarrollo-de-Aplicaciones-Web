import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CatAntisepticosComponent } from './cat-antisepticos.component';

describe('CatAntisepticosComponent', () => {
  let component: CatAntisepticosComponent;
  let fixture: ComponentFixture<CatAntisepticosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CatAntisepticosComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CatAntisepticosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
