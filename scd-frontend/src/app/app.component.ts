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
  console.log('filechan')
    this.file = file.files[0];
    this.startProcess()
    // WshShell.Run("../app/files-from-server/file_example_XLS_10.xls", 1, false);
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

  startSecondProcess(file: any) {
    this.httpService.PostFirstProcess('pointId').subscribe(data => {
      console.log(data);
      this.showResults2 = true;
    // const file1 = file.target.files[0]
    // var form_data = new FormData();
    // form_data.append('file', file1)
    // console.log(file1);

    // let formData:FormData = new FormData();
    // formData.append('uploadFile', file1, 'file1.name');
    // let headers = new HttpHeaders({
    //   'Content-Type': 'image/jpeg'
   });
    /** In Angular 5, including the header Content-Type can invalidate your request */
  //   let options = {
  //     headers: headers
  //  }


    // this.httpService.postSecondProcess(formData, options).subscribe(data => {
    //   console.log(data);
    // })
  }
}

