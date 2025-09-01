// static/js/ab-testing.js

class ABTestingModule {
    constructor() {
        this.apiBase = '/api/ab-testing';
        this.modal = null;
        this.init();
    }

    init() {
        // This event listener is on the whole document because the buttons are created dynamically.
        document.addEventListener('click', (e) => {
            if (e.target && e.target.classList.contains('create-ab-test-btn')) {
                this.handleCreateTestClick(e.target);
            }
        });
    }

    handleCreateTestClick(button) {
        const baseContent = JSON.parse(button.dataset.content);
        const testName = `A/B Test for "${baseContent.focus}"`;

        this.createTest(testName, baseContent);
    }

    async createTest(testName, baseContent) {
        this.showNotification('Creating A/B test variations...', 'info');

        try {
            const response = await fetch(`${this.apiBase}/create-test`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    test_name: testName,
                    base_content: baseContent,
                }),
            });

            const result = await response.json();
            if (!result.success) {
                throw new Error(result.error || 'Failed to create test.');
            }

            this.displayTestModal(result.test);

        } catch (error) {
            console.error('Error creating A/B test:', error);
            this.showNotification(`Error: ${error.message}`, 'error');
        }
    }

    displayTestModal(testData) {
        // First, remove any existing modal
        if (this.modal) {
            this.modal.remove();
        }

        let variationsHtml = testData.variations.map((v, i) => `
            <div class="variation-item">
                <h4>Variation ${String.fromCharCode(65 + i)}</h4>
                <p>${v.content.replace(/\n/g, '  
')}</p>
            </div>
        `).join('');

        const modalHtml = `
            <div class="ab-modal-overlay">
                <div class="ab-modal-content">
                    <button class="ab-modal-close">&times;</button>
                    <h3>${testData.name}</h3>
                    <p>Your A/B test variations are ready. Post these to your social media to see which performs best.</p>
                    <div class="variations-container">
                        ${variationsHtml}
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
        this.modal = document.querySelector('.ab-modal-overlay');

        this.modal.querySelector('.ab-modal-close').addEventListener('click', () => {
            this.modal.remove();
            this.modal = null;
        });
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        const colors = {
            success: 'bg-green-500 text-white',
            error: 'bg-red-500 text-white',
            warning: 'bg-yellow-500 text-white',
            info: 'bg-blue-500 text-white'
        };
        notification.className = `fixed top-5 right-5 p-4 rounded-lg shadow-lg z-50 ${colors[type] || 'bg-blue-500 text-white'}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 5000);
    }
}

// Initialize the module when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.abTestingModule = new ABTestingModule();
});
