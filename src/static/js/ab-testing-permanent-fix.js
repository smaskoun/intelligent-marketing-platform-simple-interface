// Permanent A/B Testing Fix
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Loading permanent A/B testing fix...');
    
    // Fix for View Results and View Details buttons
    document.addEventListener('click', function(e) {
        if (e.target.textContent && (
            e.target.textContent.includes('View Results') || 
            e.target.textContent.includes('View Details')
        )) {
            e.preventDefault();
            e.stopPropagation();
            
            console.log('🎯 A/B Testing button clicked');
            
            // Get test ID from the test container
            const testContainer = e.target.closest('.test-container') || e.target.closest('[data-test-id]');
            let testId = null;
            
            // Try to find test ID from various sources
            if (testContainer) {
                testId = testContainer.getAttribute('data-test-id');
            }
            
            // Fallback: use the most recent test ID (you can update this)
            if (!testId) {
                testId = '6957f992-8ec6-410b-b282-762d68b6c04d'; // Your latest test
            }
            
            console.log('📡 Fetching results for:', testId);
            
            // Show loading
            showABLoading();
            
            // Fetch results
            fetch(`/api/ab-testing/analyze-results/${testId}`)
                .then(response => response.json())
                .then(data => {
                    hideABLoading();
                    console.log('✅ API Response:', data);
                    
                    if (data.success && data.data) {
                        showABResults(data.data);
                    } else {
                        alert('Error: ' + (data.error || 'Failed to load results'));
                    }
                })
                .catch(error => {
                    hideABLoading();
                    console.error('❌ Error:', error);
                    alert('Error: ' + error.message);
                });
        }
    });
    
    // Loading function
    function showABLoading() {
        removeABModals();
        document.body.insertAdjacentHTML('beforeend', `
            <div id="ab-loading" style="position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.8);display:flex;justify-content:center;align-items:center;z-index:99999;font-family:Arial,sans-serif;">
                <div style="background:white;padding:30px;border-radius:10px;text-align:center;">
                    <h3>🔄 Loading A/B Test Results...</h3>
                    <div style="margin:20px 0;">Please wait...</div>
                </div>
            </div>
        `);
    }
    
    // Hide loading
    function hideABLoading() {
        const loading = document.getElementById('ab-loading');
        if (loading) loading.remove();
    }
    
    // Show results function
    function showABResults(data) {
        removeABModals();
        
        let variationsHTML = '';
        if (data.variations && data.variations.length > 0) {
            variationsHTML = data.variations.map(v => `
                <div style="border:2px solid #ddd;margin:15px 0;padding:20px;border-radius:8px;background:#f9f9f9;">
                    <h4 style="color:#007bff;margin:0 0 10px 0;">📄 Version ${v.version}</h4>
                    <p style="color:#666;margin:5px 0;"><strong>Strategy:</strong> ${v.focus || v.approach}</p>
                    <div style="background:white;padding:15px;border-radius:5px;margin:10px 0;border-left:4px solid #007bff;font-size:16px;">
                        ${v.content}
                    </div>
                    <button onclick="copyABText('${v.content.replace(/'/g, "\\'")}', this)" style="background:#28a745;color:white;border:none;padding:8px 16px;border-radius:4px;cursor:pointer;">📋 Copy Content</button>
                </div>
            `).join('');
        } else {
            variationsHTML = '<p>No variations found</p>';
        }
        
        const modalHTML = `
            <div id="ab-results" style="position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.8);display:flex;justify-content:center;align-items:center;z-index:99999;font-family:Arial,sans-serif;">
                <div style="background:white;padding:30px;border-radius:10px;max-width:800px;max-height:80vh;overflow-y:auto;width:90%;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                        <h2 style="margin:0;color:#333;">🧪 A/B Test Results</h2>
                        <button onclick="removeABModals()" style="background:#dc3545;color:white;border:none;padding:8px 12px;border-radius:4px;cursor:pointer;font-size:16px;">✕</button>
                    </div>
                    
                    <h3 style="color:#666;margin-bottom:15px;">${data.test_name || 'Test Results'}</h3>
                    
                    <div style="background:#d4edda;padding:15px;border-radius:8px;margin-bottom:20px;color:#155724;">
                        <strong>✅ ${data.message || 'Content variations ready for testing'}</strong>
                    </div>
                    
                    <h4 style="color:#333;margin-bottom:15px;">📝 Content Variations:</h4>
                    ${variationsHTML}
                    
                    <div style="text-align:center;margin-top:20px;">
                        <button onclick="removeABModals()" style="background:#6c757d;color:white;border:none;padding:12px 24px;border-radius:6px;cursor:pointer;font-size:16px;">Close</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }
    
    // Remove modals function
    function removeABModals() {
        ['ab-results', 'ab-loading'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.remove();
        });
    }
    
    console.log('✅ Permanent A/B Testing fix loaded!');
});

// Copy function (global scope)
function copyABText(text, button) {
    navigator.clipboard.writeText(text).then(() => {
        button.textContent = '✅ Copied!';
        button.style.background = '#17a2b8';
        setTimeout(() => {
            button.textContent = '📋 Copy Content';
            button.style.background = '#28a745';
        }, 2000);
    }).catch(() => {
        // Fallback
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        button.textContent = '✅ Copied!';
        setTimeout(() => {
            button.textContent = '📋 Copy Content';
        }, 2000);
    });
}

// Remove modals function (global scope)
function removeABModals() {
    ['ab-results', 'ab-loading'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.remove();
    });
}
