document.addEventListener('DOMContentLoaded', function () {
  const contactForm = document.querySelector('#contact form');
  const contactSection = document.querySelector('#contact');

  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();

      const formData = new FormData(contactForm);
      const action = contactForm.getAttribute('action');
      
      // Give feedback that the form is submitting
      const submitButton = contactForm.querySelector('button[type="submit"]');
      submitButton.textContent = 'Sending...';
      submitButton.disabled = true;

      fetch(action, {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json'
        }
      }).then(response => {
        if (response.ok) {
          // Show a success message
          contactSection.innerHTML = '<h2 class="section-heading">Thank You!</h2><p>Your message has been sent successfully. I will get back to you shortly.</p>';
        } else {
          // Handle server errors
          response.json().then(data => {
            if (Object.hasOwn(data, 'errors')) {
              const errorMsg = data["errors"].map(error => error["message"]).join(", ");
              throw new Error(errorMsg);
            }
            throw new Error('Something went wrong on the server.');
          }).catch(error => {
            showError(error.message);
          });
        }
      }).catch(error => {
        // Handle network errors
        showError(error.message);
      });
    });
  }

  function showError(message) {
    // Restore the form and show an error
    const submitButton = contactForm.querySelector('button[type="submit"]');
    submitButton.textContent = 'Send Message';
    submitButton.disabled = false;
    
    // Create an error message element if it doesn't exist
    let errorElement = contactSection.querySelector('.form-error');
    if (!errorElement) {
      errorElement = document.createElement('p');
      errorElement.className = 'form-error';
      errorElement.style.color = 'red';
      contactForm.appendChild(errorElement);
    }
    errorElement.textContent = `Error: ${message}`;
  }
});
