// Get the current date and time
function getCurrentDateTime() {
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };
    return now.toLocaleDateString('en-US', options);
  }
  
  // Update the content of the HTML element with id="datetime" every second
  function updateDateTime() {
    const datetimeElement = document.getElementById('datetime');
    if (datetimeElement) {
      datetimeElement.textContent = getCurrentDateTime();
    }
  }
  
  // Update date and time initially and then every second
  updateDateTime();
  setInterval(updateDateTime, 1000);
  