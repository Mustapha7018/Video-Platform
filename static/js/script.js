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