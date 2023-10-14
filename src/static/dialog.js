
// Элементы виджета
const listMessages = document.getElementById('list_messages')
const inputBox = document.getElementById('dialog_input')
const sendButton = document.getElementById('button_send_message')

// Список сообщений
let messages = []

// Формирование сообщения для чата
function createMessage(inputText) {
    return `
    <li class="list-group-item d-flex justify-content-between align-items-center">
      <span>${inputText}</span>
    </li>
    `
}

// Отправка сообщения в чат
sendButton.onclick = function(event) {
    const value = inputBox.value
    if (value.length > 0) {
        messages.push('Вы: ' + value)
        inputBox.value = ''
    }
    updateChat()
}

// Обновление списка сообщений в чате
function updateChat() {
    listMessages.innerHTML = ''
    for (const msg of messages) {
        const msgHTML = createMessage(msg)
        listMessages.insertAdjacentHTML('afterbegin', msgHTML)
    }
}