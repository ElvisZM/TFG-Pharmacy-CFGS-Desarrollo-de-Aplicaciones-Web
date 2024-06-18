import { Component, DoCheck, OnInit } from '@angular/core';
import { Router, ActivatedRoute, RouterLink, NavigationEnd } from '@angular/router';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { FormBuilder,FormControl,FormGroup,Validators } from '@angular/forms';
import { CrudproductService } from '../servicios/crudproduct.service';
import { CommonModule, ViewportScroller } from '@angular/common';
import { Title } from '@angular/platform-browser';
import { DatosService } from '../servicios/datos.service';
import { environment } from '../../environments/environment';


@Component({
  selector: 'app-formproductupdate',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, FormsModule],
  templateUrl: './formproductupdate.component.html',
  styleUrl: './formproductupdate.component.scss'
})
export class FormproductupdateComponent implements OnInit, DoCheck{

  product: any;

  public url = environment.apiImageUrl;

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

  falloServidor: boolean = false;
  errorFalloServidor: string = 'Error en el servidor. Inténtelo más tarde.';

  constructor(private router: Router, private route:ActivatedRoute, private crudProduct: CrudproductService, public fb: FormBuilder, private titleService: Title, private datosService: DatosService, private viewportScroller: ViewportScroller) { }

  ngOnInit(): void {
  
    this.titleService.setTitle('Sitio Administrativo | Modificar producto');


    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.viewportScroller.scrollToPosition([0, 0]);
      }
    });

    this.route.paramMap.subscribe(params => {
      const cn_prod = +params.get('cn_prod')!;
      const cif_farm = params.get('cif_farm')!;
      this.datosService.getProduct(cn_prod, cif_farm).subscribe(
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
    this.emptyFieldsFunction();
  }


  onFileSelected(event: any) {
    const fileTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp']
    const maxFileSize = 900*1024; //921kb
    const file: File = event.target.files[0];
    if(file && !fileTypes.includes(file.type)){
      this.pic_existe = false;
      this.FormUpdateProduct.get('update_picture')?.setValue('');
      alert('El archivo debe ser PNG, JPEG, JPG o WEBP.')
    
    }else if (file.size > maxFileSize){
      this.pic_existe = false;
      this.FormUpdateProduct.get('update_picture')?.setValue('');
      alert('La imagen es demasiado grande')
    
    }else{
      this.picture_copy = file;
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

    if (this.FormUpdateProduct){
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
    }
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

        this.crudProduct.updateProduct(updateData, updateData.cn_prod).subscribe(
          response => {
            console.log('datos actualizados')
            localStorage.setItem('activeTab', 'tables');
            this.router.navigate(['/admin/panel']);
          }, error=>{
            console.log(error)
            setTimeout(() => {
              this.falloServidor = false;
            },2000);

          }
        )
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
        this.crudProduct.updateProduct(updateData, updateData.cn_prod).subscribe(
          response => {
            console.log('datos actualizados')
            localStorage.setItem('activeTab', 'tables');
            this.router.navigate(['/admin/panel']);
          }, error=>{
            console.log(error)
            this.falloServidor = true;
            setTimeout(() => {
              this.falloServidor = false;
            },2000);
          }
        )
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
  }

  delete(){
    const cn_prod = this.product.cn_prod
    const cif_farm = this.product.cif_farm

    const confirmDelete = window.confirm("¿Estás seguro de que quieres eliminar este producto?");

    if(confirmDelete){
  
      this.crudProduct.deleteProduct(cn_prod, cif_farm).subscribe(
        response => {
          console.log('Producto eliminado')
          localStorage.setItem('activeTab', 'tables');
          this.router.navigate(['/admin/panel']);
        }, error=>{
          console.log(error)
          this.falloServidor = true;
          setTimeout(() => {
            this.falloServidor = false;
          },2000);
        }
      )
    }
    
  }


  backToAdmin(){
    this.router.navigate(['/admin/panel']);
  }

}
