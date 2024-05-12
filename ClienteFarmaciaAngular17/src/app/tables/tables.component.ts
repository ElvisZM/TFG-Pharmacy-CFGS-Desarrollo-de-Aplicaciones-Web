import { Component, DoCheck, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CsvproductosService } from '../servicios/csvproductos.service';
import { DatosService } from '../servicios/datos.service';
import { AdminPanelComponent } from '../admin-panel/admin-panel.component';
import { Router } from '@angular/router';
import { CrudproductService } from '../servicios/crudproduct.service';

@Component({
  selector: 'app-tables',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tables.component.html',
  styleUrl: './tables.component.scss'
})
export class TablesComponent implements OnInit, DoCheck {

  importedData: Array<any> = [];

  myProductsList: Array<any> = [];
  CreatingProductMessage: string = '';

  url: string = 'http://localhost:8000';
  

  constructor(private _csvService: CsvproductosService, public datosService: DatosService, private adminPanel: AdminPanelComponent, private crudProduct : CrudproductService, private router: Router){}

  ngOnInit() {
    this.productsList();
  }

  ngDoCheck(){
  }
// ************************************PRODUCTOS*********************************************


  async importDataFromCSV(event: any) {
    let fileContent = await this.getTextFromFile(event);
    this.importedData = this._csvService.importDataFromCSV(fileContent);
    this._csvService.saveDataBackend(this.importedData).subscribe(response => {
      if (response) {
        localStorage.setItem('activeTab', 'tables')
        window.location.reload();
      };
    }, error => {
      if (error.error === 'Uno o más productos ya existen en esa farmacia o la farmacia no existe.'){

        localStorage.setItem('errorTab', 'tables');
        localStorage.setItem('errorProd', '1')
        window.location.reload();
      }else{
        localStorage.setItem('errorTab', 'tables');
        localStorage.setItem('errorProd', '2')
        window.location.reload();
      };
    })
  }

  async getTextFromFile(event: any) {
    const file: File = event.target.files[0];
    let fileContent = await file.text();

    return fileContent;
  }


  public saveDataInCSV(name: string, data: Array<any>): void {
    let csvContent = this._csvService.saveDataInCSV(data);

    var hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csvContent);
    hiddenElement.target = '_blank';
    hiddenElement.download = name + '.csv';
    hiddenElement.click();
  }

  productsList(){
    this.datosService.getProductsList().subscribe(
      response => {
        this.myProductsList = response;
        console.log(this.myProductsList)
    },
    error => {
      console.log(error);
    })
  }

  getProgressBarColor(stock: number, maxStock: number): string {
    const percentage = (stock / maxStock) * 100;
    if (percentage <= 25) {
        return 'progress-red'; 
    } else if (percentage <= 50) {
        return 'progress-orange'; 
    } else {
        return 'progress-green'; 
    }
  }

  createProduct(){
    this.router.navigate(['/admin/panel/create/product']);
  }

  updateProduct(product: number){
    this.router.navigate([`/admin/panel/update/product`, product]);
  }

}
