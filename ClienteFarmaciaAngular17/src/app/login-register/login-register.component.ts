declare var google: any;
declare const FB: any;
import { Component, OnInit, NgZone } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { RegistroService } from '../servicios/registro.service';
import { LoginService } from '../servicios/login.service';

import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { FormBuilder,FormControl,FormGroup,Validators } from '@angular/forms';
import { AuthService } from '../servicios/auth.service';



@Component({
  selector: 'app-login-register',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, RouterLink, FormsModule],
  templateUrl: './login-register.component.html',
  styleUrl: './login-register.component.scss'
})
export class LoginRegisterComponent implements OnInit{

  public FormRegister! : FormGroup;

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
  login_password: string="";

  errorMessageEmail: string ="";
  errorMessageUser: string ="";
  errorMessagePhone: string ="";
  invalidEmail: boolean = false;
  invalidUser: boolean = false;
  invalidPhone: boolean = false;

  errorCredentials: string= "";
  invalidLogin: boolean = false;

  passwordVisibility: boolean = false;

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
      

    }, {validator: this.formValidator})
    
  };

  ngOnInit(): void {
    accessObj.loginStyle();
    google.accounts.id.initialize({
      client_id: '924952635176-rom3np6k4kh95qmttp6iglh5lm550s13.apps.googleusercontent.com',
      callback: (resp: any) => {
        this.handleLogin(resp);        
      
      }
    });

    google.accounts.id.renderButton(document.getElementById('google-btn'), {
      theme: 'filled-blue',
      size: 'large',
      shape: 'rectangle',
      width: 350
    })

  }

  formValidator(formGroup: FormGroup){

    const email = formGroup.get('register_email')?.value;
    const emailRegEx = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    if (!emailRegEx.test(email)){
      formGroup.get('register_email')?.setErrors({ invalidFormatEmail: true });
    }else{
      formGroup.get('register_email')?.setErrors(null);
    }

    const phone = formGroup.get('register_phone')?.value
    const phoneRegEx = /^[6-7-9]\d{8}$/;
    
    if (!phoneRegEx.test(phone)){
      formGroup.get('register_phone')?.setErrors({ invalidFormatPhone:true })
    }
    else{
      formGroup.get('register_phone')?.setErrors(null)
    }

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
        picture: null,
        first_name: myForm.register_name,
        email: myForm.register_email,
        username: myForm.register_username,
        telefono: myForm.register_phone,
        birthday_date: new Date(myForm.register_birthday).toISOString().split('T')[0],
        password1: myForm.register_password1,
        password2: myForm.register_password2,
        domicilio: myForm.register_adress,
        rol: 1

      }
      this.registerService.registerUser(registerData).subscribe(
        response => {
          const loginData = {
            'username': registerData['username'],
            'password': registerData['password1']
          }
          this.loginService.loginToken(loginData).subscribe(
            response => {
              this.authService.setTokenCookie(response.access_token);
              this.authService.setNamePicture(registerData['first_name'])
              this.authService.setUserRol(registerData['rol'].toString())
              this.router.navigate(['/']);
            },error => {
              console.log(error);
            }
          )
        },
        error => {
          if(error.error.email == 'Email ya en uso.'){
            this.errorMessageEmail = 'El email ya está en uso.'
            this.invalidEmail = true
          }
          if(error.error.username == 'Usuario existente.'){
            this.errorMessageUser = 'El usuario ya está en uso.'
            this.invalidUser = true
          }
          if(error.error.telefono == 'Teléfono inválido o en uso.'){
            this.errorMessagePhone = 'El teléfono ya está en uso o es inválido.'
            this.invalidPhone = true            
          }
        }
      )
    }
  };

  login() {
    const user = {username:this.login_username,password:this.login_password}
    this.loginService.loginToken(user).subscribe((data)=>{
      console.log(data)
      this.authService.setTokenCookie(data.access_token);
      this.authService.getUserInfo();
      this.router.navigate(['/']);
      setTimeout(() => {
        window.location.reload();
      }, 400);
    }, error => {
      this.errorCredentials = 'Credenciales incorrectas. Por favor, inténtelo de nuevo.';
      this.invalidLogin = true;
      
    })
  }

  showLoginPassword(){
    if(this.passwordVisibility==false){
      this.passwordVisibility=true;
    }else{
      this.passwordVisibility=false;
    }
  }

  private decodeToken(token: string){
    return JSON.parse(atob(token.split(".")[1]));
  }

  handleLogin(response: any){
    if (response){
      const payLoad = this.decodeToken(response.credential);
      const dataToSave = {
        first_name: payLoad.given_name,
        last_name: payLoad.family_name,
        email: payLoad.email,
        profile_pic: payLoad.picture,
        rol: 2
      }
      this.registerService.registerGoogleDataToServer(dataToSave).subscribe(
        response => {
          this.authService.setNamePicture(payLoad.given_name, payLoad.picture)
          this.authService.setTokenCookie(payLoad.jti);
          this.authService.setUserRol(dataToSave.rol.toString())
          this.router.navigate(['/']);
          
        },error =>{
          console.log(error);            
        }
      )
    }
  }


  loginFB(){
    this.invalidLogin = false;
    FB.login((result:any) => {
      this.invalidLogin = false;

      if (result) {
        const accessToken = result.authResponse.accessToken;

        this.authService.getFacebookUserProfile(accessToken).subscribe(datos_response => {
          const dataToSave = {
            first_name: datos_response.name,
            email: datos_response.email,
            profile_pic: datos_response.picture.data.url,
            rol: 2
          }
          this.registerService.registerFacebookDataToServer(dataToSave).subscribe(
            response => {
              // this.authService.exchangeFacebookToken(accessToken).subscribe(
              //   response => {
              //     console.log(response);
              //   }, (error) => {
              //     console.log(error);
              //   }
              // )
              this.authService.setNamePicture(datos_response.name, datos_response.picture.data.url)
              this.authService.setTokenCookie(accessToken);
              this.authService.setUserRol(dataToSave.rol.toString())
              this.router.navigate(['/']);
              
            },error =>{
              console.log(error);            
            }
          )
        }
      );
      } else {
        console.log('User cancelled login or did not fully authorize.');
      }
        
    }, {scope:'email'});
  }


}
