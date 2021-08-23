import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { from } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class HttpService {
  private baseUrl: string;
  constructor(private http: HttpClient) {
    this.baseUrl = '';
  }


  public uploadFile(files: any, option?: any) {
    // const formData = new FormData();
    // formData.append("file", file, 'file.name');
    console.log('sec11');
    console.log(files);
    return this.http.post(this.baseUrl + 'upload_file',
    files, {headers : new HttpHeaders({ 'enctype': 'multipart/form-data' })}
    )
  }

  public preprocess() {
    return this.http.get(this.baseUrl + 'preprocess')
  }

  public PostFirstProcess() {
  
    return this.http.get(this.baseUrl + 'start_first_process', {
            headers:
            {
                'Content-Disposition': "attachment; filename=template.xlsx",
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            },
           responseType: 'blob',
        })
  }

  public PostSecondProcess() {
    let headers = new HttpHeaders({'FileName': 'asd'})
    return this.http.get(this.baseUrl + 'start_second_process' )
  }

  public getDataForDiagram() {
    let headers = new HttpHeaders({'FileName': 'asd'})
    return this.http.get(this.baseUrl + 'data_for_diagram', {
      headers:
      {
          'Content-Disposition': "attachment; filename=template.xlsx",
          'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      },
     responseType: 'blob',
  })
  }
}
