/**
 * Content Management Module
 * Handles training the AI brand voice.
 */
class ContentManager {
    constructor() {
        this.apiBase = '/api';
        this.currentUser = 'default_user';
        this.init();
    }

    init() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        const addContentBtn = document.getElementById('add-content-btn');
        if (addContentBtn) {
            addContentBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.addTrainingContent();
            });
        }
    }

    async addTrainingContent() {
        const contentInput = document.getElementById('post-content-input');
        const imageUrlInput = document.getElementById('post-image-url');
        const typeSelect = document.getElementById('post-type-select');
        const addButton = document.getElementById('add-content-btn');

        if (!contentInput || !contentInput.value.trim()) {
            this.showNotification('Please enter the post text.', 'warning');
            return;
        }

        const trainingData = {
            user_id: this.currentUser,
            content: contentInput.value.trim(),
            image_url: imageUrlInput.value.trim() || null,
            post_type: typeSelect.value,
        };

        addButton.disabled = true;
        addButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Adding...';

        try {
            // This endpoint must match your backend route (e.g., in brand_voice_routes.py)
            const response = await fetch(`${this.apiBase}/brand-voice/train`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(trainingData),
            });

            const result = await response.json();
            if (response.ok && result.success) {
                this.showNotification('Content added to AI memory!', 'success');
                this.clearTrainingForm();
            } else {
                throw new Error(result.error || 'An unknown error occurred.');
            }
        } catch (error) {
            console.error('Error adding training content:', error);
            this.showNotification(`Failed to add content: ${error.message}`, 'error');
        } finally {
            addButton.disabled = false;
            addButton.innerHTML = '<i class="fas fa-plus mr-2"></i>Add Content to AI Memory';
        }
    }

    clearTrainingForm() {
        document.getElementById('post-content-input').value = '';
        document.getElementById('post-image-url').value = '';
        document.getElementById('post-type-select').value = 'listing';
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        const colors = {
            success: 'bg-green-500 text-white',
            error: 'bg-red-500 text-white',
            warning: 'bg-yellow-500 text-white',
        };
        notification.className = `fixed top-5 right-5 p-4 rounded-lg shadow-lg z-50 ${colors[type] || 'bg-blue-500 text-white'}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 5000);
    }
}

document.addEventListener('DOMContentLoaded', () => { window.contentManager = new ContentManager(); });
