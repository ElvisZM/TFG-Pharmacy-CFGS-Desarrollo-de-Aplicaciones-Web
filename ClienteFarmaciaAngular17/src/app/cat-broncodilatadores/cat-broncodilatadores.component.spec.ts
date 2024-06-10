import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CatBroncodilatadoresComponent } from './cat-broncodilatadores.component';

describe('CatBroncodilatadoresComponent', () => {
  let component: CatBroncodilatadoresComponent;
  let fixture: ComponentFixture<CatBroncodilatadoresComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CatBroncodilatadoresComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CatBroncodilatadoresComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
