(function() {
  document.addEventListener('DOMContentLoaded', function() {
    const questionsContainer = document.getElementById('questions-container');
    const addQuestionButton = document.getElementById('add-question');

    addQuestionButton.addEventListener('click', function() {
      const questionCount = questionsContainer.children.length;
      if (questionCount < 10) {
        const newQuestion = document.createElement('div');
        newQuestion.className = 'input-group mb-3';
        newQuestion.innerHTML = `
          <input class="form-control" name="questions-${questionCount}-question" placeholder="Question ${questionCount + 1}" type="text">
          <button class="btn btn-outline-secondary remove-question" type="button">Remove</button>
        `;
        questionsContainer.appendChild(newQuestion);
      }
    });

    questionsContainer.addEventListener('click', function(event) {
      if (event.target.classList.contains('remove-question')) {
        const questionCount = questionsContainer.children.length;
        if (questionCount > 1) {
          event.target.parentElement.remove();
        }
      }
    });
  });
}).call(this);

// Get the modal element
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("openModalBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
