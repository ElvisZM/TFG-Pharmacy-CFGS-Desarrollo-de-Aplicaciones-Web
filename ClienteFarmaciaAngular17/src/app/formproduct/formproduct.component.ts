import { Component, DoCheck, OnInit } from '@angular/core';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { FormBuilder,FormControl,FormGroup,Validators } from '@angular/forms';
import { CrudproductService } from '../servicios/crudproduct.service';
import { CommonModule } from '@angular/common';
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
  formVacioError: string = '';

  categories: any[] = [];
  pharmacies: any[] = [];
  providers: any[] = [];


  constructor(private router: Router, private activatedRoute:ActivatedRoute, private crudProduct: CrudproductService, public fb: FormBuilder, private titleService: Title, private datosService: DatosService) {
    this.FormCreateProduct = this.fb.group({
      register_cn_prod:['', Validators.required],
      register_picture:['', Validators.required],
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
    const file: File = event.target.files[0];
    this.picture_copy = file;
    if (file) {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        this.content_type = file.type.split('/')[1];
        this.picture_url = reader.result as string;
        this.pic_existe = true;
      };
    }
  }

  emptyFieldsFunction(){
    let emptyField = false;

    this.FormCreateProduct.get('register_categoria_id')?.setValue(this.selectedCategoryOption)
    this.FormCreateProduct.get('register_farmacia_id')?.setValue(this.selectedPharmacyOption)
    this.FormCreateProduct.get('register_proveedor_id')?.setValue(this.selectedProviderOption)

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


  //   this.FormCreateProduct.get('register_categoria_id')?.setValue(this.selectedCategoryOption)
  //   this.FormCreateProduct.get('register_farmacia_id')?.setValue(this.selectedPharmacyOption)
  //   this.FormCreateProduct.get('register_proveedor_id')?.setValue(this.selectedProviderOption)

  //   if(this.FormCreateProduct.get('register_categoria_id')?.value === undefined ||
  //      this.FormCreateProduct.get('register_farmacia_id')?.value === undefined || 
  //      this.FormCreateProduct.get('register_proveedor_id')?.value === undefined) {
        
  //       this.campoFormVacio = true;
  //       return this.campoFormVacio;
  //       console.log("3 vacios")
  //   }else if(this.campoFormVacio === false){

  //     Object.keys(this.FormCreateProduct.controls).forEach(control => {
  //       if(control !== 'register_picture' && this.FormCreateProduct.get(control)?.value=== ''){
  //         this.campoFormVacio = true;
  //         this.formVacioError = `El campo ${control} no puede estar vacío`;
  //         console.log(this.formVacioError)
  //       }else{
  //         this.campoFormVacio = false;
  //       }
  //     })
  //     return this.campoFormVacio
  //   }else{
  //     this.campoFormVacio = false;
  //     return this.campoFormVacio;
  //   }
  // }
  register() {
    const myForm = this.FormCreateProduct.value;
    const product_pic = this.picture_copy
  
    // Verificar si product_pic es un archivo
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
          formato_imagen: this.content_type,
        };

        this.crudProduct.saveProduct(registerData).subscribe(
        response => {
          localStorage.setItem('activeTab', 'tables');
          this.router.navigate(['/admin/panel']);
        }, error=>{
          console.log(error)
        })
        // Aquí puedes llamar a tu método para guardar el producto si es necesario
        // this.saveProduct(registerData);
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
      console.log('Fuera de reader.onload');
      console.log(myForm);
      console.log(registerData);
  
      // Aquí puedes llamar a tu método para guardar el producto si es necesario
      // this.saveProduct(registerData);
    }
  }
    
  backToAdmin(){
    this.router.navigate(['/admin/panel']);
  }

}





