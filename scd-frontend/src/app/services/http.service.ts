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


  public uploadFile(file: any, option?: any) {
    // const formData = new FormData();
    // formData.append("file", file, 'file.name');
    console.log('sec11');
    console.log(file);
    const formData = new FormData();
    formData.append("file", file,'myfile');
    return this.http.post(this.baseUrl + 'upload_file',
    formData, {headers : new HttpHeaders({ 'Content-Type': 'image/jpeg','enctype': 'multipart/form-data' })}
    )
  }

  public PostFirstProcess(file: any) {
  
    return this.http.get(this.baseUrl + 'start_first_process', {
            headers:
            {
                'Content-Disposition': "attachment; filename=template.xlsx",
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            },
           responseType: 'blob',
        })
  }

  public PostSecondProcess(file: any) {
    let headers = new HttpHeaders({'FileName': 'asd'})
    return this.http.get(this.baseUrl + 'start_second_process', {
            headers:
            {
                'Content-Disposition': "attachment; filename=template.xlsx",
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            },
           responseType: 'blob',
        })
  }

  public getDataForDiagram() {
    let headers = new HttpHeaders({'FileName': 'asd'})
    return this.http.get(this.baseUrl + 'data_for_diagram', )
  }
}
