/**
 * AI Chatbot Widget for Rwanda Trade Intelligence Dashboard
 * Floating chat interface with context-aware assistance
 */

class TradeAssistantWidget {
    constructor() {
        this.isOpen = false;
        this.messages = [];
        this.isTyping = false;
        this.currentPage = this.getCurrentPage();
        
        this.init();
    }
    
    getCurrentPage() {
        const path = window.location.pathname;
        return path.split('/').pop() || 'front_page.html';
    }
    
    init() {
        // Create widget HTML
        this.createWidget();
        
        // Attach event listeners
        this.attachEventListeners();
        
        // Welcome message
        this.addMessage('assistant', '👋 Hello! I\'m your Rwanda Trade Intelligence Assistant. How can I help you today?');
        
        // Load quick actions
        this.loadQuickActions();
    }
    
    createWidget() {
        const widgetHTML = `
            <!-- Chat Button -->
            <div id="chatbot-button" class="chatbot-btn">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
                <span class="chatbot-badge">AI</span>
            </div>
            
            <!-- Chat Window -->
            <div id="chatbot-window" class="chatbot-window" style="display: none;">
                <!-- Header -->
                <div class="chatbot-header">
                    <div class="chatbot-header-title">
                        <span class="chatbot-icon">🤖</span>
                        <div>
                            <div class="chatbot-title">Trade Assistant</div>
                            <div class="chatbot-status">Online</div>
                        </div>
                    </div>
                    <button id="chatbot-close" class="chatbot-close-btn">✕</button>
                </div>
                
                <!-- Quick Actions -->
                <div id="chatbot-quick-actions" class="chatbot-quick-actions"></div>
                
                <!-- Messages -->
                <div id="chatbot-messages" class="chatbot-messages">
                    <!-- Messages will be added here -->
                </div>
                
                <!-- Input -->
                <div class="chatbot-input-container">
                    <input 
                        type="text" 
                        id="chatbot-input" 
                        class="chatbot-input" 
                        placeholder="Ask me anything..."
                        autocomplete="off"
                    />
                    <button id="chatbot-send" class="chatbot-send-btn">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </div>
            </div>
        `;
        
        // Add to body
        const container = document.createElement('div');
        container.innerHTML = widgetHTML;
        document.body.appendChild(container);
        
        // Add styles
        this.addStyles();
    }
    
    addStyles() {
        const styleSheet = document.createElement('style');
        styleSheet.textContent = `
            /* Chat Button */
            .chatbot-btn {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #4da6ff, #0066cc);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 4px 20px rgba(77, 166, 255, 0.4);
                transition: all 0.3s ease;
                z-index: 9998;
                color: white;
            }
            
            .chatbot-btn:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 30px rgba(77, 166, 255, 0.6);
            }
            
            .chatbot-badge {
                position: absolute;
                top: -5px;
                right: -5px;
                background: #ff5252;
                color: white;
                font-size: 10px;
                font-weight: bold;
                padding: 2px 6px;
                border-radius: 10px;
                border: 2px solid #001f3f;
            }
            
            /* Chat Window */
            .chatbot-window {
                position: fixed;
                bottom: 90px;
                right: 20px;
                width: 380px;
                height: 550px;
                background: #002d5a;
                border-radius: 16px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
                display: flex;
                flex-direction: column;
                z-index: 9999;
                border: 1px solid rgba(77, 166, 255, 0.3);
                animation: slideUp 0.3s ease;
            }
            
            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            /* Header */
            .chatbot-header {
                background: linear-gradient(135deg, #003d7a, #001f3f);
                padding: 16px;
                border-radius: 16px 16px 0 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid rgba(77, 166, 255, 0.2);
            }
            
            .chatbot-header-title {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .chatbot-icon {
                font-size: 28px;
            }
            
            .chatbot-title {
                color: #C0C0C0;
                font-weight: bold;
                font-size: 16px;
            }
            
            .chatbot-status {
                color: #4caf50;
                font-size: 12px;
            }
            
            .chatbot-close-btn {
                background: transparent;
                border: none;
                color: #C0C0C0;
                font-size: 24px;
                cursor: pointer;
                padding: 0;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: all 0.2s;
            }
            
            .chatbot-close-btn:hover {
                background: rgba(255, 255, 255, 0.1);
                color: white;
            }
            
            /* Quick Actions */
            .chatbot-quick-actions {
                padding: 12px;
                background: rgba(0, 51, 102, 0.5);
                border-bottom: 1px solid rgba(77, 166, 255, 0.2);
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
                overflow-x: auto;
            }
            
            .chatbot-quick-action-btn {
                background: rgba(77, 166, 255, 0.2);
                border: 1px solid rgba(77, 166, 255, 0.4);
                color: #C0C0C0;
                padding: 6px 12px;
                border-radius: 16px;
                font-size: 12px;
                cursor: pointer;
                white-space: nowrap;
                transition: all 0.2s;
            }
            
            .chatbot-quick-action-btn:hover {
                background: rgba(77, 166, 255, 0.4);
                color: white;
            }
            
            /* Messages */
            .chatbot-messages {
                flex: 1;
                overflow-y: auto;
                padding: 16px;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .chatbot-message {
                display: flex;
                gap: 8px;
                animation: fadeIn 0.3s ease;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .chatbot-message.user {
                flex-direction: row-reverse;
            }
            
            .chatbot-message-avatar {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                flex-shrink: 0;
            }
            
            .chatbot-message.assistant .chatbot-message-avatar {
                background: linear-gradient(135deg, #4da6ff, #0066cc);
            }
            
            .chatbot-message.user .chatbot-message-avatar {
                background: linear-gradient(135deg, #4caf50, #2e7d32);
            }
            
            .chatbot-message-content {
                max-width: 75%;
                padding: 10px 14px;
                border-radius: 12px;
                line-height: 1.5;
                font-size: 14px;
            }
            
            .chatbot-message.assistant .chatbot-message-content {
                background: rgba(77, 166, 255, 0.2);
                border: 1px solid rgba(77, 166, 255, 0.3);
                color: #C0C0C0;
                border-bottom-left-radius: 4px;
            }
            
            .chatbot-message.user .chatbot-message-content {
                background: rgba(76, 175, 80, 0.2);
                border: 1px solid rgba(76, 175, 80, 0.3);
                color: #C0C0C0;
                border-bottom-right-radius: 4px;
            }
            
            .chatbot-message-time {
                font-size: 10px;
                color: #808080;
                margin-top: 4px;
            }
            
            /* Typing indicator */
            .chatbot-typing {
                display: flex;
                gap: 4px;
                padding: 10px;
            }
            
            .chatbot-typing-dot {
                width: 8px;
                height: 8px;
                background: #4da6ff;
                border-radius: 50%;
                animation: typing 1.4s infinite;
            }
            
            .chatbot-typing-dot:nth-child(2) { animation-delay: 0.2s; }
            .chatbot-typing-dot:nth-child(3) { animation-delay: 0.4s; }
            
            @keyframes typing {
                0%, 60%, 100% { transform: translateY(0); }
                30% { transform: translateY(-10px); }
            }
            
            /* Action button in message */
            .chatbot-action-btn {
                display: inline-block;
                margin-top: 8px;
                padding: 6px 12px;
                background: rgba(77, 166, 255, 0.3);
                border: 1px solid rgba(77, 166, 255, 0.5);
                border-radius: 6px;
                color: #4da6ff;
                font-size: 12px;
                cursor: pointer;
                transition: all 0.2s;
            }
            
            .chatbot-action-btn:hover {
                background: rgba(77, 166, 255, 0.5);
                color: white;
            }
            
            /* Input */
            .chatbot-input-container {
                display: flex;
                gap: 8px;
                padding: 16px;
                background: rgba(0, 51, 102, 0.5);
                border-top: 1px solid rgba(77, 166, 255, 0.2);
                border-radius: 0 0 16px 16px;
            }
            
            .chatbot-input {
                flex: 1;
                background: rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(77, 166, 255, 0.3);
                border-radius: 20px;
                padding: 10px 16px;
                color: #C0C0C0;
                font-size: 14px;
                outline: none;
                transition: all 0.2s;
            }
            
            .chatbot-input:focus {
                border-color: #4da6ff;
                background: rgba(0, 0, 0, 0.4);
            }
            
            .chatbot-input::placeholder {
                color: #808080;
            }
            
            .chatbot-send-btn {
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #4da6ff, #0066cc);
                border: none;
                border-radius: 50%;
                color: white;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s;
            }
            
            .chatbot-send-btn:hover {
                transform: scale(1.1);
                box-shadow: 0 4px 15px rgba(77, 166, 255, 0.4);
            }
            
            .chatbot-send-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            /* Scrollbar */
            .chatbot-messages::-webkit-scrollbar {
                width: 6px;
            }
            
            .chatbot-messages::-webkit-scrollbar-track {
                background: rgba(0, 0, 0, 0.2);
            }
            
            .chatbot-messages::-webkit-scrollbar-thumb {
                background: rgba(77, 166, 255, 0.4);
                border-radius: 3px;
            }
            
            .chatbot-messages::-webkit-scrollbar-thumb:hover {
                background: rgba(77, 166, 255, 0.6);
            }
            
            /* Mobile responsive */
            @media (max-width: 480px) {
                .chatbot-window {
                    width: calc(100vw - 40px);
                    height: calc(100vh - 120px);
                    right: 20px;
                    bottom: 90px;
                }
            }
        `;
        
        document.head.appendChild(styleSheet);
    }
    
    attachEventListeners() {
        // Toggle chat window
        document.getElementById('chatbot-button').addEventListener('click', () => {
            this.toggleChat();
        });
        
        // Close button
        document.getElementById('chatbot-close').addEventListener('click', () => {
            this.toggleChat();
        });
        
        // Send message
        document.getElementById('chatbot-send').addEventListener('click', () => {
            this.sendMessage();
        });
        
        // Enter key to send
        document.getElementById('chatbot-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }
    
    toggleChat() {
        const window = document.getElementById('chatbot-window');
        const button = document.getElementById('chatbot-button');
        
        this.isOpen = !this.isOpen;
        
        if (this.isOpen) {
            window.style.display = 'flex';
            button.style.transform = 'scale(0.9)';
            document.getElementById('chatbot-input').focus();
        } else {
            window.style.display = 'none';
            button.style.transform = 'scale(1)';
        }
    }
    
    addMessage(role, text, action = null) {
        const messagesDiv = document.getElementById('chatbot-messages');
        const time = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${role}`;
        
        const avatar = role === 'assistant' ? '🤖' : '👤';
        
        let actionHTML = '';
        if (action && action.type === 'navigate') {
            actionHTML = `<button class="chatbot-action-btn" onclick="window.tradeAssistant.navigateTo('${action.page}')">
                📍 Go to ${action.page.replace('.html', '').replace(/_/g, ' ')}
            </button>`;
        }
        
        messageDiv.innerHTML = `
            <div class="chatbot-message-avatar">${avatar}</div>
            <div>
                <div class="chatbot-message-content">
                    ${text}
                    ${actionHTML}
                </div>
                <div class="chatbot-message-time">${time}</div>
            </div>
        `;
        
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        
        this.messages.push({ role, text, time });
    }
    
    showTyping() {
        const messagesDiv = document.getElementById('chatbot-messages');
        const typingDiv = document.createElement('div');
        typingDiv.id = 'chatbot-typing-indicator';
        typingDiv.className = 'chatbot-message assistant';
        typingDiv.innerHTML = `
            <div class="chatbot-message-avatar">🤖</div>
            <div class="chatbot-message-content">
                <div class="chatbot-typing">
                    <div class="chatbot-typing-dot"></div>
                    <div class="chatbot-typing-dot"></div>
                    <div class="chatbot-typing-dot"></div>
                </div>
            </div>
        `;
        messagesDiv.appendChild(typingDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        this.isTyping = true;
    }
    
    hideTyping() {
        const typingDiv = document.getElementById('chatbot-typing-indicator');
        if (typingDiv) {
            typingDiv.remove();
        }
        this.isTyping = false;
    }
    
    async sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = input.value.trim();
        
        if (!message || this.isTyping) return;
        
        // Add user message
        this.addMessage('user', message);
        input.value = '';
        
        // Show typing indicator
        this.showTyping();
        
        try {
            // Send to API
            const response = await fetch('/api/chatbot/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    current_page: this.currentPage
                })
            });
            
            const data = await response.json();
            
            // Hide typing
            this.hideTyping();
            
            // Add assistant response
            this.addMessage('assistant', data.answer, data.suggested_action);
            
        } catch (error) {
            console.error('Chatbot error:', error);
            this.hideTyping();
            this.addMessage('assistant', '❌ Sorry, I encountered an error. Please try again.');
        }
    }
    
    async loadQuickActions() {
        try {
            const response = await fetch('/api/chatbot/quick_actions');
            const data = await response.json();
            
            if (data.quick_actions) {
                const actionsDiv = document.getElementById('chatbot-quick-actions');
                actionsDiv.innerHTML = data.quick_actions.map(action => 
                    `<button class="chatbot-quick-action-btn" onclick="window.tradeAssistant.sendQuickAction('${action.query}')">${action.label}</button>`
                ).join('');
            }
        } catch (error) {
            console.error('Error loading quick actions:', error);
        }
    }
    
    sendQuickAction(query) {
        document.getElementById('chatbot-input').value = query;
        this.sendMessage();
    }
    
    navigateTo(page) {
        window.location.href = page;
    }
}

// Initialize chatbot when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.tradeAssistant = new TradeAssistantWidget();
    });
} else {
    window.tradeAssistant = new TradeAssistantWidget();
}
