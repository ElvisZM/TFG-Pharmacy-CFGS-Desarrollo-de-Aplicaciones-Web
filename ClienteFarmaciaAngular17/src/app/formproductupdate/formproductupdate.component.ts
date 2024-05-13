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
  update_farmacia_cif!: FormControl;
  update_proveedor_cif!: FormControl;

  selectedCategoryOption!: string;
  selectedPharmacyOption!: string;
  selectedProviderOption!: string;

  pic_existe: boolean = false;
  picture_url: string = '';
  picture_copy!: File;

  api_imagen_url: string = '';
  api_imagen_existe: boolean = false;

  campoFormVacio: boolean = false;
  formVacioError: string = 'Por favor, rellene todos los campos.';

  categories: any[] = [];
  pharmacies: any[] = [];
  providers: any[] = [];


  formulario_original: Array<any> = []
  iguales: boolean = false;
  formIgualError: string = 'No se han realizado cambios.';

  constructor(private router: Router, private route:ActivatedRoute, private crudProduct: CrudproductService, public fb: FormBuilder, private titleService: Title, private datosService: DatosService) {
    


  }

  ngOnInit(): void {
  
    this.titleService.setTitle('Sitio Administrativo | Modificar producto');

    this.route.paramMap.subscribe(params => {
      const cn_prod = +params.get('cn_prod')!;
      this.datosService.getProduct(cn_prod).subscribe(
        response => {
          this.product = response

          if(this.product.imagen_prod){
            this.api_imagen_url = this.url + this.product.imagen_pro
            this.api_imagen_existe = true;
          }

          this.FormUpdateProduct = this.fb.group({
            update_cn_prod:[this.product.cn_prod, Validators.required],
            update_picture:[''],
            update_prod_name:[this.product.nombre_prod, Validators.required],
            update_descripcion:[this.product.descripcion, Validators.required],
            update_precio:[this.product.precio, Validators.required],
            update_stock:[this.product.stock, Validators.required],
            update_categoria_id:[this.product.categoria_id.id],
            update_farmacia_cif:[this.product.farmacia_id.cif_farm],
            update_proveedor_cif:[this.product.proveedor_id[0].cif_prov],
          });

          this.formulario_original = { ...this.FormUpdateProduct.value }



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
    if(this.FormUpdateProduct){
      this.emptyFieldsFunction();
    }
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
    return file;
  }


  emptyFieldsFunction(){
    let emptyField = false;

    if(this.FormUpdateProduct.get('update_categoria_id')?.value === undefined ||
       this.FormUpdateProduct.get('update_categoria_id')?.value === "" ||
       this.FormUpdateProduct.get('update_farmacia_cif')?.value === undefined || 
       this.FormUpdateProduct.get('update_farmacia_cif')?.value === "" || 
       this.FormUpdateProduct.get('update_proveedor_cif')?.value === undefined || 
       this.FormUpdateProduct.get('update_proveedor_cif')?.value === "" ) {
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
    const myForm = this.FormUpdateProduct.value;
    const product_pic = this.picture_copy

    if (typeof myForm.update_categoria_id === 'string'){
      this.datosService.helperGetCategoryIdbyName(myForm.update_categoria_id).subscribe(data => {
        myForm.update_categoria_id = data.id;
      })
    }

    if (!myForm.update_proveedor_cif.startsWith('PV')){
      this.datosService.helperGetCifProviderbyName(myForm.update_proveedor_cif).subscribe(data => {
        myForm.update_proveedor_cif = data.cif_prov;
      })  
    }   

    if (!myForm.update_farmacia_cif.startsWith('PH')){
      this.datosService.helperGetCifPharmacybyName(myForm.update_farmacia_cif).subscribe(data => {
        myForm.update_farmacia_cif = data.cif_farm;
      })
    }

    if (product_pic instanceof File) {
      const reader = new FileReader();
      reader.readAsDataURL(product_pic);
      reader.onload = () => {
        const base64Image = reader.result; 

        myForm.update_picture = base64Image;

        const updateData = {
          cn_prod: myForm.update_cn_prod,
          imagen_prod: myForm.update_picture,
          nombre_prod: myForm.update_prod_name,
          descripcion: myForm.update_descripcion,
          precio: myForm.update_precio,
          stock: myForm.update_stock,
          categoria_id: myForm.update_categoria_id,
          cif_farm: myForm.update_farmacia_cif,
          cif_prov: myForm.update_proveedor_cif,
        };
      }

    }else{

      const updateData = {
        cn_prod: myForm.update_cn_prod,
        imagen_prod: myForm.update_picture,
        nombre_prod: myForm.update_prod_name,
        descripcion: myForm.update_descripcion,
        precio: myForm.update_precio,
        stock: myForm.update_stock,
        categoria_id: myForm.update_categoria_id,
        cif_farm: myForm.update_farmacia_cif,
        cif_prov: myForm.update_proveedor_cif,
      };

      if (!this.comprobarFormIgual(this.formulario_original, updateData)){
          console.log('Los datos han cambiado')
        // this.crudProduct.updateProduct(updateData, updateData.cn_prod).subscribe(
        //   response => {
        //     console.log(response)
        //   }, error=>{
        //     console.log(error)
        //   }
        // )
      }
 
      

    }
    
  }

  comprobarFormIgual(original_form: Object, updated_form: Object){
    let datos_original = Object.values(original_form)
    let datos_actualizados = Object.values(updated_form)

    for (let i = 0; i < datos_original.length; i++) {
      if (datos_original[i] !== datos_actualizados[i]) {
          this.iguales = false;
          break;
      }else{
        this.iguales = true;
      }
    }

    if (this.iguales) {
      datos_original.splice(0, datos_original.length)
      datos_actualizados.splice(0, datos_actualizados.length)
      setTimeout(() => {
        this.iguales = false;
      },2000)
      return true
      
    } else {
      return false
      
    }
    datos_original.splice(0, datos_original.length)
    datos_actualizados.splice(0, datos_actualizados.length)
  }

  backToAdmin(){
    this.router.navigate(['/admin/panel']);
  }

}
