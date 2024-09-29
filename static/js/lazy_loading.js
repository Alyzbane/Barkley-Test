document.addEventListener('DOMContentLoaded', function() {
const uploadForm = document.getElementById('uploadForm');
const loadingSpinner = document.getElementById('loadingSpinner');

if (uploadForm) {
    uploadForm.addEventListener('submit', function() {
    loadingSpinner.style.display = 'flex'; // Show the spinner
    });
}

// For file input change, you can also trigger the spinner if needed
const fileInput = document.getElementById('file');
if (fileInput) {
    fileInput.addEventListener('change', function() {
    if (fileInput.files.length > 0) {
        loadingSpinner.style.display = 'flex'; // Show the spinner when a file is selected
    }
    });
}
});



