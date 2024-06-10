import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CatSuplementosComponent } from './cat-suplementos.component';

describe('CatSuplementosComponent', () => {
  let component: CatSuplementosComponent;
  let fixture: ComponentFixture<CatSuplementosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CatSuplementosComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CatSuplementosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
