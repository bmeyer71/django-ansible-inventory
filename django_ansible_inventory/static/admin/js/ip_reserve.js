document.addEventListener("DOMContentLoaded", function () {
  const ipSelect = document.getElementById("id_ip_address");
  let reservedIpId = null;

  if (ipSelect) {
    ipSelect.addEventListener("change", function () {
      const ipId = this.value;
      //   console.log("Selected IP ID:", ipId); // For debugging

      // Release the previous reservation if it exists and is different from the new selection
      if (reservedIpId && reservedIpId !== ipId) {
        releaseIp(reservedIpId);
      }

      if (ipId) {
        reserveIp(ipId);
        reservedIpId = ipId;
      } else if (reservedIpId) {
        // Release reservation if no IP is selected
        releaseIp(reservedIpId);
        reservedIpId = null;
      }
    });

    // Release reservation when the page is unloaded
    window.addEventListener("beforeunload", function () {
      if (reservedIpId) {
        // Use navigator.sendBeacon for a synchronous request on page unload
        const formData = new FormData();
        formData.append("ip_id", reservedIpId);
        navigator.sendBeacon(
          "/admin/django_ansible_inventory/host/release-ip/",
          formData
        );
      }
    });
  }

  function reserveIp(ipId) {
    const formData = new FormData();
    formData.append("ip_id", ipId);

    fetch("/admin/django_ansible_inventory/host/reserve-ip/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (!data.success) {
          alert(data.message);
        } else {
          //   console.log("IP reserved successfully.");
        }
      })
      .catch((error) => {
        console.error("Error during IP reservation:", error);
      });
  }

  function releaseIp(ipId) {
    const formData = new FormData();
    formData.append("ip_id", ipId);

    fetch("/admin/django_ansible_inventory/host/release-ip/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          //   console.log("IP released successfully.");
        } else {
          console.error("Error releasing IP:", data.message);
        }
      })
      .catch((error) => {
        console.error("Error during IP release:", error);
      });
  }

  // Function to get CSRF token from cookies
  function getCookie(name) {
    // ... existing code ...
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
