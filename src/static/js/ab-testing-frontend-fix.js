// Comprehensive A/B Testing Frontend Fix
// This script fixes the React component integration issues

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Loading comprehensive A/B testing frontend fix...');
    
    // Wait for React to render
    setTimeout(initializeABTestingFix, 1000);
    
    function initializeABTestingFix() {
        console.log('🎯 Initializing A/B testing fix...');
        
        // Fix Create A/B Test button
        fixCreateTestButton();
        
        // Fix View Details buttons
        fixViewDetailsButtons();
        
        // Fix Start Test buttons
        fixStartTestButtons();
        
        // Monitor for dynamic content changes
        observeForChanges();
    }
    
    function fixCreateTestButton() {
        // Find the Create A/B Test button
        const createButton = document.querySelector('button[class*="Create"], button:contains("Create A/B Test")') || 
                           Array.from(document.querySelectorAll('button')).find(btn => 
                               btn.textContent.includes('Create A/B Test') || 
                               btn.textContent.includes('Create Test')
                           );
        
        if (createButton) {
            console.log('✅ Found Create A/B Test button, adding fix...');
            
            // Remove existing event listeners
            createButton.removeEventListener('click', handleCreateTest);
            
            // Add new event listener
            createButton.addEventListener('click', handleCreateTest);
        } else {
            console.log('⚠️ Create A/B Test button not found, will retry...');
            setTimeout(fixCreateTestButton, 2000);
        }
    }
    
    function handleCreateTest(e) {
        e.preventDefault();
        e.stopPropagation();
        
        console.log('🎯 Create A/B Test button clicked');
        
        // Collect form data
        const formData = collectFormData();
        
        if (!formData.name || formData.name.trim() === '') {
            alert('Please enter a test name');
            return;
        }
        
        // Show loading
        showLoading('Creating A/B Test...');
        
        // Make API call
        fetch('/api/ab-testing/create-test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            console.log('✅ Test created:', data);
            
            if (data.success) {
                alert('A/B Test created successfully!');
                // Refresh the active tests view
                refreshActiveTests();
                // Clear form
                clearForm();
            } else {
                alert('Error creating test: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            hideLoading();
            console.error('❌ Error creating test:', error);
            alert('Error creating test: ' + error.message);
        });
    }
    
    function collectFormData() {
        // Get form inputs
        const testNameInput = document.querySelector('input[placeholder*="Hook Optimization"], input[placeholder*="test name"]') ||
                             Array.from(document.querySelectorAll('input')).find(input => 
                                 input.placeholder && input.placeholder.toLowerCase().includes('test')
                             );
        
        const contentTypeSelect = document.querySelector('select') ||
                                 Array.from(document.querySelectorAll('select')).find(select => 
                                     select.innerHTML.includes('Property Showcase')
                                 );
        
        const platformSelect = Array.from(document.querySelectorAll('select')).find(select => 
                                   select.innerHTML.includes('Instagram')
                               );
        
        const locationInput = document.querySelector('input[placeholder="Windsor"]') ||
                             Array.from(document.querySelectorAll('input')).find(input => 
                                 input.placeholder === 'Windsor'
                             );
        
        // Get checkbox states for what to test
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        const testElements = [];
        
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                const label = checkbox.closest('label') || checkbox.nextElementSibling;
                if (label) {
                    const text = label.textContent || label.innerText;
                    if (text.includes('Opening Hooks')) testElements.push('hooks');
                    if (text.includes('Call-to-Action')) testElements.push('cta');
                    if (text.includes('Emoji Usage')) testElements.push('emoji');
                    if (text.includes('Hashtag Strategy')) testElements.push('hashtags');
                }
            }
        });
        
        // Default to hooks if nothing selected
        if (testElements.length === 0) {
            testElements.push('hooks');
        }
        
        const formData = {
            name: testNameInput ? testNameInput.value || 'Hook Testing - Windsor Properties' : 'Hook Testing - Windsor Properties',
            content_type: contentTypeSelect ? contentTypeSelect.value || 'property_showcase' : 'property_showcase',
            platform: platformSelect ? platformSelect.value || 'instagram' : 'instagram',
            location: locationInput ? locationInput.value || 'Windsor' : 'Windsor',
            test_elements: testElements,
            variations_count: 3
        };
        
        console.log('📋 Collected form data:', formData);
        return formData;
    }
    
    function fixViewDetailsButtons() {
        const viewButtons = Array.from(document.querySelectorAll('button')).filter(btn => 
            btn.textContent.includes('View Details') || btn.textContent.includes('View Results')
        );
        
        viewButtons.forEach(button => {
            button.removeEventListener('click', handleViewDetails);
            button.addEventListener('click', handleViewDetails);
        });
        
        if (viewButtons.length > 0) {
            console.log(`✅ Fixed ${viewButtons.length} View Details buttons`);
        }
    }
    
    function handleViewDetails(e) {
        e.preventDefault();
        e.stopPropagation();
        
        console.log('🎯 View Details button clicked');
        
        // Try to find test ID from the context
        let testId = findTestIdFromContext(e.target);
        
        if (!testId) {
            // Fallback: get the most recent test
            fetch('/api/ab-testing/tests')
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.tests && data.tests.length > 0) {
                        testId = data.tests[data.tests.length - 1].id;
                        loadTestResults(testId);
                    } else {
                        alert('No tests found. Please create a test first.');
                    }
                })
                .catch(error => {
                    console.error('Error fetching tests:', error);
                    alert('Error loading tests: ' + error.message);
                });
            return;
        }
        
        loadTestResults(testId);
    }
    
    function findTestIdFromContext(element) {
        // Look for test ID in various places
        let current = element;
        
        while (current && current !== document.body) {
            // Check data attributes
            if (current.dataset && current.dataset.testId) {
                return current.dataset.testId;
            }
            
            // Check for UUID patterns in text content
            const textContent = current.textContent || '';
            const uuidMatch = textContent.match(/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}/);
            if (uuidMatch) {
                return uuidMatch[0];
            }
            
            current = current.parentElement;
        }
        
        return null;
    }
    
    function loadTestResults(testId) {
        console.log('📡 Loading test results for:', testId);
        
        showLoading('Loading A/B Test Results...');
        
        fetch(`/api/ab-testing/analyze-results/${testId}`)
            .then(response => response.json())
            .then(data => {
                hideLoading();
                console.log('✅ Test results loaded:', data);
                
                if (data.success && data.data) {
                    showResultsModal(data.data);
                } else {
                    alert('Error loading results: ' + (data.error || 'Unknown error'));
                }
            })
            .catch(error => {
                hideLoading();
                console.error('❌ Error loading results:', error);
                alert('Error loading results: ' + error.message);
            });
    }
    
    function showResultsModal(data) {
        // Remove any existing modals
        removeExistingModals();
        
        let variationsHTML = '';
        if (data.variations && data.variations.length > 0) {
            variationsHTML = data.variations.map((variation, index) => `
                <div style="border: 2px solid #e9ecef; margin: 15px 0; padding: 20px; border-radius: 8px; background: #f8f9fa;">
                    <h4 style="color: #007bff; margin: 0 0 10px 0;">
                        Version ${String.fromCharCode(65 + index)}
                    </h4>
                    <div style="background: white; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #007bff;">
                        ${variation.content}
                    </div>
                    <button onclick="copyToClipboard('${variation.content.replace(/'/g, "\\'")}', this)" 
                            style="background: #28a745; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; margin-right: 10px;">
                        📋 Copy Content
                    </button>
                </div>
            `).join('');
        } else {
            variationsHTML = '<div style="text-align: center; padding: 40px; color: #666;"><h4>No variations found</h4></div>';
        }
        
        const modalHTML = `
            <div id="results-modal" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: flex; justify-content: center; align-items: center; z-index: 99999; font-family: Arial, sans-serif;">
                <div style="background: white; padding: 30px; border-radius: 12px; max-width: 900px; max-height: 85vh; overflow-y: auto; width: 90%; box-shadow: 0 8px 32px rgba(0,0,0,0.3);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
                        <h2 style="margin: 0; color: #333;">🧪 A/B Test Results</h2>
                        <button onclick="removeExistingModals()" style="background: #dc3545; color: white; border: none; padding: 8px 12px; border-radius: 6px; cursor: pointer;">✕</button>
                    </div>
                    
                    <h3 style="color: #666; margin-bottom: 15px;">${data.test_name || 'Content Variations'}</h3>
                    
                    <div style="background: #d4edda; padding: 15px; border-radius: 8px; margin-bottom: 20px; color: #155724;">
                        <strong>✅ ${data.message || 'Content variations ready for testing'}</strong>
                    </div>
                    
                    <h4 style="color: #333; margin-bottom: 15px;">Content Variations:</h4>
                    ${variationsHTML}
                    
                    <div style="text-align: center; margin-top: 25px;">
                        <button onclick="removeExistingModals()" style="background: #6c757d; color: white; border: none; padding: 12px 30px; border-radius: 8px; cursor: pointer;">Close</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }
    
    function fixStartTestButtons() {
        const startButtons = Array.from(document.querySelectorAll('button')).filter(btn => 
            btn.textContent.includes('Start Test') || btn.textContent.includes('Start')
        );
        
        startButtons.forEach(button => {
            button.removeEventListener('click', handleStartTest);
            button.addEventListener('click', handleStartTest);
        });
        
        if (startButtons.length > 0) {
            console.log(`✅ Fixed ${startButtons.length} Start Test buttons`);
        }
    }
    
    function handleStartTest(e) {
        e.preventDefault();
        e.stopPropagation();
        
        console.log('🎯 Start Test button clicked');
        
        const testId = findTestIdFromContext(e.target);
        
        if (!testId) {
            alert('Could not find test ID. Please try again.');
            return;
        }
        
        showLoading('Starting A/B Test...');
        
        fetch(`/api/ab-testing/start-test/${testId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            console.log('✅ Test started:', data);
            
            if (data.success) {
                alert('A/B Test started successfully!');
                refreshActiveTests();
            } else {
                alert('Error starting test: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            hideLoading();
            console.error('❌ Error starting test:', error);
            alert('Error starting test: ' + error.message);
        });
    }
    
    function refreshActiveTests() {
        // Trigger a refresh of the active tests view
        const activeTestsButton = Array.from(document.querySelectorAll('button')).find(btn => 
            btn.textContent.includes('Active Tests')
        );
        
        if (activeTestsButton) {
            activeTestsButton.click();
        }
    }
    
    function clearForm() {
        // Clear form inputs
        const inputs = document.querySelectorAll('input[type="text"], input[type="email"], textarea');
        inputs.forEach(input => {
            if (input.placeholder && !input.placeholder.includes('Windsor')) {
                input.value = '';
            }
        });
        
        // Uncheck checkboxes
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });
        
        // Reset selects to first option
        const selects = document.querySelectorAll('select');
        selects.forEach(select => {
            select.selectedIndex = 0;
        });
    }
    
    function observeForChanges() {
        // Monitor for dynamic content changes
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    // Re-apply fixes when new content is added
                    setTimeout(() => {
                        fixCreateTestButton();
                        fixViewDetailsButtons();
                        fixStartTestButtons();
                    }, 500);
                }
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    // Utility functions
    function showLoading(message = 'Loading...') {
        removeExistingModals();
        
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
    
    function removeExistingModals() {
        const modals = document.querySelectorAll('#loading-modal, #results-modal, #ab-results-modal, #active-tests-modal');
        modals.forEach(modal => modal.remove());
    }
    
    // Global functions for modal interactions
    window.copyToClipboard = function(text, button) {
        navigator.clipboard.writeText(text).then(() => {
            const originalText = button.textContent;
            button.textContent = '✅ Copied!';
            button.style.background = '#28a745';
            
            setTimeout(() => {
                button.textContent = originalText;
                button.style.background = '#28a745';
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy text: ', err);
            alert('Failed to copy text. Please copy manually.');
        });
    };
    
    window.removeExistingModals = removeExistingModals;
    
    console.log('✅ A/B Testing frontend fix loaded successfully');
});

