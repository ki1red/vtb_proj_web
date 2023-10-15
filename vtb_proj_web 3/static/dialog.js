// Элементы виджета
const listMessages = document.getElementById('list_messages')
const inputBox = document.getElementById('dialog_input')
const sendButton = document.getElementById('button_send_message')

const default_text = 'Здравствуйте! Вас приветствует бот-помощник по работе сайта. В данный момент проводятся технические работы, извините за предоставленные неудобства'
const default_text_2 = 'Извините, в данный момент не могу обработать ваш запрос.'

// Список сообщений
let messages = [default_text]

// Формирование сообщения для чата
function createMessage(inputText) {
    return `
    <li class="list-group-item d-flex justify-content-between align-items-center">
      <span>${inputText}</span>
    </li>
    `
}

// Отправка сообщения в чат
sendButton.onclick = function (event) {
    const value = inputBox.value
    if (value.length > 0) {
        messages.push('Вы: ' + value)
        messages.push('Бот: ' + default_text_2)
        inputBox.value = ''
    }
    updateChat()
}

// Обновление списка сообщений в чате
function updateChat() {
    listMessages.innerHTML = ''
    let html = ''
    for (const msg of messages) {
        const msgHTML = createMessage(msg)
        html += msgHTML
    }
    listMessages.insertAdjacentHTML('beforeend', html) // Добавлен вызов insertAdjacentHTML

}

// Вызов функции updateChat() в конце файла
updateChat();