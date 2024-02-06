import { Component, inject } from '@angular/core';
import { FetchapiService } from '../../fetchapi.service'; 

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrl: './search-bar.component.css',
  
})
export class SearchBarComponent {
  public article:any = "";
  public fapi = inject(FetchapiService);
  public res = null;

async showData() {
    
    console.log("Searching...")
    this.res = await this.fapi.getData(this.article);
    console.log(this.res)


  }

}
