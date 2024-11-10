(function() {
  document.addEventListener('DOMContentLoaded', function() {
    const questionsContainer = document.getElementById('questions-container');
    const addQuestionButton = document.getElementById('add-question');
    console.log(document.querySelectorAll('input[name^="questions-"]').length);
    function addQuestionField(index, value = '') {
      const newQuestion = document.createElement('div');
      newQuestion.className = 'input-group mb-3';
      newQuestion.innerHTML = `
        <input class="form-control" name="questions-${index}-question" placeholder="Question ${index + 1}" type="text" value="${value}">
        <button class="btn btn-outline-secondary remove-question" type="button">Remove</button>
      `;
      questionsContainer.appendChild(newQuestion);
    }

    // Add existing questions
    const existingQuestions = document.querySelectorAll('input[name^="questions-"]').length;
    for (let i = 0; i < existingQuestions; i++) {
      const questionValue = document.querySelector(`input[name="questions-${i}-question"]`).value;
      addQuestionField(i, questionValue);
    }

    addQuestionButton.addEventListener('click', function() {
      const questionCount = questionsContainer.children.length;
      if (questionCount < 10) {
        addQuestionField(questionCount);
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

// Get the submit button inside the modal
var submitBtn = document.querySelector("#myModal input[type='submit']");


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


// Get the submit button inside the modal
var submitBtn = document.querySelector("#myModal input[type='submit']");

// Get the input field inside the modal
var answerInput = document.getElementById("modalInput");

// When the user clicks the submit button, close the modal
submitBtn.onclick = function() {
    modal.style.display = "none";
}



var inputField = document.querySelector("#myModal input[type='text']");




// When the user clicks the submit button, validate input, close modal, and update button
submitBtn.onclick = function (event) {
  event.preventDefault(); // Prevent default form submission behavior

  // Validate the input field
  if (inputField.value.trim() === "") {
      inputField.setCustomValidity("Please answer the question.");
      inputField.reportValidity(); // Show the validation message
      return; // Exit the function without closing the modal or updating the button
  } else {
      inputField.setCustomValidity(""); // Clear the custom validity message
  }

  // Close the modal
  modal.style.display = "none";

  // Update the "Follow Request" button text and disable it
  if (btn) {
      btn.textContent = "Requested";
      btn.disabled = true;
      btn.classList.remove("btn-primary");
      btn.classList.add("btn-secondary");
  }
};









// When the user clicks the submit button, validate input, close modal, and update button
submitBtn.onclick = function (event) {
  event.preventDefault(); // Prevent default form submission behavior

  // Validate the input field
  if (inputField.value.trim() === "") {
      inputField.setCustomValidity("Please answer the question.");
      inputField.reportValidity(); // Show the validation message
      return; // Exit the function without closing the modal or updating the button
  } else {
      inputField.setCustomValidity(""); // Clear the custom validity message
  }

  // Close the modal
  modal.style.display = "none";

  // Update the "Follow Request" button text and disable it
  if (btn) {
      btn.textContent = "Requested";
      btn.disabled = true;
      btn.classList.remove("btn-primary");
      btn.classList.add("btn-secondary");
  }
};