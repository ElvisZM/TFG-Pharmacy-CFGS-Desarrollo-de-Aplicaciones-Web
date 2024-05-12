import { Component, DoCheck, OnInit } from '@angular/core';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { FormBuilder,FormControl,FormGroup,Validators } from '@angular/forms';
import { CrudproductService } from '../servicios/crudproduct.service';
import { CommonModule } from '@angular/common';
import { Title } from '@angular/platform-browser';
import { DatosService } from '../servicios/datos.service';

@Component({
  selector: 'app-formproductupdate',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, FormsModule],
  templateUrl: './formproductupdate.component.html',
  styleUrl: './formproductupdate.component.scss'
})
export class FormproductupdateComponent implements OnInit, DoCheck{

  product: any;

  url: string="http://localhost:8000";

  public FormUpdateProduct! : FormGroup;

  update_cn_prod: string="";
  update_picture: string="";
  update_prod_name: string="";
  update_descripcion: string="";
  update_precio: string="";
  update_stock: string="";
  update_categoria_id!: FormControl;
  update_farmacia_id: string="";
  update_proveedor_id: string="";

  selectedCategoryOption!: string;
  selectedPharmacyOption!: string;
  selectedProviderOption!: string;

  pic_existe: boolean = false;
  picture_url: string = '';
  picture_copy!: File;

  api_imagen_url: string = '';
  api_imagen_existe: boolean = false;

  campoFormVacio: boolean = false;
  formVacioError: string = '';

  categories: any[] = [];
  pharmacies: any[] = [];
  providers: any[] = [];




  constructor(private router: Router, private route:ActivatedRoute, private crudProduct: CrudproductService, public fb: FormBuilder, private titleService: Title, private datosService: DatosService) {
    this.FormUpdateProduct = this.fb.group({
      update_cn_prod:['', Validators.required],
      update_picture:['', Validators.required],
      update_prod_name:['', Validators.required],
      update_descripcion:['', Validators.required],
      update_precio:['', Validators.required],
      update_stock:['', Validators.required],
      update_categoria_id:[''],
      update_farmacia_id:[''],
      update_proveedor_id:[''],
    });


  }

  ngOnInit(): void {
  
    this.titleService.setTitle('Sitio Administrativo | Modificar producto');


    this.route.paramMap.subscribe(params => {
      const cn_prod = +params.get('cn_prod')!;
      this.datosService.getProduct(cn_prod).subscribe(
        response => {
          this.product = response
          console.log('Product')
          console.log(this.product)
          this.fillForm();

      }, error =>{
        console.error('Error: ' + error)
      }
      );
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
  }


  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    this.picture_copy = file;
    if (file) {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        this.picture_url = reader.result as string;
        this.pic_existe = true;
        this.api_imagen_existe = false;
      };
    }
  }


  emptyFieldsFunction(){
    let emptyField = false;

    this.FormUpdateProduct.get('update_categoria_id')?.setValue(this.selectedCategoryOption)
    this.FormUpdateProduct.get('update_farmacia_id')?.setValue(this.selectedPharmacyOption)
    this.FormUpdateProduct.get('update_proveedor_id')?.setValue(this.selectedProviderOption)

    if(this.FormUpdateProduct.get('update_categoria_id')?.value === undefined ||
       this.FormUpdateProduct.get('update_farmacia_id')?.value === undefined || 
       this.FormUpdateProduct.get('update_proveedor_id')?.value === undefined) {
        
        emptyField=true;
    }

    Object.keys(this.FormUpdateProduct.controls).forEach(control => {
      if(control !== 'update_picture' && this.FormUpdateProduct.get(control)?.value=== ''){
        emptyField = true;
      }else if(control !== 'update_picture' && this.FormUpdateProduct.get(control)?.value=== null){
        emptyField = true;
      }
    })
    this.campoFormVacio = emptyField;
  }

  update() {
    const myForm = this.FormUpdateProduct;
    const product_pic = this.picture_copy
    // myForm.update_categoria_id = this.selectedCategoryOption;
    console.log(myForm)
    console.log(this.selectedCategoryOption)
    return
    // if (this.campoFormVacio === true){
    //   this.formVacioError = 'Por favor, rellene todos los campos.';
    //   return;
    // }

    // // Verificar si product_pic es un archivo
    // if (product_pic instanceof File) {
    //   const reader = new FileReader();
    //   reader.readAsDataURL(product_pic);
    //   reader.onload = () => {
    //     const base64Image = reader.result; 

    //     myForm.update_picture = base64Image;
  
    //     const UpdateData = {
    //       cn_prod: myForm.update_cn_prod,
    //       imagen_prod: myForm.update_picture,
    //       nombre_prod: myForm.update_prod_name,
    //       descripcion: myForm.update_descripcion,
    //       precio: myForm.update_precio,
    //       stock: myForm.update_stock,
    //       categoria_id: myForm.update_categoria_id,
    //       cif_farm: myForm.update_farmacia_id,
    //       cif_prov: myForm.update_proveedor_id,
    //     };

    //     this.crudProduct.saveProduct(UpdateData).subscribe(
    //     response => {
    //       localStorage.setItem('activeTab', 'tables');
    //       this.router.navigate(['/admin/panel']);
    //     }, error=>{
    //       console.log(error)
    //     })
    //     // Aquí puedes llamar a tu método para guardar el producto si es necesario
    //     // this.saveProduct(registerData);
    //   };
    // } else {

    //   const UpdateData = {
    //     cn_prod: myForm.update_cn_prod,
    //     imagen_prod: myForm.update_picture,
    //     nombre_prod: myForm.update_prod_name,
    //     descripcion: myForm.update_descripcion,
    //     precio: myForm.update_precio,
    //     stock: myForm.update_stock,
    //     categoria_id: myForm.update_categoria_id,
    //     cif_farm: myForm.update_farmacia_id,
    //     cif_prov: myForm.update_proveedor_id,
    //   };
    //   console.log('Fuera de reader.onload');
    //   console.log(myForm);
    //   console.log(UpdateData);
  
      // Aquí puedes llamar a tu método para guardar el producto si es necesario
      // this.saveProduct(registerData);
    // }
  }

  fillForm(){
    this.FormUpdateProduct.get('update_cn_prod')?.setValue(this.product.cn_prod);
    if(this.product.imagen_prod){
      this.api_imagen_url = this.url + this.product.imagen_pro
      this.api_imagen_existe = true;
    }
    this.FormUpdateProduct.get('update_prod_name')?.setValue(this.product.nombre_prod);
    this.FormUpdateProduct.get('update_descripcion')?.setValue(this.product.descripcion);
    this.FormUpdateProduct.get('update_precio')?.setValue(this.product.precio);
    this.FormUpdateProduct.get('update_stock')?.setValue(this.product.stock);
    this.FormUpdateProduct.get('update_categoria_id')?.setValue(this.product.categoria_id.id);
    this.FormUpdateProduct.get('update_farmacia_id')?.setValue(this.product.cif_farm);
    this.FormUpdateProduct.get('update_proveedor_id')?.setValue(this.product.proveedor_id.cif_prov);
  }

  backToAdmin(){
    this.router.navigate(['/admin/panel']);
  }

}
