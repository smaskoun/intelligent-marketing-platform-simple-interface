// A/B Testing Frontend Fix
console.log('Loading A/B Testing fix...');

// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    console.log('A/B Testing fix initialized');
    
    // Override View Results functionality
    document.addEventListener('click', function(e) {
        // Check if clicked element is View Results button
        if (e.target.textContent.includes('View Results') || 
            e.target.closest('button')?.textContent.includes('View Results')) {
            
            e.preventDefault();
            e.stopPropagation();
            
            console.log('View Results clicked - applying fix');
            
            // Get test ID from the test container
            const testContainer = e.target.closest('[data-test-id], .test-item, .test-card');
            let testId = null;
            
            if (testContainer) {
                testId = testContainer.dataset.testId || 
                        testContainer.getAttribute('data-test-id') ||
                        testContainer.querySelector('[data-test-id]')?.dataset.testId;
            }
            
            // Fallback: get all tests and use the first one
            if (!testId) {
                fetch('/api/ab-testing/tests')
                    .then(response => response.json())
                    .then(data => {
                        if (data.success && data.tests && data.tests.length > 0) {
                            testId = data.tests[0].id;
                            showABTestResults(testId);
                        }
                    });
                return;
            }
            
            showABTestResults(testId);
        }
        
        // Also handle View Details button
        if (e.target.textContent.includes('View Details')) {
            e.preventDefault();
            e.stopPropagation();
            
            // Trigger View Results instead
            const testContainer = e.target.closest('[data-test-id], .test-item, .test-card');
            const viewResultsBtn = testContainer?.querySelector('button:contains("View Results")') ||
                                 testContainer?.querySelector('[data-action="view-results"]');
            
            if (viewResultsBtn) {
                viewResultsBtn.click();
            }
        }
    });
});

// Function to show A/B test results
function showABTestResults(testId) {
    console.log('Fetching results for test ID:', testId);
    
    // Show loading
    showLoadingModal();
    
    // Fetch results from API
    fetch(`/api/ab-testing/analyze-results/${testId}`)
        .then(response => response.json())
        .then(data => {
            hideLoadingModal();
            
            if (data.success && data.data) {
                displayResultsModal(data.data);
            } else {
                showErrorModal('Failed to load test results: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            hideLoadingModal();
            console.error('Error fetching results:', error);
            showErrorModal('Error loading results: ' + error.message);
        });
}

// Show loading modal
function showLoadingModal() {
    removeExistingModals();
    
    const loadingHTML = `
        <div id="ab-loading-modal" style="
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.7); display: flex; justify-content: center; align-items: center;
            z-index: 10000; font-family: Arial, sans-serif;
        ">
            <div style="background: white; padding: 30px; border-radius: 10px; text-align: center;">
                <div style="font-size: 18px; margin-bottom: 15px;">Loading A/B Test Results...</div>
                <div style="width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #007bff; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto;"></div>
            </div>
        </div>
        <style>
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
    `;
    
    document.body.insertAdjacentHTML('beforeend', loadingHTML);
}

// Hide loading modal
function hideLoadingModal() {
    const modal = document.getElementById('ab-loading-modal');
    if (modal) modal.remove();
}

// Display results modal
function displayResultsModal(testData) {
    removeExistingModals();
    
    const modalHTML = `
        <div id="ab-results-modal" style="
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8); display: flex; justify-content: center; align-items: center;
            z-index: 10000; font-family: Arial, sans-serif;
        ">
            <div style="
                background: white; padding: 30px; border-radius: 12px; max-width: 900px; max-height: 85vh;
                overflow-y: auto; width: 90%; box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 style="color: #333; margin: 0;">🧪 A/B Test Results</h2>
                    <button onclick="document.getElementById('ab-results-modal').remove()" style="
                        background: #dc3545; color: white; border: none; padding: 8px 12px;
                        border-radius: 6px; cursor: pointer; font-size: 16px;
                    ">✕</button>
                </div>
                
                <h3 style="color: #666; margin-bottom: 15px;">${testData.test_name || 'Test Results'}</h3>
                
                <div style="background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                    <strong style="color: #155724;">✅ ${testData.message || 'Content variations are ready for testing'}</strong>
                </div>
                
                <h4 style="color: #333; margin-bottom: 20px;">📝 Content Variations:</h4>
                
                <div style="display: grid; gap: 20px; margin-bottom: 25px;">
                    ${testData.variations ? testData.variations.map((variation, index) => `
                        <div style="
                            border: 2px solid #e9ecef; padding: 20px; border-radius: 10px;
                            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
                            transition: transform 0.2s ease;
                        " onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                <h4 style="color: #007bff; margin: 0; font-size: 20px;">
                                    📄 Version ${variation.version}
                                </h4>
                                <button onclick="copyToClipboard('${variation.content.replace(/'/g, "\\'")}', this)" style="
                                    background: #28a745; color: white; border: none; padding: 8px 16px;
                                    border-radius: 6px; cursor: pointer; font-size: 14px; transition: background 0.2s;
                                " onmouseover="this.style.background='#218838'" onmouseout="this.style.background='#28a745'">
                                    📋 Copy Content
                                </button>
                            </div>
                            
                            <p style="color: #6c757d; font-style: italic; margin: 10px 0; font-size: 14px;">
                                <strong>Strategy:</strong> ${variation.focus || variation.approach}
                            </p>
                            
                            <div style="
                                background: white; padding: 18px; border-radius: 8px;
                                border-left: 5px solid #007bff; margin: 15px 0;
                                font-size: 16px; line-height: 1.6; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                            ">
                                ${variation.content}
                            </div>
                        </div>
                    `).join('') : '<p>No variations available</p>'}
                </div>
                
                <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <h4 style="color: #856404; margin: 0 0 15px 0;">📋 Testing Instructions:</h4>
                    <ol style="color: #856404; margin: 0; padding-left: 25px; line-height: 1.8;">
                        ${testData.instructions ? testData.instructions.map(instruction => 
                            `<li style="margin: 8px 0;">${instruction}</li>`
                        ).join('') : `
                            <li>Copy each variation above using the copy buttons</li>
                            <li>Post them to your social media at different times/days</li>
                            <li>Track engagement metrics (likes, comments, shares, saves)</li>
                            <li>Note which version performs best</li>
                            <li>Apply winning elements to future content strategy</li>
                        `}
                    </ol>
                </div>
                
                <div style="text-align: center; margin-top: 25px;">
                    <button onclick="document.getElementById('ab-results-modal').remove()" style="
                        background: #6c757d; color: white; border: none; padding: 12px 30px;
                        border-radius: 8px; cursor: pointer; font-size: 16px; transition: background 0.2s;
                    " onmouseover="this.style.background='#5a6268'" onmouseout="this.style.background='#6c757d'">
                        Close Results
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

// Show error modal
function showErrorModal(message) {
    removeExistingModals();
    
    const errorHTML = `
        <div id="ab-error-modal" style="
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.7); display: flex; justify-content: center; align-items: center;
            z-index: 10000; font-family: Arial, sans-serif;
        ">
            <div style="background: white; padding: 30px; border-radius: 10px; max-width: 500px; text-align: center;">
                <h3 style="color: #dc3545; margin-bottom: 15px;">❌ Error</h3>
                <p style="color: #333; margin-bottom: 20px;">${message}</p>
                <button onclick="document.getElementById('ab-error-modal').remove()" style="
                    background: #dc3545; color: white; border: none; padding: 10px 20px;
                    border-radius: 5px; cursor: pointer; font-size: 16px;
                ">Close</button>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', errorHTML);
}

// Remove existing modals
function removeExistingModals() {
    const modals = ['ab-results-modal', 'ab-loading-modal', 'ab-error-modal'];
    modals.forEach(id => {
        const modal = document.getElementById(id);
        if (modal) modal.remove();
    });
}

// Copy to clipboard function
function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text).then(() => {
        const originalText = button.textContent;
        button.textContent = '✅ Copied!';
        button.style.background = '#17a2b8';
        
        setTimeout(() => {
            button.textContent = originalText;
            button.style.background = '#28a745';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        button.textContent = '✅ Copied!';
        setTimeout(() => {
            button.textContent = '📋 Copy Content';
        }, 2000);
    });
}

console.log('✅ A/B Testing fix loaded successfully!');
