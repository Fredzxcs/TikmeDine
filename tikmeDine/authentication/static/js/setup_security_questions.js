 // Access JWT token from Django context
 const jwtToken = "{{ token }}";

 // Toggle visibility for password fields
 function toggleVisibility(fieldId) {
     const field = document.getElementById(fieldId);
     field.type = field.type === "password" ? "text" : "password";
 }

 // Example function to use JWT token in an API request
 async function submitSecurityAnswers() {
     const formData = new FormData(document.getElementById('security-questions-form'));
     try {
         const response = await fetch('/api/security-answers/', {
             method: 'POST',
             headers: {
                 'Authorization': `Bearer ${jwtToken}`,  // Pass JWT in the Authorization header
                 'X-CSRFToken': formData.get('csrfmiddlewaretoken')
             },
             body: formData
         });
         const result = await response.json();
         if (response.ok) {
             console.log("Success:", result);
         } else {
             console.error("Error:", result);
         }
     } catch (error) {
         console.error("Request failed:", error);
     }
 }

 // Attach form submission handler to submit security answers
 document.getElementById('security-questions-form').addEventListener('submit', function (event) {
     event.preventDefault();
     submitSecurityAnswers();
 });