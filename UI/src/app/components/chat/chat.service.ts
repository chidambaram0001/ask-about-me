import { Injectable } from "@angular/core";

import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  constructor(private http: HttpClient) { }

  postQuestion(question: string) {
    return this.http.post('/v2/chat', { message:question });
  }
}
