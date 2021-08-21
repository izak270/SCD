import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { from } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class HttpService {
  private POINTS = 'point';
  private baseUrl: string;

  constructor(private http: HttpClient) {
    this.baseUrl = '';
  }

  public PostFirstProcess(file: any) {
    let headers = new HttpHeaders({'FileName': 'asd'})

    console.log('serve');
    console.log(typeof(file))
    const formData = new FormData();
    formData.append("file", file,'myfile');
    return this.http.post(this.baseUrl + 'start_pre_process', formData, {
            headers:
            {
                'Content-Disposition': "attachment; filename=template.xlsx",
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            },
           responseType: 'blob',
        })
//     return this.http.get(this.baseUrl + 'helloworld', file)

  }

  public PostSecondProcess(file: any) {
    let headers = new HttpHeaders({'FileName': 'asd'})

    console.log('serve');
    console.log(typeof(file))
    const formData = new FormData();
    formData.append("file", file,'myfile');
    return this.http.post(this.baseUrl + 'start_pre_process', formData, {
            headers:
            {
                'Content-Disposition': "attachment; filename=template.xlsx",
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            },
           responseType: 'blob',
        })
//     return this.http.get(this.baseUrl + 'helloworld', file)

  }

  public uploadFile(file: any, option?: any) {
    // const formData = new FormData();
    // formData.append("file", file, 'file.name');
    console.log('sec11');
    console.log(file);
    return this.http.post(this.baseUrl + 'audio_file',
      file, {headers : new HttpHeaders({ 'Content-Type': 'image/jpeg','enctype': 'multipart/form-data' })}
    )
  }

}
