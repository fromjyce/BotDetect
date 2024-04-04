document.getElementById("pcap_file").addEventListener("change", function () {
  var fileInput = this;
  var uploadButton = document.getElementById("uploadButton");
  var selectedFileText = document.getElementById("selectedFileText");

  if (fileInput.files.length > 0) {
    var fileName = fileInput.files[0].name;
    selectedFileText.innerText = fileName + " is selected.";
    selectedFileText.style.display = "block";
    uploadButton.style.display = "block";
  } else {
    selectedFileText.style.display = "none";
    uploadButton.style.display = "none";
  }
});

document
  .getElementById("reload-link")
  .addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default behavior of link click
    window.location.href = "http://127.0.0.1:5000/"; // Redirect to the specified URL
  });

