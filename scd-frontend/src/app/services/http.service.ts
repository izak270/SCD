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
    return this.http.post(this.baseUrl + 'audio_file', formData,{headers,observe:'events'})
//     return this.http.get(this.baseUrl + 'helloworld', file)

  }

  public postSecondProcess(file: any, option: any) {
    // const formData = new FormData();
    // formData.append("file", file, 'file.name');
    console.log('sec');
    console.log(file);
    return this.http.post(this.baseUrl + 'v1/google-ads/customer_list',
      file, {headers : new HttpHeaders({ 'Content-Type': 'image/jpeg','enctype': 'multipart/form-data' })}
    )
  }

}
