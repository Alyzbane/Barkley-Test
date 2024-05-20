var imageInput = document.getElementById("file")
var imagePreview = document.getElementById("imagePreview");
    
fileInput.addEventListener("change", function() {
  changeImage(this);
});

function changeImage(input) {
  var reader;

  if (input.files && input.files[0]) {
    reader = new FileReader();

    reader.onload = function(e) {
       imagePreview.src = reader.result;
    }   
    reader.readAsDataURL(input.files[0]);
  }
  else {
      imagePreview = '#';
  }
}


