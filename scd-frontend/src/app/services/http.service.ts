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
    this.baseUrl = 'api/';
  }

  public PostFirstProcess(file: any) {
    console.log('serve');
    return this.http.post(this.baseUrl + 'v1/google-ads/customer_list', file)
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
