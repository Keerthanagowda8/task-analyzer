// 1. Adds a new blank form to the page
    function addTaskForm() {
        const container = document.getElementById('task-list-container');
        
        const html = `
            <div class="task-input-box">
                <label>Task Title:</label>
                <input type="text" class="input-title" placeholder="e.g. Finish Assignment">
                
                <label>Due Date:</label>
                <input type="date" class="input-date">
                
                <label>Importance (1-10):</label>
                <input type="number" class="input-importance" min="1" max="10" value="5">
                
                <label>Effort (Hours):</label>
                <input type="number" class="input-hours" min="1" value="1">
                
                <button class="btn-remove" onclick="this.parentElement.remove()">Remove</button>
            </div>
        `;
        
        container.insertAdjacentHTML('beforeend', html);
    }

    // Add one empty box immediately when page loads
    addTaskForm();