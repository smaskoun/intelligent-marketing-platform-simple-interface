/**
 * Content Management Module
 * Handles training the AI brand voice and managing generated content.
 */

class ContentManager {
    constructor() {
        // The base URL for your API endpoints.
        this.apiBase = '/api'; 
        
        // A placeholder for the current user. In a real app, you'd get this from a login system.
        this.currentUser = 'default_user'; 

        // Start the application logic.
        this.init();
    }

    /**
     * Initializes the page by setting up event listeners.
     */
    init() {
        this.setupEventListeners();
    }

    /**
     * Sets up all the necessary click handlers for the page.
     */
    setupEventListeners() {
        // Find the "Add Content to AI Memory" button.
        const addContentBtn = document.getElementById('add-content-btn');
        
        // If the button exists, listen for clicks and call the addTrainingContent method.
        if (addContentBtn) {
            addContentBtn.addEventListener('click', (e) => {
                e.preventDefault(); // Prevent the form from submitting in the traditional way
                this.addTrainingContent();
            });
        }

        // We can add listeners for the "Manage Content" tab here later.
        // For example, for deleting or editing training data.
    }

    /**
     * Gathers data from the "Train Brand Voice" form and sends it to the backend.
     */
    async addTrainingContent() {
        // Get the data from the form fields.
        const contentInput = document.getElementById('post-content-input');
        const imageUrlInput = document.getElementById('post-image-url');
        const typeSelect = document.getElementById('post-type-select');
        const addButton = document.getElementById('add-content-btn');

        // --- Input Validation ---
        // Check if the main content text area is empty.
        if (!contentInput || !contentInput.value.trim()) {
            this.showNotification('Please enter the post text to add.', 'warning');
            return; // Stop the function if validation fails.
        }

        // Prepare the data payload to send to the backend.
        const trainingData = {
            user_id: this.currentUser,
            content: contentInput.value.trim(),
            image_url: imageUrlInput.value.trim() || null, // Send null if the URL is empty.
            post_type: typeSelect.value,
        };

        // --- API Call ---
        // Disable the button to prevent multiple clicks while processing.
        addButton.disabled = true;
        addButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Adding...';

        try {
            // Use the fetch API to send a POST request to your backend endpoint.
            // IMPORTANT: You might need to change '/train-voice' to your actual backend endpoint URL.
            const response = await fetch(`${this.apiBase}/train-voice`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(trainingData),
            });

            const result = await response.json();

            // If the backend signals success...
            if (response.ok && result.success) {
                this.showNotification('Content added to AI memory successfully!', 'success');
                this.clearTrainingForm(); // Clear the form for the next entry.
            } else {
                // If the backend gives an error, show it.
                throw new Error(result.error || 'An unknown error occurred.');
            }
        } catch (error) {
            // If the network request itself fails, show an error.
            console.error('Error adding training content:', error);
            this.showNotification(`Failed to add content: ${error.message}`, 'error');
        } finally {
            // Re-enable the button whether the request succeeded or failed.
            addButton.disabled = false;
            addButton.innerHTML = '<i class="fas fa-plus mr-2"></i>Add Content to AI Memory';
        }
    }

    /**
     * Clears the input fields in the training form.
     */
    clearTrainingForm() {
        document.getElementById('post-content-input').value = '';
        document.getElementById('post-image-url').value = '';
        document.getElementById('post-type-select').value = 'listing'; // Reset to default.
    }

    /**
     * Displays a temporary notification message on the screen.
     * @param {string} message - The message to display.
     * @param {string} type - The type of notification ('success', 'error', 'warning').
     */
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        const colors = {
            success: 'bg-green-500 text-white',
            error: 'bg-red-500 text-white',
            warning: 'bg-yellow-500 text-white',
            info: 'bg-blue-500 text-white',
        };
        notification.className = `fixed top-5 right-5 p-4 rounded-lg shadow-lg z-50 transition-transform transform translate-x-full ${colors[type] || colors.info}`;
        notification.textContent = message;
        document.body.appendChild(notification);

        // Animate the notification in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 10);

        // Animate it out and remove it after 5 seconds
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            notification.addEventListener('transitionend', () => notification.remove());
        }, 5000);
    }
}

// When the entire page is loaded, create an instance of our ContentManager class.
document.addEventListener('DOMContentLoaded', () => {
    window.contentManager = new ContentManager();
});
