// 1. Helper to clear error style immediately when user types
        function clearError(input) {
            input.style.border = "1px solid #ddd";
            // Also hide the global error message if it exists
            const errorMsg = document.getElementById('error-message');
            if(errorMsg) errorMsg.style.display = 'none';
        }

        // 2. Add Task Form (Updated with 'oninput' triggers)
        function addTaskForm() {
            const container = document.getElementById('task-list-container');
            
            // Note the new 'oninput="clearError(this)"' attribute in every input
            const html = `
                <div class="task-input-box">
                    <label>Task Title:</label>
                    <input type="text" class="input-title" placeholder="e.g. Finish Assignment" 
                           oninput="clearError(this)">
                    
                    <label>Due Date:</label>
                    <input type="date" class="input-date" 
                           oninput="clearError(this)">
                    
                    <label>Importance (1-10):</label>
                    <input type="number" class="input-importance" min="1" max="10" value="5" 
                           oninput="clearError(this)">
                    
                    <label>Effort (Hours):</label>
                    <input type="number" class="input-hours" min="1" value="1" 
                           oninput="clearError(this)">
                    
                    <button class="btn-remove" onclick="this.parentElement.remove()">Remove</button>
                </div>
            `;
            container.insertAdjacentHTML('beforeend', html);
        }

        // 3. Analyze Logic (Updated to use on-screen errors)
        async function analyzeTasks() {
            const resultsArea = document.getElementById('resultsArea');
            resultsArea.innerHTML = ''; // Clear previous results

            const taskBoxes = document.querySelectorAll('.task-input-box');
            const tasksList = [];
            let hasError = false;

            // Loop through every box
            taskBoxes.forEach(box => {
                const titleInput = box.querySelector('.input-title');
                const dateInput = box.querySelector('.input-date');
                const impInput = box.querySelector('.input-importance');
                const hoursInput = box.querySelector('.input-hours');

                const title = titleInput.value.trim();
                const date = dateInput.value;
                const imp = impInput.value;
                const hours = hoursInput.value;

                let boxIsValid = true;

                // Check Title
                if (!title) {
                    titleInput.style.border = "2px solid #ff4444"; // Red border
                    boxIsValid = false;
                }
                
                // Check Date
                if (!date) {
                    dateInput.style.border = "2px solid #ff4444";
                    boxIsValid = false;
                }

                if (!boxIsValid) {
                    hasError = true;
                } else {
                    tasksList.push({
                        "title": title,
                        "due_date": date,
                        "importance": parseInt(imp),
                        "estimated_hours": parseInt(hours)
                    });
                }
            });

            // ERROR HANDLING: Show message on screen (No Alert!)
            if (hasError) {
                resultsArea.innerHTML = `
                    <div id="error-message" style="background:#ffe6e6; color:#cc0000; padding:15px; border-radius:5px; border:1px solid #ffcccc;">
                        <strong>⚠ Missing Information</strong><br>
                        Please fill in the highlighted fields to proceed.
                    </div>
                `;
                return; // Stop here
            }

            if (tasksList.length === 0) {
                resultsArea.innerHTML = <p style="color:orange">Please add at least one task.</p>;
                return;
            }

            // SUCCESS: Send to Backend
            try {
                resultsArea.innerHTML = '<p style="color:#666">Analyzing...</p>'; // Loading state
                
                const response = await fetch('http://127.0.0.1:8000/api/tasks/analyze/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(tasksList)
                });

                if (!response.ok) throw new Error("Server Error");

                const sortedTasks = await response.json();
                displayResults(sortedTasks);
            } catch (error) {
                resultsArea.innerHTML = <p style="color:red">Connection Error: Is the backend running?</p>;
            }
        }

        function displayResults(tasks) {
            const container = document.getElementById('resultsArea');
            container.innerHTML = '<h2>🎯 Prioritized List</h2>';

            tasks.forEach(task => {
                let color = '#00C851'; // Green
                if (task.score > 80) color = '#ff4444'; // Red
                else if (task.score > 40) color = '#ffbb33'; // Orange

                const card = `
                    <div style="border-left: 5px solid ${color}; background: #fff; padding: 15px; margin-bottom: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                        <div style="float:right; background:#333; color:white; padding:2px 8px; border-radius:10px; font-size:0.8em;">
                            Score: ${task.score}
                        </div>
                        <h3 style="margin:0 0 5px 0;">${task.title}</h3>
                        <p style="margin:0; font-size:0.9em; color:#666;">
                            Due: ${task.due_date} | Imp: ${task.importance} | Effort: ${task.estimated_hours}h
                        </p>
                    </div>
                `;
                container.innerHTML += card;
            });
        }

        // Initialize with one form
        addTaskForm();