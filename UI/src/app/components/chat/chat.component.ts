import { AfterViewChecked, Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import {ChatService} from './chat.service';
class Message {
  text?: string;
  type: MessageType;
}

enum MessageType {
  Bot = 'bot',
  User = 'user',
  Loading = 'loading'
}

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
export class ChatComponent implements OnInit, AfterViewChecked {
  @ViewChild('messageContainer') private messageContainer: ElementRef | undefined;
  @Input() public display: string;

  public form: FormGroup = new FormGroup({});
  public messages: Array<Message> = [];
  private canSendMessage = true;

  constructor(private formBuilder: FormBuilder, private chatService: ChatService){}

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      message: ['']
    });
    this.getBotMessage();
  }

  ngAfterViewChecked(): void {        
    this.scrollToBottom();        
  } 

  public onClickSendMessage(): void {
    const message = this.form.get('message').value;

    if (message && this.canSendMessage) {
      const userMessage: Message = {text: message, type: MessageType.User};
      this.messages.push(userMessage);
      this.getBotMessage(userMessage);
      this.form.get('message').setValue('');
      this.form.updateValueAndValidity();
      
    }
  }

  private getBotMessage(userMessage?: any ): void {
    this.canSendMessage = false;
    const waitMessage: Message = {type: MessageType.Loading};
    this.messages.push(waitMessage);

    setTimeout(() => {
      this.messages.pop();
      if(!userMessage) {
       const botMessage: Message = {text: 'Hello! feel free to ask about chidambaram?', type: MessageType.Bot};
       this.messages.push(botMessage);
      }else{
         this.chatService.postQuestion(userMessage?.text).subscribe((response: any) => {
        const botMessage: Message = {text: response.response, type: MessageType.Bot};
        this.messages.push(botMessage);
      });
      }
     
      this.canSendMessage = true;
   }, 2000);
  }
public convertMarkdownToHtml(text: string): string {

  return text ? text.replace(/\*\*(.*?)\*\*/g, '<br/><strong color="black">$1</strong> <br/>') : '';
}
  public onClickEnter(event: KeyboardEvent): void {
    event.preventDefault();
    this.onClickSendMessage();
  }

  private scrollToBottom(): void {
    this.messageContainer.nativeElement.scrollTop = this.messageContainer.nativeElement.scrollHeight;         
  }
  
}
