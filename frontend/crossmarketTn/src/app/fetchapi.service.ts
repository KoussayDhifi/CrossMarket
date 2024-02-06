import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class FetchapiService {

  constructor() { }

  private data = null;

  async getArticles (article:string) {
    let url = `http://127.0.0.1:8000/${article}`
    try{
    let json = await fetch(url);
    let d = await json.json();
    this.data = d;
    }catch(err) {
      console.error(err);
    }
    
    
  }
  async getData (article:string) {
    await this.getArticles(article);
    return this.data;
  }
}
