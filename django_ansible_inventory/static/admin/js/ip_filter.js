$(function ($) {
  $(document).ready(function () {
    // Function to load available IP addresses based on the selected VLAN
    function loadAvailableIPs(vlanId, selectedIP = null) {
      var ipAddressField = $("#id_ip_address");
      if (vlanId) {
        $.ajax({
          url: "/inventory/get-available-ips/",
          data: {
            vlan: vlanId,
            selected_ip: selectedIP, // Pass selected IP to the view
          },
          success: function (response) {
            ipAddressField.html(""); // Clear the existing options
            ipAddressField.append('<option value="">---------</option>');

            // Add the available IPs from the response
            $.each(response.available_ips, function (index, ip) {
              var selected = selectedIP == ip.id ? " selected" : "";
              ipAddressField.append(
                '<option value="' +
                  ip.id +
                  '"' +
                  selected +
                  ">" +
                  ip.ip_address +
                  "</option>"
              );
            });
          },
        });
      } else {
        ipAddressField.html('<option value="">---------</option>');
      }
    }

    // When the page is loaded, check if we are editing an existing host
    var initialVlan = $("#id_vlan").val();
    var selectedIP = $("#id_ip_address").val(); // This should be the selected IP's ID

    // If there's a selected VLAN, load the IP addresses based on that VLAN
    if (initialVlan) {
      loadAvailableIPs(initialVlan, selectedIP);
    }

    // Dynamically load IP addresses when the VLAN selection changes
    $("#id_vlan").change(function () {
      var vlanId = $(this).val();
      loadAvailableIPs(vlanId);
    });
  });
});
