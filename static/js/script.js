document.addEventListener('DOMContentLoaded', (event) => {
    const inputs = document.querySelectorAll('.code-input');

    inputs.forEach((input, index) => {
        input.addEventListener('input', () => {
            if (input.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && input.value === '' && index > 0) {
                inputs[index - 1].focus();
            }
        });
    });
});


// Function to remove messages after 5 seconds
setTimeout(function () {
var alertMessages = document.querySelectorAll(".alert");
alertMessages.forEach(function (alert) {
    alert.remove();
});
}, 5000);


document.addEventListener('DOMContentLoaded', (event) => {
    const shareButton = document.getElementById('share-button');
    shareButton.addEventListener('click', () => {
        if (navigator.share) {
            navigator.share({
                title: document.title,
                url: window.location.href
            }).then(() => {
                console.log('Thanks for sharing!');
            }).catch(console.error);
        } else {
            alert('Your browser does not support the Web Share API');
        }
    });
});


document.getElementById('resend-button').addEventListener('click', function() {
    fetch("{% url 'resend-verification' %}", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}'
      },
      body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('A new verification code has been sent to your email.');
      } else {
        alert('Error resending verification code: ' + data.error);
      }
    })
    .catch(error => console.error('Error:', error));
  });