import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';



interface Message {
  text: string;
  sender: 'user' | 'bot';
}

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.scss'
})
export class ChatbotComponent {
  chatOpen: boolean = false;
  messageText: string = '';
  messages: Message[] = [
    { text: 'Hi', sender: 'bot' },
    { text: 'How are you ...???', sender: 'bot' }
  ];

  openChat() {
    this.chatOpen = true;
  }

  closeChat() {
    this.chatOpen = false;
  }

  sendMessage(event: Event) {
    event.preventDefault(); // Prevenir el comportamiento por defecto del formulario
    console.log('Mensaje enviado:', this.messageText);
    // Aquí puedes implementar la lógica para enviar el mensaje
    this.messageText = ''; // Limpiar el campo de mensaje después de enviar
  }
}
