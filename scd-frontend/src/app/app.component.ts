import { Component, OnInit } from '@angular/core';
import { HttpService } from './services/http.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  title = 'sd-front-end';
  public showResults = false;
  public showResults2 = false;
  public showLoader = false;
  public colors = [
    '#FF6633',
    '#FFB399',
    '#FF33FF',
    '#FFFF99',
    '#00B3E6',
    '#E6B333',
    '#3366E6',
    '#999966',
    '#99FF99',
    '#B34D4D',
    '#B366CC',
    '#4D8000',
    '#B33300',
    '#CC80CC',
    '#66664D',
    '#991AFF',
    '#E666FF',
    '#4DB3FF',
    '#1AB399',
    '#E666B3',
    '#33991A',
    '#6666FF',
  ];
  public speackers: any = [
    { 0: 40.123, 1: 40.313, 2: Array(256), 3: 1 },
    { 0: 40.123, 1: 40.313, 2: Array(256), 3: 2 },
    { 0: 40.123, 1: 40.313, 2: Array(256), 3: 3 },
    { 0: 40.123, 1: 40.313, 2: Array(256), 3: 1 },
    { 0: 40.123, 1: 40.313, 2: Array(256), 3: 4 },
    { 0: 40.123, 1: 40.313, 2: Array(256), 3: 2 },
    { 0: 40.123, 1: 40.313, 2: Array(256), 3: 5 },
    { 0: 40.123, 1: 40.313, 2: Array(256), 3: 1 },
    { 0: 40.123, 1: 40.313, 2: Array(256), 3: 4 },
    { 0: 40.123, 1: 40.313, 2: Array(256), 3: 2 },
    { 0: 40.123, 1: 40.313, 2: Array(256), 3: 5 },
    { 0: 40.123, 1: 40.313, 2: Array(256), 3: 1 },
    { 0: 40.123, 1: 40.313, 2: Array(256), 3: 1 },
  ];
  public file: any;
  constructor(private httpService: HttpService) {}

  ngOnInit() {
  }
  onFileSelected(file: any) {
    this.file = file.files[0];
    // this.startProcess()
    this.uploadFile(this.file);
    // WshShell.Run("../app/files-from-server/file_example_XLS_10.xls", 1, false);
  }

  uploadFile(file: any) {
    this.showResults2 = true;
    var form_data = new FormData();
    // form_data.append('file', file1)
    // console.log(file1);

    let formData: FormData = new FormData();
    formData.append('uploadFile', file, 'file1.name');
    //   let headers = new HttpHeaders({
    //     'Content-Type': 'image/jpeg'})
    //   let options = {
    //     headers: headers
    //  }

    this.showLoader = true;
    this.httpService.uploadFile(formData).subscribe((data) => {
      setTimeout(() => {
        this.showLoader = false;
      }, 3000);
      console.log(data);
    });
  }

  startProcess() {
    console.log('startProcess');
    this.httpService.PostFirstProcess(this.file).subscribe((response) => {
      console.log(response, '111');
      const url = window.URL.createObjectURL(new Blob([response]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'template.xlsx');
      document.body.appendChild(link);
      link.click();
    });
  }

  startSecondProcess() {
    console.log('second');
    this.httpService.PostSecondProcess(this.file).subscribe((response) => {
      console.log(response);
      const url = window.URL.createObjectURL(new Blob([response]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'template.xlsx');
      document.body.appendChild(link);
      link.click();
      const reader = new FileReader();
      console.log('reader');

      const file = new File([response], 'file');
      console.log(file);
      this.httpService.getDataForDiagram().subscribe((ress) => {
        console.log(ress);
        this.speackers = ress;
      });
    });
  }
}
