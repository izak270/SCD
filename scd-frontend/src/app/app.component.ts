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
  public speakers: any = [
//     { "From": 40.123, "To": 44.313, 2: Array(256), 'cluster': 4 },
//     { "From": 44.313, "To": 45.313, 2: Array(256), 'cluster': 2 },
//     { "From": 45.313, "To": 46.313, 2: Array(256), 'cluster': 2 },
//     { "From": 46.123, "To": 48.313, 2: Array(256), 'cluster': 1 },
//     { "From": 48.123, "To": 51.313, 2: Array(256), 'cluster': 4 },
//     { "From": 51.123, "To": 53.313, 2: Array(256), 'cluster': 2 },
//     { "From": 53.123, "To": 55.313, 2: Array(256), 'cluster': 2 },
//     { "From": 55.123, "To": 57.313, 2: Array(256), 'cluster': 1 },
//     { "From": 40.123, "To": 44.313, 2: Array(256), 'cluster': 4 },
//     { "From": 40.123, "To": 43.313, 2: Array(256), 'cluster': 2 },
//     { "From": 40.123, "To": 42.313, 2: Array(256), 'cluster': 2 },
//     { "From": 40.123, "To": 41.313, 2: Array(256), 'cluster': 1 },
//     { "From": 40.123, "To": 44.313, 2: Array(256), 'cluster': 4 },
//     { "From": 40.123, "To": 43.313, 2: Array(256), 'cluster': 2 },    { "From": 40.123, "To": 41.313, 2: Array(256), 'cluster': 1 },
//     { "From": 40.123, "To": 42.313, 2: Array(256), 'cluster': 2 },
//     { "From": 40.123, "To": 41.313, 2: Array(256), 'cluster': 1 },
//     { "From": 40.123, "To": 44.313, 2: Array(256), 'cluster': 4 },
//     { "From": 40.123, "To": 43.313, 2: Array(256), 'cluster': 2 },    { "From": 40.123, "To": 41.313, 2: Array(256), 'cluster': 1 },
//     { "From": 40.123, "To": 42.313, 2: Array(256), 'cluster': 2 },
//     { "From": 40.123, "To": 41.313, 2: Array(256), 'cluster': 1 },
//     { "From": 40.123, "To": 44.313, 2: Array(256), 'cluster': 4 },
//     { "From": 40.123, "To": 43.313, 2: Array(256), 'cluster': 2 },    { "From": 40.123, "To": 41.313, 2: Array(256), 'cluster': 1 },
//     { "From": 40.123, "To": 42.313, 2: Array(256), 'cluster': 2 },
//     { "From": 40.123, "To": 41.313, 2: Array(256), 'cluster': 1 },
//     { "From": 40.123, "To": 44.313, 2: Array(256), 'cluster': 4 },
//     { "From": 40.123, "To": 43.313, 2: Array(256), 'cluster': 2 },    { "From": 40.123, "To": 41.313, 2: Array(256), 'cluster': 1 },
//     { "From": 40.123, "To": 42.313, 2: Array(256), 'cluster': 2 },
//     { "From": 40.123, "To": 41.313, 2: Array(256), 'cluster': 1 },
//     { "From": 40.123, "To": 44.313, 2: Array(256), 'cluster': 1 },
//     { "From": 40.123, "To": 43.313, 2: Array(256), 'cluster': 1 },

  ];
  public files: any;
  constructor(private httpService: HttpService) {}
  ngOnInit() {
    const toSplice:any = []
   this.speakers.forEach((element, index) => {
      if(index>0&&this.speakers[index-1]['cluster']===element['cluster']){
        this.speakers[index]['From']=this.speakers[index-1]['From']
        this.speakers[index-1]=0
      }

    });
    this.speakers=this.speakers.filter(item=>{
      return item != 0
    })
    this.speakers.slice(0,20)

  }

  connectSpeakers(){
    console.log('connect')
      const toSplice:any = []
   this.speakers.forEach((element, index) => {
      if(index>0&&this.speakers[index-1]['cluster']===element['cluster']){
        this.speakers[index]['From']=this.speakers[index-1]['From']
        this.speakers[index-1]=0
      }

    });
    this.speakers=this.speakers.filter(item=>{
      return item != 0
    })
    this.speakers = this.speakers.slice(0,20)

    console.log(this.speakers);
  }


  onFileSelected(target: any) {
    this.files = target.files;
    console.log(this.files);
    this.uploadFile(this.files);
  }

  uploadFile(files: any) {
    let filelist: any = [];
    let formData: FormData = new FormData();
    for (var i = 0; i < files.length; ++i) {
      filelist[i] = files.item(i).name;
      console.log(files.item(i));
      formData.append(
        'uploadFile1',
        files.item(i),
        (filelist[i] = files.item(i).name)
      );
    }
    this.showLoader = true;
    this.httpService.uploadFile(formData).subscribe((data) => {
      this.showLoader = false;
      console.log(data);
    });
  }

  startPreprocess(){
    this.httpService.preprocess().subscribe(data=>{
      console.log(data);
    })
  }

  startProcess() {
    console.log('startProcess');
    this.showLoader = true;
    this.httpService.PostFirstProcess().subscribe((response) => {
      console.log(response, '111');
      this.showLoader = false
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
    this.showLoader = true;
    this.httpService.PostSecondProcess().subscribe((response) => {
      this.speakers = response;
      this.connectSpeakers()
      console.log(response);
      this.httpService.getDataForDiagram().subscribe((ress) => {
        this.showLoader = false;
        const url = window.URL.createObjectURL(new Blob([ress]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'template.xlsx');
        document.body.appendChild(link);
        link.click();
        console.log(ress);
      });
    });
  }
}
