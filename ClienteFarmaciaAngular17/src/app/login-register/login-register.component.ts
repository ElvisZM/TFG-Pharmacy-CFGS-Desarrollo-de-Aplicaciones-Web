import { Component, DoCheck, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { RegistroService } from '../servicios/registro.service';
import { LoginService } from '../servicios/login.service';

import { ReactiveFormsModule } from '@angular/forms';
import { FormBuilder,FormControl,FormGroup,Validators } from '@angular/forms';
import { AuthService } from '../servicios/auth.service';



@Component({
  selector: 'app-login-register',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, RouterLink],
  templateUrl: './login-register.component.html',
  styleUrl: './login-register.component.scss'
})
export class LoginRegisterComponent implements OnInit{

  public FormRegister! : FormGroup;
  public FormLogin! : FormGroup;

  register_name: string="";
  register_email: string="";
  register_username: string="";
  register_phone: string="";
  register_birthday: string="";
  register_password1: string="";
  register_password2: string="";
  register_adress: string="";
  register_rol: string="";


  login_username: string="";
  login_password1: string="";

  errorMessage: string ="";

  constructor(private router: Router, private registerService: RegistroService, private loginService: LoginService, public fb: FormBuilder, private activatedRoute:ActivatedRoute, private authService:AuthService) {
    this.FormRegister = this.fb.group({
      register_name:['', Validators.required],
      register_email:['', Validators.required],
      register_username:['', Validators.required],
      register_phone:['', Validators.required],
      register_birthday:['', Validators.required],
      register_password1:['', Validators.required],
      register_password2:['', Validators.required],
      register_adress:['', Validators.required],
      

    }, {validator: this.PasswordValidator}),
    this.FormLogin = this.fb.group({
      login_username:['', Validators.required],
      login_password1:['', Validators.required]
    })
  };
  ngOnInit(): void {
    accessObj.loginStyle();
  }
  ngDoCheck(): void {
      // this.loadScript('../../assets/js/login-register.js');
    };

  // loadScript(scriptUrl: string): void {
  //   try {
  //     const script = document.createElement('script');
  //     script.src = scriptUrl;
  //     document.body.appendChild(script);
      
  //   } catch (error) {
  //     console.error('Error al cargar script:', error);
  //   }
  // }

  PasswordValidator(formGroup: FormGroup) {
    const password1 = formGroup.get('register_password1')?.value;
    const password2 = formGroup.get('register_password2')?.value;

    if (password1 != password2){
      formGroup.get('register_password2')?.setErrors({ passwordMismatch: true });
    } else{
      formGroup.get('register_password2')?.setErrors(null);
    }
  }

  register() {
    if (this.FormRegister.valid){
      const myForm = this.FormRegister.value;
      const registerData = {
        first_name: myForm.register_name,
        email: myForm.register_email,
        username: myForm.register_username,
        telefono: myForm.register_phone,
        birthday_date: new Date(myForm.register_birthday).toISOString().split('T')[0],
        password1: myForm.register_password1,
        password2: myForm.register_password2,
        domicilio: myForm.register_adress,
        rol: 2

      }
      this.registerService.registerUser(registerData).subscribe(
        response => {
          this.router.navigate(['/']);
        },
        error => {
          console.log('Error Register', error);
        }
      )

    }
  };

  login() {
    const user = {username:this.login_username,password:this.login_password1}
    this.loginService.login(user).subscribe((data)=>{
      this.authService.setTokenCookie(data.access_token);
      this.router.navigate(['/']);
    }, error => {
      this.errorMessage = "Credenciales incorrectas. Por favor, inténtalo de nuevo."
    })
  }

}
