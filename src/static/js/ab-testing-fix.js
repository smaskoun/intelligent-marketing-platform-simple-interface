/**
 * A/B Testing Results Module
 * Handles fetching and displaying A/B test results in a clean, reusable modal.
 */
class ABTestingModule {
    constructor() {
        this.apiBase = '/api/ab-testing';
        this.init();
    }

    /**
     * Initializes the module by setting up the main event listener.
     */
    init() {
        // Use a single, delegated event listener for better performance.
        document.addEventListener('click', this.handleDocumentClick.bind(this));
    }

    /**
     * Handles all clicks on the document to see if they are relevant to A/B testing.
     * @param {Event} e - The click event.
     */
    handleDocumentClick(e) {
        // Find the closest button with a 'data-action' attribute.
        const targetButton = e.target.closest('[data-action]');
        if (!targetButton) return;

        const action = targetButton.dataset.action;

        // If the action is to view results, find the test ID and fetch the data.
        if (action === 'view-ab-results') {
            e.preventDefault();
            e.stopPropagation();
            
            const testContainer = e.target.closest('[data-test-id]');
            if (testContainer && testContainer.dataset.testId) {
                this.fetchAndShowResults(testContainer.dataset.testId);
            } else {
                console.warn('Could not find test ID for the clicked "View Results" button.');
            }
        }
    }

    /**
     * Fetches the results for a given test ID and displays them.
     * @param {string} testId - The ID of the test to analyze.
     */
    async fetchAndShowResults(testId) {
        this.showModal('loading');
        try {
            const response = await fetch(`${this.apiBase}/analyze-results/${testId}`);
            const data = await response.json();

            if (response.ok && data.success) {
                this.showModal('results', data.data);
            } else {
                throw new Error(data.error || 'Failed to load test results.');
            }
        } catch (error) {
            console.error('Error fetching A/B test results:', error);
            this.showModal('error', { message: error.message });
        }
    }

    /**
     * Creates and displays a modal window.
     * @param {'loading' | 'results' | 'error'} type - The type of modal to show.
     * @param {object} data - The data to populate the modal with.
     */
    showModal(type, data = {}) {
        // Remove any existing modals first.
        this.removeModal();

        const modal = document.createElement('div');
        modal.id = 'ab-test-modal-container';
        modal.className = 'ab-modal-container';
        
        let modalContentHTML = '';
        switch (type) {
            case 'loading':
                modalContentHTML = this.getLoadingHTML();
                break;
            case 'results':
                modalContentHTML = this.getResultsHTML(data);
                break;
            case 'error':
                modalContentHTML = this.getErrorHTML(data);
                break;
        }

        modal.innerHTML = modalContentHTML;
        document.body.appendChild(modal);

        // Add a listener to the close button if it exists.
        const closeButton = modal.querySelector('.ab-modal-close');
        if (closeButton) {
            closeButton.addEventListener('click', () => this.removeModal());
        }
    }

    /**
     * Removes the modal from the DOM.
     */
    removeModal() {
        const modal = document.getElementById('ab-test-modal-container');
        if (modal) {
            modal.remove();
        }
    }

    // --- HTML Generation Methods ---

    getLoadingHTML() {
        return `
            <div class="ab-modal-content">
                <h3>Loading A/B Test Results...</h3>
                <div class="ab-spinner"></div>
            </div>
        `;
    }

    getErrorHTML(data) {
        return `
            <div class="ab-modal-content">
                <button class="ab-modal-close">✕</button>
                <h3 class="error-title">❌ Error</h3>
                <p>${data.message || 'An unknown error occurred.'}</p>
            </div>
        `;
    }

    getResultsHTML(data) {
        const variationsHTML = data.variations?.map(v => `
            <div class="ab-variation-card">
                <div class="ab-variation-header">
                    <h4>📄 Version ${v.version}</h4>
                    <button class="ab-copy-btn" data-content="${this.escapeHTML(v.content)}">📋 Copy</button>
                </div>
                <p class="ab-variation-strategy"><strong>Strategy:</strong> ${v.focus || v.approach}</p>
                <div class="ab-variation-content">${v.content}</div>
            </div>
        `).join('') || '<p>No variations available.</p>';

        const instructionsHTML = data.instructions?.map(i => `<li>${i}</li>`).join('') || `
            <li>Copy each variation and post it to your social media.</li>
            <li>Track engagement metrics (likes, comments, etc.).</li>
            <li>Note which version performs best and apply learnings.</li>
        `;

        return `
            <div class="ab-modal-content results">
                <button class="ab-modal-close">✕</button>
                <h2>🧪 A/B Test Results</h2>
                <h3>${data.test_name || 'Test Results'}</h3>
                <div class="ab-message-success">✅ ${data.message || 'Content variations are ready.'}</div>
                
                <h4>📝 Content Variations:</h4>
                <div class="ab-variations-container">${variationsHTML}</div>
                
                <div class="ab-instructions">
                    <h4>📋 Testing Instructions:</h4>
                    <ol>${instructionsHTML}</ol>
                </div>
            </div>
        `;
    }

    /**
     * Copies text to the clipboard and provides user feedback.
     * @param {HTMLElement} button - The button that was clicked.
     */
    copyToClipboard(button) {
        const content = button.dataset.content;
        navigator.clipboard.writeText(content).then(() => {
            const originalText = button.textContent;
            button.textContent = '✅ Copied!';
            button.disabled = true;
            setTimeout(() => {
                button.textContent = originalText;
                button.disabled = false;
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy text:', err);
            this.showModal('error', { message: 'Could not copy text to clipboard.' });
        });
    }

    /**
     * Escapes HTML characters to prevent issues when storing content in data attributes.
     * @param {string} str - The string to escape.
     */
    escapeHTML(str) {
        return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
    }
}

// Initialize the module when the DOM is loaded.
document.addEventListener('DOMContentLoaded', () => {
    window.abTestingModule = new ABTestingModule();
});
