// AI Diet Planner - Main JavaScript
const API_BASE = '';
let currentToken = null;
let currentUser = null;

document.addEventListener('DOMContentLoaded', initApp);

async function initApp() {
    setupEventListeners();
    try {
        const token = localStorage.getItem('diet_token');
        if (token) {
            currentToken = token;
            await loadUserProfile(token);
        }
    } catch (err) {
        console.error('Init error:', err);
    }
}

function setupEventListeners() {
    // Auth
    document.getElementById('auth-form').addEventListener('submit', handleAuth);
    document.getElementById('toggle-link').addEventListener('click', toggleAuthMode);
    
    // Main app
    document.getElementById('logout-btn').addEventListener('click', logout);
    document.getElementById('new-plan-btn').addEventListener('click', showDietForm);
    document.getElementById('diet-form').addEventListener('submit', handleDietSubmit);
    document.getElementById('save-plan').addEventListener('click', saveCurrentPlan);
    document.getElementById('new-plan-again').addEventListener('click', showDietForm);
    
    // Chat
    document.getElementById('chat-form').addEventListener('submit', handleChat);
    
    // Load plans
    loadPlans();
}

async function handleAuth(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value;
    const isRegister = document.getElementById('email').style.display !== 'none';
    
    try {
        let response;
        if (isRegister) {
            response = await fetch(`${API_BASE}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });
        } else {
            response = await fetch(`${API_BASE}/token`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
            });
        }
        
        if (!response.ok) {
            throw new Error(await response.text());
        }
        
        const data = await response.json();
        currentToken = data.access_token;
        localStorage.setItem('diet_token', currentToken);
        
        await loadUserProfile(currentToken);
        showMainApp();
        
    } catch (err) {
        alert('Error: ' + err.message);
    }
}

async function loadUserProfile(token) {
    try {
        const response = await fetch(`${API_BASE}/users/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            currentUser = await response.json();
            document.getElementById('user-info').textContent = `Welcome, ${currentUser.username}!`;
        }
    } catch (err) {
        console.error('Profile load error:', err);
    }
}

function toggleAuthMode(e) {
    e.preventDefault();
    const isRegister = document.getElementById('email').style.display !== 'none';
    const title = document.getElementById('auth-title');
    const toggleText = document.getElementById('toggle-link');
    const emailInput = document.getElementById('email');
    
    if (isRegister) {
        title.textContent = 'Login';
        toggleText.textContent = 'Register';
        emailInput.style.display = 'none';
    } else {
        title.textContent = 'Register';
        toggleText.textContent = 'Login';
        emailInput.style.display = 'block';
    }
}

function showMainApp() {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('main-app').style.display = 'block';
    loadPlans();
}

function logout() {
    localStorage.removeItem('diet_token');
    currentToken = null;
    currentUser = null;
    document.getElementById('main-app').style.display = 'none';
    document.getElementById('auth-section').style.display = 'block';
}

function showDietForm() {
    document.getElementById('diet-form-section').style.display = 'block';
    document.getElementById('results-section').style.display = 'none';
    document.querySelector('.plans-grid').style.display = 'none';
    document.getElementById('diet-form').reset();
    document.getElementById('diet-form-section').scrollIntoView({ behavior: 'smooth' });
}

async function handleDietSubmit(e) {
    e.preventDefault();
    const generateBtn = document.getElementById('generate-btn');
    const generateText = document.getElementById('generate-text');
    const spinner = document.getElementById('loading-spinner');
    
    generateBtn.disabled = true;
    generateText.style.display = 'none';
    spinner.style.display = 'inline-block';
    
    const formData = new FormData(e.target);
    const dietData = Object.fromEntries(formData);
    
    try {
        const response = await fetch(`${API_BASE}/calculate-diet`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${currentToken}`
            },
            body: JSON.stringify(dietData)
        });
        
        if (!response.ok) {
            throw new Error(await response.text());
        }
        
        const plan = await response.json();
        displayPlan(plan);
        loadPlans(); // Refresh plans list
        
    } catch (err) {
        alert('Error generating plan: ' + err.message);
    } finally {
        generateBtn.disabled = false;
        generateText.style.display = 'inline';
        spinner.style.display = 'none';
    }
}

function displayPlan(plan) {
    document.getElementById('bmi').textContent = plan.bmi;
    document.getElementById('daily-calories').textContent = `${plan.daily_calories.toLocaleString()} kcal`;
    document.getElementById('water-intake').textContent = plan.water_intake;
    document.getElementById('breakfast').textContent = plan.breakfast;
    document.getElementById('lunch').textContent = plan.lunch;
    document.getElementById('dinner').textContent = plan.dinner;
    document.getElementById('snacks').textContent = plan.snacks;
    
    document.getElementById('diet-form-section').style.display = 'none';
    document.getElementById('results-section').style.display = 'block';
    document.querySelector('.plans-grid').style.display = 'grid';
    document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
    
    window.currentPlan = plan; // For PDF export
}

async function loadPlans() {
    if (!currentToken) return;
    
    try {
        const response = await fetch(`${API_BASE}/my-plans`, {
            headers: { 'Authorization': `Bearer ${currentToken}` }
        });
        if (response.ok) {
            const plans = await response.json();
            displayPlans(plans);
        }
    } catch (err) {
        console.error('Plans load error:', err);
    }
}

function displayPlans(plans) {
    const container = document.querySelector('.plans-grid');
    container.innerHTML = '<button id="new-plan-btn" class="plan-card new-plan">+ New Diet Plan</button>';
    
    plans.slice(0, 4).forEach((plan, idx) => {
        const card = document.createElement('div');
        card.className = 'plan-card';
        card.innerHTML = `
            <h4>Plan ${idx + 1}</h4>
            <p>BMI: ${plan.bmi} | ${plan.daily_calories.toLocaleString()} kcal</p>
            <small>${new Date(plan.created_at).toLocaleDateString()}</small>
        `;
        card.addEventListener('click', () => loadPlanDetails(plan));
        container.appendChild(card);
    });
    
    // Re-attach event listener for new-plan-btn
    document.getElementById('new-plan-btn').addEventListener('click', showDietForm);
}

function loadPlanDetails(plan) {
    displayPlan(plan);
}

async function saveCurrentPlan() {
    alert('Plan already auto-saved to your account!');
}

async function handleChat(e) {
    e.preventDefault();
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;
    
    addChatMessage('user', message);
    input.value = '';
    
    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await response.json();
        addChatMessage('ai', data.response);
    } catch (err) {
        addChatMessage('ai', 'Chat service temporarily unavailable.');
    }
}

function addChatMessage(sender, text) {
    const messages = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = `chat-message ${sender}-message`;
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

