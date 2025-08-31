// React-specific A/B Testing Fix
// This script specifically targets React component interactions

(function() {
    'use strict';
    
    console.log('🔧 Loading React A/B Testing Fix...');
    
    // Wait for React to fully render
    function waitForReact() {
        if (window.React || document.querySelector('[data-reactroot]') || document.getElementById('root').children.length > 0) {
            console.log('✅ React detected, initializing fix...');
            initReactFix();
        } else {
            console.log('⏳ Waiting for React...');
            setTimeout(waitForReact, 500);
        }
    }
    
    // Start waiting for React
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', waitForReact);
    } else {
        waitForReact();
    }
    
    function initReactFix() {
        // Override React's event handling for A/B testing
        interceptReactEvents();
        
        // Monitor for React re-renders
        observeReactChanges();
        
        // Add global event delegation
        addGlobalEventDelegation();
    }
    
    function interceptReactEvents() {
        // Intercept all button clicks in the A/B testing section
        document.addEventListener('click', function(e) {
            const target = e.target;
            
            // Check if we're in the A/B testing section
            const abSection = target.closest('[class*="ab-test"], [class*="testing"]') || 
                             (target.textContent && (
                                 target.textContent.includes('Create A/B Test') ||
                                 target.textContent.includes('View Details') ||
                                 target.textContent.includes('Start Test')
                             ));
            
            if (!abSection && !target.textContent) return;
            
            // Handle Create A/B Test
            if (target.textContent && target.textContent.includes('Create A/B Test')) {
                console.log('🎯 Intercepted Create A/B Test click');
                e.preventDefault();
                e.stopPropagation();
                handleCreateABTest();
                return false;
            }
            
            // Handle View Details
            if (target.textContent && target.textContent.includes('View Details')) {
                console.log('🎯 Intercepted View Details click');
                e.preventDefault();
                e.stopPropagation();
                handleViewDetails();
                return false;
            }
            
            // Handle Start Test
            if (target.textContent && target.textContent.includes('Start Test')) {
                console.log('🎯 Intercepted Start Test click');
                e.preventDefault();
                e.stopPropagation();
                handleStartTest();
                return false;
            }
        }, true); // Use capture phase to intercept before React
    }
    
    function handleCreateABTest() {
        console.log('📝 Creating A/B Test...');
        
        // Collect form data from React inputs
        const formData = collectReactFormData();
        
        if (!formData.name || formData.name.trim() === '') {
            showAlert('Please enter a test name', 'warning');
            return;
        }
        
        showLoading('Creating A/B Test...');
        
        // Make API call
        fetch('/api/ab-testing/create-test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            console.log('📡 API Response status:', response.status);
            return response.json();
        })
        .then(data => {
            hideLoading();
            console.log('✅ Test creation response:', data);
            
            if (data.success) {
                showAlert('A/B Test created successfully!', 'success');
                // Switch to Active Tests tab
                setTimeout(() => {
                    const activeTestsTab = Array.from(document.querySelectorAll('button')).find(btn => 
                        btn.textContent.includes('Active Tests')
                    );
                    if (activeTestsTab) activeTestsTab.click();
                }, 1000);
            } else {
                showAlert('Error creating test: ' + (data.error || 'Unknown error'), 'error');
            }
        })
        .catch(error => {
            hideLoading();
            console.error('❌ Error creating test:', error);
            showAlert('Error creating test: ' + error.message, 'error');
        });
    }
    
    function collectReactFormData() {
        // Find React form inputs
        const inputs = document.querySelectorAll('input, select, textarea');
        const formData = {
            name: '',
            content_type: 'property_showcase',
            platform: 'instagram',
            location: 'Windsor',
            test_elements: [],
            variations_count: 3
        };
        
        inputs.forEach(input => {
            const label = input.previousElementSibling || input.closest('label') || 
                         document.querySelector(`label[for="${input.id}"]`);
            const labelText = label ? label.textContent.toLowerCase() : '';
            
            if (input.type === 'text' || input.type === 'email') {
                if (labelText.includes('test name') || input.placeholder.includes('Hook Optimization')) {
                    formData.name = input.value || 'Frontend Fix Test';
                } else if (labelText.includes('location') || input.placeholder.includes('Windsor')) {
                    formData.location = input.value || 'Windsor';
                }
            } else if (input.tagName === 'SELECT') {
                if (labelText.includes('content type') || input.innerHTML.includes('Property Showcase')) {
                    formData.content_type = input.value || 'property_showcase';
                } else if (labelText.includes('platform') || input.innerHTML.includes('Instagram')) {
                    formData.platform = input.value || 'instagram';
                }
            } else if (input.type === 'checkbox' && input.checked) {
                const checkboxLabel = input.closest('label') || input.nextElementSibling;
                if (checkboxLabel) {
                    const text = checkboxLabel.textContent.toLowerCase();
                    if (text.includes('hook')) formData.test_elements.push('hooks');
                    if (text.includes('call-to-action')) formData.test_elements.push('cta');
                    if (text.includes('emoji')) formData.test_elements.push('emoji');
                    if (text.includes('hashtag')) formData.test_elements.push('hashtags');
                }
            }
        });
        
        // Default to hooks if nothing selected
        if (formData.test_elements.length === 0) {
            formData.test_elements = ['hooks'];
        }
        
        console.log('📋 Collected React form data:', formData);
        return formData;
    }
    
    function handleViewDetails() {
        console.log('👁️ Viewing test details...');
        
        showLoading('Loading Test Details...');
        
        // Get the most recent test
        fetch('/api/ab-testing/tests')
            .then(response => response.json())
            .then(data => {
                if (data.success && data.tests && data.tests.length > 0) {
                    const testId = data.tests[data.tests.length - 1].id;
                    return fetch(`/api/ab-testing/analyze-results/${testId}`);
                } else {
                    throw new Error('No tests found');
                }
            })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                console.log('✅ Test details loaded:', data);
                
                if (data.success && data.data) {
                    showResultsModal(data.data);
                } else {
                    showAlert('Error loading test details: ' + (data.error || 'Unknown error'), 'error');
                }
            })
            .catch(error => {
                hideLoading();
                console.error('❌ Error loading test details:', error);
                showAlert('Error loading test details: ' + error.message, 'error');
            });
    }
    
    function handleStartTest() {
        console.log('▶️ Starting test...');
        
        showLoading('Starting Test...');
        
        // Get the most recent test and start it
        fetch('/api/ab-testing/tests')
            .then(response => response.json())
            .then(data => {
                if (data.success && data.tests && data.tests.length > 0) {
                    const testId = data.tests[data.tests.length - 1].id;
                    return fetch(`/api/ab-testing/start-test/${testId}`, { method: 'POST' });
                } else {
                    throw new Error('No tests found to start');
                }
            })
            .then(response => response.json())
            .then(data => {
                hideLoading();
                console.log('✅ Test started:', data);
                
                if (data.success) {
                    showAlert('Test started successfully!', 'success');
                } else {
                    showAlert('Error starting test: ' + (data.error || 'Unknown error'), 'error');
                }
            })
            .catch(error => {
                hideLoading();
                console.error('❌ Error starting test:', error);
                showAlert('Error starting test: ' + error.message, 'error');
            });
    }
    
    function addGlobalEventDelegation() {
        // Add global click handler for any A/B testing related buttons
        document.body.addEventListener('click', function(e) {
            const target = e.target;
            
            // Skip if already handled
            if (target.dataset.abFixed) return;
            
            // Mark as handled
            target.dataset.abFixed = 'true';
            
            // Handle based on button text
            if (target.tagName === 'BUTTON') {
                const text = target.textContent.trim();
                
                if (text.includes('Create A/B Test') || text.includes('Create Test')) {
                    e.preventDefault();
                    e.stopPropagation();
                    setTimeout(() => handleCreateABTest(), 10);
                } else if (text.includes('View Details') || text.includes('View Results')) {
                    e.preventDefault();
                    e.stopPropagation();
                    setTimeout(() => handleViewDetails(), 10);
                } else if (text.includes('Start Test') || text.includes('Start')) {
                    e.preventDefault();
                    e.stopPropagation();
                    setTimeout(() => handleStartTest(), 10);
                }
            }
        }, true);
    }
    
    function observeReactChanges() {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    // Re-apply fixes when React re-renders
                    setTimeout(() => {
                        addGlobalEventDelegation();
                    }, 100);
                }
            });
        });
        
        const root = document.getElementById('root');
        if (root) {
            observer.observe(root, {
                childList: true,
                subtree: true
            });
        }
    }
    
    function showResultsModal(data) {
        removeModals();
        
        let variationsHTML = '';
        if (data.variations && data.variations.length > 0) {
            variationsHTML = data.variations.map((variation, index) => `
                <div style="border: 2px solid #e9ecef; margin: 15px 0; padding: 20px; border-radius: 8px; background: #f8f9fa;">
                    <h4 style="color: #007bff; margin: 0 0 10px 0;">
                        <span style="background: #007bff; color: white; width: 30px; height: 30px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-right: 10px;">
                            ${String.fromCharCode(65 + index)}
                        </span>
                        Version ${String.fromCharCode(65 + index)}
                    </h4>
                    <div style="background: white; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #007bff; font-size: 16px; line-height: 1.5;">
                        ${variation.content}
                    </div>
                    <button onclick="copyContent('${variation.content.replace(/'/g, "\\'")}', this)" 
                            style="background: #28a745; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; margin-right: 10px;">
                        📋 Copy Content
                    </button>
                </div>
            `).join('');
        } else {
            variationsHTML = '<div style="text-align: center; padding: 40px; color: #666;"><h4>📭 No variations found</h4><p>The test may still be generating content.</p></div>';
        }
        
        const modalHTML = `
            <div id="ab-results-modal" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: flex; justify-content: center; align-items: center; z-index: 99999; font-family: Arial, sans-serif;">
                <div style="background: white; padding: 30px; border-radius: 12px; max-width: 900px; max-height: 85vh; overflow-y: auto; width: 90%; box-shadow: 0 8px 32px rgba(0,0,0,0.3);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; border-bottom: 2px solid #f8f9fa; padding-bottom: 15px;">
                        <h2 style="margin: 0; color: #333; display: flex; align-items: center;">
                            <span style="margin-right: 10px;">🧪</span>
                            A/B Test Results
                        </h2>
                        <button onclick="removeModals()" style="background: #dc3545; color: white; border: none; padding: 8px 12px; border-radius: 6px; cursor: pointer; font-size: 16px;">✕</button>
                    </div>
                    
                    <h3 style="color: #666; margin-bottom: 15px;">${data.test_name || 'Content Variations'}</h3>
                    
                    <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); padding: 15px; border-radius: 8px; margin-bottom: 20px; color: #155724; border-left: 4px solid #28a745;">
                        <strong>✅ ${data.message || 'Content variations ready for manual testing'}</strong>
                    </div>
                    
                    <h4 style="color: #333; margin-bottom: 15px; display: flex; align-items: center;">
                        <span style="margin-right: 8px;">📝</span>
                        Content Variations (${data.variations ? data.variations.length : 0}):
                    </h4>
                    ${variationsHTML}
                    
                    <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; color: #856404; border-left: 4px solid #ffc107;">
                        <h4 style="margin: 0 0 10px 0; display: flex; align-items: center;">
                            <span style="margin-right: 8px;">📋</span>
                            Testing Instructions:
                        </h4>
                        <ol style="color: #666; line-height: 1.6;">
                            <li style="margin: 5px 0;">Copy each variation using the copy buttons</li>
                            <li style="margin: 5px 0;">Post them to your social media at different times</li>
                            <li style="margin: 5px 0;">Track engagement metrics (likes, comments, shares)</li>
                            <li style="margin: 5px 0;">Note which version performs best</li>
                            <li style="margin: 5px 0;">Use winning elements in future content</li>
                        </ol>
                    </div>
                    
                    <div style="text-align: center; margin-top: 25px; padding-top: 20px; border-top: 1px solid #eee;">
                        <button onclick="removeModals()" style="background: #6c757d; color: white; border: none; padding: 12px 30px; border-radius: 8px; cursor: pointer; font-size: 16px;">Close</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }
    
    function collectReactFormData() {
        const formData = {
            name: 'Frontend Fix Test',
            content_type: 'property_showcase',
            platform: 'instagram',
            location: 'Windsor',
            test_elements: ['hooks'],
            variations_count: 3
        };
        
        // Try to get actual form values
        const nameInput = document.querySelector('input[placeholder*="Hook"], input[placeholder*="test"]');
        if (nameInput && nameInput.value) {
            formData.name = nameInput.value;
        }
        
        const locationInput = document.querySelector('input[placeholder="Windsor"]');
        if (locationInput && locationInput.value) {
            formData.location = locationInput.value;
        }
        
        // Get selected options from selects
        const selects = document.querySelectorAll('select');
        selects.forEach((select, index) => {
            if (index === 0) { // First select is content type
                formData.content_type = select.value || 'property_showcase';
            } else if (index === 1) { // Second select is platform
                formData.platform = select.value || 'instagram';
            }
        });
        
        // Get checked test elements
        const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
        if (checkboxes.length > 0) {
            formData.test_elements = [];
            checkboxes.forEach(checkbox => {
                const label = checkbox.closest('label') || checkbox.nextElementSibling;
                if (label) {
                    const text = label.textContent.toLowerCase();
                    if (text.includes('hook')) formData.test_elements.push('hooks');
                    if (text.includes('call-to-action')) formData.test_elements.push('cta');
                    if (text.includes('emoji')) formData.test_elements.push('emoji');
                    if (text.includes('hashtag')) formData.test_elements.push('hashtags');
                }
            });
        }
        
        console.log('📋 Collected form data:', formData);
        return formData;
    }
    
    function observeReactChanges() {
        const observer = new MutationObserver(function(mutations) {
            let shouldReapplyFix = false;
            
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    // Check if A/B testing content was added
                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === 1 && (
                            node.textContent.includes('A/B Test') ||
                            node.textContent.includes('Create Test') ||
                            node.querySelector && node.querySelector('button')
                        )) {
                            shouldReapplyFix = true;
                        }
                    });
                }
            });
            
            if (shouldReapplyFix) {
                setTimeout(() => {
                    console.log('🔄 React re-rendered, reapplying fixes...');
                    interceptReactEvents();
                }, 200);
            }
        });
        
        const root = document.getElementById('root');
        if (root) {
            observer.observe(root, {
                childList: true,
                subtree: true
            });
        }
    }
    
    // Utility functions
    function showLoading(message) {
        removeModals();
        
        const loadingHTML = `
            <div id="loading-modal" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: flex; justify-content: center; align-items: center; z-index: 99999; font-family: Arial, sans-serif;">
                <div style="background: white; padding: 30px; border-radius: 10px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
                    <h3 style="margin: 0 0 15px 0; color: #333;">🔄 ${message}</h3>
                    <div style="margin: 20px 0; color: #666;">Please wait...</div>
                    <div style="width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #007bff; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto;"></div>
                </div>
            </div>
            <style>
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        `;
        
        document.body.insertAdjacentHTML('beforeend', loadingHTML);
    }
    
    function hideLoading() {
        const loading = document.getElementById('loading-modal');
        if (loading) loading.remove();
    }
    
    function showAlert(message, type = 'info') {
        const colors = {
            success: { bg: '#d4edda', border: '#28a745', text: '#155724' },
            error: { bg: '#f8d7da', border: '#dc3545', text: '#721c24' },
            warning: { bg: '#fff3cd', border: '#ffc107', text: '#856404' },
            info: { bg: '#d1ecf1', border: '#17a2b8', text: '#0c5460' }
        };
        
        const color = colors[type] || colors.info;
        
        const alertHTML = `
            <div id="alert-modal" style="position: fixed; top: 20px; right: 20px; background: ${color.bg}; color: ${color.text}; border: 2px solid ${color.border}; padding: 15px 20px; border-radius: 8px; z-index: 99999; font-family: Arial, sans-serif; max-width: 400px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold;">${message}</span>
                    <button onclick="document.getElementById('alert-modal').remove()" style="background: none; border: none; font-size: 18px; cursor: pointer; color: ${color.text}; margin-left: 10px;">×</button>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', alertHTML);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            const alert = document.getElementById('alert-modal');
            if (alert) alert.remove();
        }, 5000);
    }
    
    function removeModals() {
        const modals = document.querySelectorAll('#loading-modal, #ab-results-modal, #alert-modal');
        modals.forEach(modal => modal.remove());
    }
    
    // Global functions
    window.copyContent = function(text, button) {
        navigator.clipboard.writeText(text).then(() => {
            const originalText = button.textContent;
            button.textContent = '✅ Copied!';
            button.style.background = '#28a745';
            
            setTimeout(() => {
                button.textContent = originalText;
                button.style.background = '#28a745';
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy: ', err);
            showAlert('Failed to copy text. Please copy manually.', 'error');
        });
    };
    
    window.removeModals = removeModals;
    
    console.log('✅ React A/B Testing Fix initialized successfully');
})();

