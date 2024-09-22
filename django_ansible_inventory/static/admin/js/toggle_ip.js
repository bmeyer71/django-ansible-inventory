document.addEventListener("DOMContentLoaded", function () {
  const useManualIpCheckbox = document.getElementById("id_use_manual_ip");
  const ipDropdown = document.querySelector(".field-ip_address");
  const manualIpField = document.querySelector(".field-manual_ip");

  // Check if the elements exist before adding event listeners or manipulating the DOM
  if (useManualIpCheckbox && ipDropdown && manualIpField) {
    function toggleIpInput() {
      if (useManualIpCheckbox.checked) {
        ipDropdown.style.display = "none";
        manualIpField.style.display = "block";
      } else {
        ipDropdown.style.display = "block";
        manualIpField.style.display = "none";
      }
    }

    useManualIpCheckbox.addEventListener("change", toggleIpInput);
    toggleIpInput(); // Run on page load to set the initial state
  }
});
