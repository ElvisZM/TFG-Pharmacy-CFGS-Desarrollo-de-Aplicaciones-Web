import { Component, DoCheck, OnInit } from '@angular/core';
import { Router, ActivatedRoute, RouterLink, NavigationEnd } from '@angular/router';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { FormBuilder,FormControl,FormGroup,Validators } from '@angular/forms';
import { CrudproductService } from '../servicios/crudproduct.service';
import { CommonModule, ViewportScroller } from '@angular/common';
import { Title } from '@angular/platform-browser';
import { DatosService } from '../servicios/datos.service';


@Component({
  selector: 'app-formproduct',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, FormsModule],
  templateUrl: './formproduct.component.html',
  styleUrl: './formproduct.component.scss'
})
export class FormproductComponent implements OnInit, DoCheck{

  public FormCreateProduct! : FormGroup;

  register_cn_prod: string="";
  register_picture: string="";
  register_prod_name: string="";
  register_descripcion: string="";
  register_precio: string="";
  register_stock: string="";
  register_categoria_id!: FormControl;
  register_farmacia_id: string="";
  register_proveedor_id: string="";

  selectedCategoryOption!: string;
  selectedPharmacyOption!: string;
  selectedProviderOption!: string;

  pic_existe: boolean = false;
  picture_url: string = '';
  picture_copy!: File;
  content_type: string = '';

  campoFormVacio: boolean = false;

  categories: any[] = [];
  pharmacies: any[] = [];
  providers: any[] = [];

  errorFormulario: boolean = false;
  formError: string = 'El producto ya existe.';

  constructor(private router: Router, private activatedRoute:ActivatedRoute, private crudProduct: CrudproductService, public fb: FormBuilder, private titleService: Title, private datosService: DatosService, private viewportScroller: ViewportScroller) {
    this.FormCreateProduct = this.fb.group({
      register_cn_prod:['', Validators.required],
      register_picture:[''],
      register_prod_name:['', Validators.required],
      register_descripcion:['', Validators.required],
      register_precio:['', Validators.required],
      register_stock:['', Validators.required],
      register_categoria_id:[''],
      register_farmacia_id:[''],
      register_proveedor_id:[''],
    });


  }

  ngOnInit(): void {
    this.titleService.setTitle('Sitio Administrativo | Añadir producto');


    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.viewportScroller.scrollToPosition([0, 0]);
      }
    });

    this.datosService.getCategoriesList()
    .subscribe(categories => {
      this.categories = categories;
    });

    this.datosService.getPharmaciesList()
      .subscribe(pharmacies => {
        this.pharmacies = pharmacies;
      });

    this.datosService.getProvidersList()
      .subscribe(providers => {
        this.providers = providers;
      });

  }

  ngDoCheck(){
    this.emptyFieldsFunction();
  }


  onFileSelected(event: any) {
    const fileTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp']
    const maxFileSize = 900*1024; //921kb
    const file: File = event.target.files[0];
    if (!fileTypes.includes(file.type)) {
      this.pic_existe = false;
      this.FormCreateProduct.get('register_picture')?.setValue('');
      alert('El archivo debe ser PNG, JPEG, JPG o WEBP.')

    }else if (file.size > maxFileSize){
      this.pic_existe = false;
      this.FormCreateProduct.get('register_picture')?.setValue('');
      alert('La imagen es demasiado grande')

    }else{
      this.picture_copy = file;

      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        this.picture_url = reader.result as string;
        this.pic_existe = true;
      };
    }
  }

  emptyFieldsFunction(){
    let emptyField = false;

    if(this.FormCreateProduct.get('register_categoria_id')?.value === undefined ||
       this.FormCreateProduct.get('register_farmacia_id')?.value === undefined || 
       this.FormCreateProduct.get('register_proveedor_id')?.value === undefined) {
        
        emptyField=true;
    }

    Object.keys(this.FormCreateProduct.controls).forEach(control => {
      if(control !== 'register_picture' && this.FormCreateProduct.get(control)?.value=== ''){
        emptyField = true;
      }else if(control !== 'register_picture' && this.FormCreateProduct.get(control)?.value=== null){
        emptyField = true;
      }
    })
    this.campoFormVacio = emptyField;
  }


  register() {
    const myForm = this.FormCreateProduct.value;
    const product_pic = this.picture_copy
  
    if (product_pic instanceof File) {
      const reader = new FileReader();
      reader.readAsDataURL(product_pic);
      reader.onload = () => {
        const base64Image = reader.result; 

        myForm.register_picture = base64Image;
  
        const registerData = {
          cn_prod: myForm.register_cn_prod,
          imagen_prod: myForm.register_picture,
          nombre_prod: myForm.register_prod_name,
          descripcion: myForm.register_descripcion,
          precio: myForm.register_precio,
          stock: myForm.register_stock,
          categoria_id: myForm.register_categoria_id,
          cif_farm: myForm.register_farmacia_id,
          cif_prov: myForm.register_proveedor_id,
        };

        this.crudProduct.saveProduct(registerData).subscribe(
        response => {
          localStorage.setItem('activeTab', 'tables');
          this.router.navigate(['/admin/panel']);
        }, error=>{
          console.log(error)
          this.errorFormulario = true;
        })
        
      };
    } else {

      const registerData = {
        cn_prod: myForm.register_cn_prod,
        imagen_prod: myForm.register_picture,
        nombre_prod: myForm.register_prod_name,
        descripcion: myForm.register_descripcion,
        precio: myForm.register_precio,
        stock: myForm.register_stock,
        categoria_id: myForm.register_categoria_id,
        cif_farm: myForm.register_farmacia_id,
        cif_prov: myForm.register_proveedor_id,
      };
      this.crudProduct.saveProduct(registerData).subscribe(
        response => {
          localStorage.setItem('activeTab', 'tables');
          this.router.navigate(['/admin/panel']);
        }, error=>{
          console.log(error)
          this.errorFormulario = true;
        })
  
    }
  }
  


  backToAdmin(){
    this.router.navigate(['/admin/panel']);
  }

}





