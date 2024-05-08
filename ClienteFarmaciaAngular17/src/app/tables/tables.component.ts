import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CsvproductosService } from '../servicios/csvproductos.service';
import { DatosService } from '../servicios/datos.service';
import { AdminPanelComponent } from '../admin-panel/admin-panel.component';

@Component({
  selector: 'app-tables',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tables.component.html',
  styleUrl: './tables.component.scss'
})
export class TablesComponent implements OnInit {

  public importedData: Array<any> = [];

  myProductsList: Array<any> = [];
  CreatingProductMessage: string = '';
  createProduct: boolean = false;

  constructor(private _csvService: CsvproductosService, public datosService: DatosService, private adminPanel: AdminPanelComponent){}

  ngOnInit() {
    this.productsList();
  }


  public async importDataFromCSV(event: any) {
    let fileContent = await this.getTextFromFile(event);
    this.importedData = this._csvService.importDataFromCSV(fileContent);
    this._csvService.saveDataBackend(this.importedData).subscribe(response => {
      if (response) {
        localStorage.setItem('activeTab', 'tables')
        window.location.reload();
      };
    }, error => {
      if (error.error === 'Uno o más productos ya existen en esa farmacia'){

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

  private async getTextFromFile(event: any) {
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
        console.log(this.myProductsList);
    },
    error => {
      console.log(error);
    }
  )
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

}
