const showerBanks = document.getElementById('showerbanks')
const showerATMs = document.getElementById('showerATMs')

// Добавляем слушатель изменения состояния для каждого чекбокса
showerATMs.addEventListener('change', handleATMChange);
showerBanks.addEventListener('change', handleBankChange);

// Обработчики событий
function handleATMChange(event) {
    const checkbox = event.target;  
    const isChecked = checkbox.checked;  
    debugger
    if (isChecked) {  
      // checkbox is checked
      showAtm()
    } else {  
      // checkbox is unchecked
      clearMap()
    }
}

function handleBankChange(event) {
    const checkbox = event.target;  
    const isChecked = checkbox.checked;  
    debugger
    if (isChecked) {  
      // checkbox is checked
      show_office()
    } else {  
      // checkbox is unchecked
      clearMap()
    }
}

if (navigator.geolocation)
{
    navigator.geolocation.getCurrentPosition(showPosition);
}
else
{
    console.log("Geolocation is not supported by this browser.");
}
  
function showPosition(position) {
    console.log(position.coords.latitude); // Широта
    console.log(position.coords.longitude); // Долгота
    console.log(position.coords.accuracy);  // Точность
}