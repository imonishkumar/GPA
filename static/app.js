// logout.js
// Add an event listener to the "Log Out" button
document.getElementById('logout-button').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent the default behavior of the link

    // Display an alert when the button is clicked
    alert("You have been logged out.");
    window.location.href = "/";
    
    // You can also redirect the user to the logout URL after displaying the alert
    // window.location.href = "/logout"; // Replace "/logout" with your logout URL
});

