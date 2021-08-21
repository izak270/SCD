import { Component, OnInit } from '@angular/core';
import { HttpService } from './services/http.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'sd-front-end';
  public showResults = false;
  public showResults2 = false;
  public file: any;
  constructor(
    private httpService: HttpService,
  ) { }

  ngOnInit() {
    console.log('in')

  }
  onFileSelected(file: any) {
    this.file = file.files[0];
    this.startProcess()
    // this.uploadFile(this.file)
    // WshShell.Run("../app/files-from-server/file_example_XLS_10.xls", 1, false);
  }
  
    uploadFile(file: any) {
        this.showResults2 = true;
      var form_data = new FormData();
      // form_data.append('file', file1)
      // console.log(file1);
  
      let formData:FormData = new FormData();
      formData.append('uploadFile', file, 'file1.name');
    //   let headers = new HttpHeaders({
    //     'Content-Type': 'image/jpeg'})
    //   let options = {
    //     headers: headers
    //  }
  
  
      this.httpService.uploadFile(formData).subscribe(data => {
        console.log(data);
      })
    }

  startProcess() {
    // if (this.file) {
   console.log('startProcess')
      this.httpService.PostFirstProcess(this.file).subscribe((response) => {
       console.log(response)
        const url = window.URL.createObjectURL(new Blob([response]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'template.xlsx');
        document.body.appendChild(link);
        link.click();
    })
    // } else {
      // alert('please select file')
    // }
  }

  startSecondProcess() {
    // if (this.file) {
   console.log('startProcess')
      this.httpService.PostSecondProcess(this.file).subscribe((response) => {
       console.log(response)
        const url = window.URL.createObjectURL(new Blob([response]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'template.xlsx');
        document.body.appendChild(link);
        link.click();
    })
    // } else {
      // alert('please select file')
    // }
  }
}

