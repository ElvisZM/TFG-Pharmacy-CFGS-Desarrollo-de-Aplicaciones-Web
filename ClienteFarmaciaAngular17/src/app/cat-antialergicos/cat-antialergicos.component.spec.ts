import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CatAntialergicosComponent } from './cat-antialergicos.component';

describe('CatAntialergicosComponent', () => {
  let component: CatAntialergicosComponent;
  let fixture: ComponentFixture<CatAntialergicosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CatAntialergicosComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CatAntialergicosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
