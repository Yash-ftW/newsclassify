const displayDiv = document.getElementById('data-display');
const nextButton = document.getElementById('next-button');

let offset = 0;

// Load the initial data
loadData();

// Add event listener to the "Next" button
nextButton.addEventListener('click', () => {
  offset++;
  loadData();
});

function loadData() {
  // Send an AJAX request to fetch the data
  const xhr = new XMLHttpRequest();
  xhr.open('GET', `/data/${offset}`, true);
  xhr.onload = function() {
    if (this.status === 200) {
      displayDiv.innerHTML = this.responseText;
    }
  };
  xhr.send();
}
