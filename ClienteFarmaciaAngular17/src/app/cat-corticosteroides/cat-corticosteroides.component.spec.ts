import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CatCorticosteroidesComponent } from './cat-corticosteroides.component';

describe('CatCorticosteroidesComponent', () => {
  let component: CatCorticosteroidesComponent;
  let fixture: ComponentFixture<CatCorticosteroidesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CatCorticosteroidesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CatCorticosteroidesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
