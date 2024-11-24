// Helper function to show error messages
function showError(message) {
    const errorElement = document.getElementById('error-message');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.remove('d-none');
    }
}

// Helper function to clear error messages
function clearError() {
    const errorElement = document.getElementById('error-message');
    if (errorElement) {
        errorElement.textContent = "";
        errorElement.classList.add('d-none');
    }
}

// Helper function to get the token (either from the form or sessionStorage)
function getToken() {
    return document.querySelector('input[name="token"]')?.value || sessionStorage.getItem('token');
}

// Helper function to validate the security answers
function validateSecurityAnswers(questions, answers) {
    const uniqueQuestions = new Set(questions);
    if (questions.length !== uniqueQuestions.size) {
        showError("Please choose different questions for each field.");
        return false;
    }
    if (answers.some(answer => answer.trim() === "")) {
        showError("Please answer all security questions.");
        return false;
    }
    return true;
}

// Function to dynamically fetch `uidb64` if it's passed in the DOM or URL
function getUidb64() {
    const uidb64Field = document.querySelector('input[name="uidb64"]');
    if (uidb64Field) {
        return uidb64Field.value; // Get from a hidden input field, if available
    }

    // Try extracting `uidb64` from the URL (if it's a part of the current URL)
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('uidb64') || "default-uidb64"; // Replace "default-uidb64" with fallback logic, if needed
}

function submitSecurityAnswers(event) {
    event.preventDefault();

    const form = document.getElementById('security-questions-form');
    const questions = Array.from(form.querySelectorAll('select[name^="security_question"]')).map(field => field.value);
    const answers = Array.from(form.querySelectorAll('input[name^="security_answer"]')).map(input => input.value);

    if (!validateSecurityAnswers(questions, answers)) return;

    const token = getToken();
    const uidb64 = getUidb64();

    if (!uidb64 || !token) {
        console.error("Invalid UID or token.");
        window.location.href = "/api-auth/invalid_link/"; // Redirect on failure
        return;
    }

    sessionStorage.setItem('security_answers', JSON.stringify(answers));
    window.location.href = `/api-auth/setup_password/${uidb64}/${token}/`;
}

// Event listener for the security questions form submission
document.getElementById('security-questions-form')?.addEventListener('submit', submitSecurityAnswers);

// Optional: Add input validation for each field to check that security answers are non-empty
document.querySelectorAll('input[name^="security_answer"]').forEach(input => {
    input.addEventListener('input', function () {
        if (input.value.trim() !== "") {
            input.classList.remove('is-invalid');
        }
    });
});

// Optional: Add validation to ensure unique security questions are selected
document.querySelectorAll('select[name^="security_question"]').forEach(select => {
    select.addEventListener('change', function () {
        const questions = Array.from(document.querySelectorAll('select[name^="security_question"]')).map(select => select.value);
        const uniqueQuestions = new Set(questions);

        if (questions.length !== uniqueQuestions.size) {
            showError("Please choose different questions for each field.");
        } else {
            clearError(); // Clear any previous error messages
        }
    });
});
