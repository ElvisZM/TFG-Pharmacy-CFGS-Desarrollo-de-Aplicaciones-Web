import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CatAnalgesicosComponent } from './cat-analgesicos.component';

describe('CatAnalgesicosComponent', () => {
  let component: CatAnalgesicosComponent;
  let fixture: ComponentFixture<CatAnalgesicosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CatAnalgesicosComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CatAnalgesicosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
