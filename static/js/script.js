// Function to show the edit form for the menu item
function editMenu(itemId, itemName, itemPrice) {
    document.getElementById('edit-form').style.display = 'block';
    document.getElementById('item_id').value = itemId;
    document.getElementById('item_name').value = itemName;
    document.getElementById('price').value = itemPrice;
}

// Function to cancel the edit action and hide the edit form
function cancelEdit() {
    document.getElementById('edit-form').style.display = 'none';
}

// Function to handle the toggle of the payment status
function togglePaymentStatus(paymentId, currentStatus) {
    let newStatus = currentStatus === 'Pending' ? 'Complete' : 'Pending';

    // Send the updated status to the backend (you will need to set up an endpoint for this)
    fetch(`/toggle_payment_status/${paymentId}/${newStatus}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the status on the page without reloading
            const statusElement = document.getElementById(`status-${paymentId}`);
            statusElement.innerText = newStatus;
        } else {
            alert("Error updating payment status.");
        }
    });
}

// Function to submit the form for adding a student
function addStudent(event) {
    event.preventDefault(); // Prevent the form from refreshing the page
    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Make a POST request to add the student (adjust the URL accordingly)
    fetch('/add_student', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Student added successfully!');
            // Optionally refresh the list of students or append the new student
        } else {
            alert('Error adding student.');
        }
    });
}

// Function to submit the form for adding a menu item
function addMenu(event) {
    event.preventDefault(); // Prevent the form from refreshing the page
    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Make a POST request to add the menu item (adjust the URL accordingly)
    fetch('/add_menu', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Menu item added successfully!');
            // Optionally refresh the menu list or append the new item
        } else {
            alert('Error adding menu item.');
        }
    });
}

// Function to edit a menu item and submit the changes
function editMenuItem(event) {
    event.preventDefault(); // Prevent the form from refreshing the page
    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Make a POST request to update the menu item (adjust the URL accordingly)
    fetch('/edit_menu', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Menu item updated successfully!');
            // Optionally refresh the menu list or update the item in the list
        } else {
            alert('Error updating menu item.');
        }
    });
}

// Attach event listeners to forms (if needed)
document.addEventListener('DOMContentLoaded', function() {
    const studentForm = document.getElementById('student-form');
    if (studentForm) {
        studentForm.addEventListener('submit', addStudent);
    }

    const menuForm = document.getElementById('menu-form');
    if (menuForm) {
        menuForm.addEventListener('submit', addMenu);
    }

    const editMenuForm = document.getElementById('edit-menu-form');
    if (editMenuForm) {
        editMenuForm.addEventListener('submit', editMenuItem);
    }
});

function editInventory(itemId, itemName, quantity, price) {
    // Use the values passed in the parameters to populate the form
    document.getElementById('item_id').value = itemId;
    document.getElementById('item_name').value = itemName;
    document.getElementById('quantity').value = quantity;
    document.getElementById('price').value = price;
    // Display the edit form
    document.getElementById('edit-form').style.display = 'block';
}

function editMenu(menuId, menuName, menuPrice) {
    document.getElementById('menu-id').value = menuId;
    document.getElementById('menu-name').value = menuName;
    document.getElementById('menu-price').value = menuPrice;
}
