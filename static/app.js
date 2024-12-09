function deleteTask(taskId) {
    if (confirm("Are you sure you want to delete this task?")) {
        fetch(`/delete/${taskId}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                document.getElementById(`task-${taskId}`).remove();
            }
        });
    }
}

function editTask(taskId, currentTitle, currentDescription) {
    // Show the modal
    document.getElementById('editModal').style.display = 'block';

    // Fill the form with the current task data
    document.getElementById('edit-title').value = currentTitle;
    document.getElementById('edit-description').value = currentDescription;

    // Handle the form submission
    document.getElementById('edit-form').onsubmit = function(event) {
        event.preventDefault();

        // Get the updated values from the modal form
        const updatedTitle = document.getElementById('edit-title').value;
        const updatedDescription = document.getElementById('edit-description').value;

        // Send the updated data to the backend
        fetch(`/edit/${taskId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `title=${encodeURIComponent(updatedTitle)}&description=${encodeURIComponent(updatedDescription)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Update the task in the task list without reloading
                document.querySelector(`#task-${taskId} h3`).textContent = updatedTitle;
                document.querySelector(`#task-${taskId} p`).textContent = updatedDescription;
                
                // Close the modal
                closeEditModal();
            } else {
                console.error('Failed to update task');
            }
        })
        .catch(error => console.error('Error:', error));
    };
}

// Function to close the modal
function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

