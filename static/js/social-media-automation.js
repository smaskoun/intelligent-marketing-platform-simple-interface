/**
 * Content Platform Module
 * Handles AI training, content generation, A/B testing, and market data display.
 */
class ContentPlatform {
    constructor() {
        this.apiBase = '/api';
        this.currentUser = 'default_user';
        this.marketDataLoaded = false; // Flag to prevent multiple loads
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.handleInitialTab();
    }

    setupEventListeners() {
        // --- Tab Switching ---
        const tabs = document.querySelectorAll('.tab-button');
        tabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                this.switchTab(tab.hash);
            });
        });

        // --- "Train Brand Voice" form ---
        const addContentBtn = document.getElementById('add-content-btn');
        if (addContentBtn) {
            addContentBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.addTrainingContent();
            });
        }

        // --- "Generate Content" button ---
        const generateBtn = document.getElementById('generate-content-btn');
        if (generateBtn) {
            generateBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.generateContent();
            });
        }

        // --- Delegated listener for "Create A/B Test" buttons ---
        document.addEventListener('click', (e) => {
            if (e.target && e.target.classList.contains('create-ab-test-btn')) {
                e.preventDefault();
                this.handleCreateABTestClick(e.target);
            }
        });
    }

    // --- Tab Management ---

    handleInitialTab() {
        const initialTab = window.location.hash || '#train';
        this.switchTab(initialTab);
    }

    switchTab(tabHash) {
        document.querySelectorAll('.tab-content').forEach(panel => panel.classList.add('hidden'));
        document.querySelectorAll('.tab-button').forEach(button => button.classList.remove('active'));

        const activeTab = document.querySelector(`.tab-button[href="${tabHash}"]`);
        const activePanel = document.querySelector(`${tabHash}-content`);

        if (activeTab) activeTab.classList.add('active');
        if (activePanel) activePanel.classList.remove('hidden');

        history.pushState(null, null, tabHash);

        if (tabHash === '#market-data' && !this.marketDataLoaded) {
            this.fetchMarketData();
        }
    }

    // --- Market Data Methods ---

    async fetchMarketData() {
        this.marketDataLoaded = true;
        const container = document.getElementById('market-data-container');
        try {
            const response = await fetch(`${this.apiBase}/market-data`);
            const result = await response.json();
            if (response.ok && result.success) {
                this.displayMarketData(result.data);
            } else {
                throw new Error(result.error || 'Failed to fetch market data.');
            }
        } catch (error) {
            container.innerHTML = `<div class="text-red-500 p-4 bg-red-50 rounded-md col-span-3">Error: ${error.message}</div>`;
        }
    }

    displayMarketData(data) {
        const container = document.getElementById('market-data-container');
        const periodSpan = document.getElementById('market-data-period');
        if (periodSpan && data.report_period) {
            periodSpan.textContent = `Latest Data: ${data.report_period}`;
        }
        const formatChange = (change) => {
            if (!change) return '<span class="text-gray-500">-</span>';
            const isPositive = change.startsWith('+');
            const color = isPositive ? 'text-green-600' : 'text-red-600';
            const icon = isPositive ? 'fa-arrow-up' : 'fa-arrow-down';
            return `<span class="${color}"><i class="fas ${icon}"></i> ${change}</span>`;
        };
        container.innerHTML = `
            <div class="bg-gray-100 p-6 rounded-lg text-center"><h3 class="text-sm font-medium text-gray-500">Average Price</h3><p class="mt-1 text-3xl font-semibold text-gray-900">$${data.average_price.toLocaleString()}</p><p class="mt-2 text-sm">${formatChange(data.average_price_change)}</p></div>
            <div class="bg-gray-100 p-6 rounded-lg text-center"><h3 class="text-sm font-medium text-gray-500">Properties Sold</h3><p class="mt-1 text-3xl font-semibold text-gray-900">${data.properties_sold.toLocaleString()}</p><p class="mt-2 text-sm">${formatChange(data.properties_sold_change)}</p></div>
            <div class="bg-gray-100 p-6 rounded-lg text-center"><h3 class="text-sm font-medium text-gray-500">New Listings</h3><p class="mt-1 text-3xl font-semibold text-gray-900">${data.new_listings.toLocaleString()}</p><p class="mt-2 text-sm">${formatChange(data.new_listings_change)}</p></div>
        `;
    }

    // --- Training Brand Voice Methods ---

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

    // --- Content Generation Methods ---

    async generateContent() {
        const topicInput = document.getElementById('generator-topic');
        const typeSelect = document.getElementById('generator-type');
        const generateButton = document.getElementById('generate-content-btn');
        const resultsContainer = document.getElementById('generator-results');
        if (!topicInput || !topicInput.value.trim()) {
            this.showNotification('Please enter a topic.', 'warning');
            return;
        }
        generateButton.disabled = true;
        generateButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Generating...';
        resultsContainer.innerHTML = '<div class="text-center text-gray-500 p-4">Generating content, please wait...</div>';
        try {
            const response = await fetch(`${this.apiBase}/learning/content-recommendations?topic=${encodeURIComponent(topicInput.value)}&content_type=${typeSelect.value}`);
            const result = await response.json();
            if (response.ok && result.success) {
                this.displayResults(result);
            } else {
                throw new Error(result.error || 'Failed to generate content.');
            }
        } catch (error) {
            this.showNotification(`Failed to generate content: ${error.message}`, 'error');
            resultsContainer.innerHTML = `<div class="text-red-500 p-4 bg-red-50 rounded-md">Error: ${error.message}</div>`;
        } finally {
            generateButton.disabled = false;
            generateButton.innerHTML = '<i class="fas fa-magic mr-2"></i>Generate Content';
        }
    }

    displayResults(data) {
        const resultsContainer = document.getElementById('generator-results');
        if (!resultsContainer) return;

        if (data.error) {
            resultsContainer.innerHTML = `<div class="text-red-500 p-4 bg-red-50 rounded-md">${data.error}</div>`;
            return;
        }

        // --- THIS IS THE UPDATED PART ---
        resultsContainer.innerHTML = data.recommendations.map(rec => {
            const scoreColor = rec.seo_score >= 75 ? 'text-green-600' : rec.seo_score >= 50 ? 'text-yellow-600' : 'text-red-600';
            const recommendationsHtml = rec.seo_recommendations.map(r => `<li>${r}</li>`).join('');

            return `
                <div class="bg-white p-4 rounded-lg shadow mb-4">
                    <p class="text-gray-800 whitespace-pre-wrap">${rec.content}</p>
                    
                    <!-- SEO Score and Recommendations -->
                    <div class="mt-4 pt-4 border-t border-gray-200">
                        <div class="flex justify-between items-center">
                            <h4 class="text-sm font-semibold text-gray-700">SEO Analysis</h4>
                            <div class="text-sm font-bold ${scoreColor}">
                                Score: ${rec.seo_score}/100
                            </div>
                        </div>
                        <ul class="text-xs text-gray-600 mt-2 list-disc list-inside">
                            ${recommendationsHtml}
                        </ul>
                    </div>

                    <div class="mt-3 flex justify-between items-center">
                        <div class="text-sm text-gray-500">
                            <strong>Focus:</strong> ${rec.focus}
                        </div>
                        <button 
                            class="create-ab-test-btn bg-purple-500 text-white px-3 py-1 rounded-md text-sm hover:bg-purple-600 transition-colors"
                            data-content="${encodeURIComponent(rec.content)}"
                            data-hashtags="${encodeURIComponent(JSON.stringify(rec.hashtags))}"
                            data-focus="${rec.focus}"
                        >
                            <i class="fas fa-vial mr-1"></i> Create A/B Test
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    // --- A/B Testing Methods ---

    handleCreateABTestClick(button) {
        const baseContent = {
            content: decodeURIComponent(button.dataset.content),
            hashtags: JSON.parse(decodeURIComponent(button.dataset.hashtags)),
            focus: button.dataset.focus
        };
        this.createABTest(baseContent);
    }

    async createABTest(baseContent) {
        this.showNotification('Creating A/B test variations...', 'info');
        const payload = {
            test_name: `Test for "${baseContent.focus}"`,
            base_content: baseContent,
            variation_types: ['hooks', 'cta_styles'],
            platform: 'instagram'
        };
        try {
            const response = await fetch(`${this.apiBase}/ab-testing/create`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            const result = await response.json();
            if (response.ok && result.success) {
                if (window.abTesting && typeof window.abTesting.displayResultsModal === 'function') {
                    window.abTesting.displayResultsModal(result.data);
                } else {
                    this.showNotification('A/B Test created, but cannot display results.', 'warning');
                }
            } else {
                throw new Error(result.error || 'Failed to create A/B test.');
            }
        } catch (error) {
            this.showNotification(`Failed to create A/B test: ${error.message}`, 'error');
        }
    }

    // --- Utility Methods ---

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        const colors = {
            success: 'bg-green-500 text-white',
            error: 'bg-red-500 text-white',
            warning: 'bg-yellow-500 text-white',
            info: 'bg-blue-500 text-white',
        };
        notification.className = `fixed top-5 right-5 p-4 rounded-lg shadow-lg z-50 ${colors[type] || 'bg-gray-500 text-white'}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 5000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.contentPlatform = new ContentPlatform();
});
