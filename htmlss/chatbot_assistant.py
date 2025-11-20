"""
AI Chatbot Assistant for Rwanda Trade Intelligence Dashboard
Uses Google Gemini API (free tier) to provide intelligent assistance
"""

import os
import json
from datetime import datetime
from google import genai
from db import get_db_connection

# Configure Gemini API - Client gets API key from GEMINI_API_KEY environment variable
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

# Initialize Gemini client (automatically uses GEMINI_API_KEY env var)
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    client = None


class RwandaTradeAssistant:
    """AI Assistant for Rwanda Trade Intelligence Dashboard"""
    
    def __init__(self):
        self.model_name = 'gemini-1.5-pro'  # Using stable Gemini 1.5 Pro model
        self.conversation_history = []
        self.client = client
        
        # System context about the platform
        self.system_context = """
You are an AI assistant for the Rwanda Trade Intelligence Dashboard, a comprehensive platform 
for analyzing Rwanda's international trade data. You help users navigate the platform and 
answer questions about:

**Available Features:**
1. **Global Trade Analysis** - Exports, imports, re-imports data from 2019-2024
2. **Demand Prediction** - ML forecasts for 2026 trade volumes
3. **Currency Analysis** - Exchange rates for USD, EUR, CNY, TSH with 2026 forecasts
4. **Youth & SME Insights** - Trade opportunities for young entrepreneurs
5. **Policy Recommendations** - Data-driven trade policy suggestions

**Navigation Pages:**
- Home / Front Page
- Global Trade 2025
- Demand Prediction 2026
- Currency Analysis
- Youth & SME Opportunities
- Policy Recommendations
- Referencing & Data Sources

**Data Coverage:**
- Trade data: 2019-2024 (quarterly)
- Currency data: 6 years daily rates (USD, EUR, CNY, TSH)
- Forecasts: 2026 predictions using Prophet ML

**Your Role:**
- Answer questions about Rwanda's trade data
- Help users navigate to relevant sections
- Explain economic concepts and trends
- Provide data-driven insights
- Suggest analyses users might find useful

Be concise, accurate, and helpful. If you need specific data, indicate what database query would help.
"""
    
    def get_platform_stats(self):
        """Fetch current platform statistics from database"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get trade data summary
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT period) as total_periods,
                    SUM(exports) as total_exports,
                    SUM(imports) as total_imports,
                    MAX(period) as latest_period
                FROM exportss
            """)
            trade_stats = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return trade_stats
        except Exception as e:
            print(f"Error fetching platform stats: {e}")
            return {}
    
    def query_trade_data(self, query_type, params=None):
        """
        Query specific trade data from database
        
        Args:
            query_type: Type of query (exports, imports, trends, top_products, etc.)
            params: Additional parameters for the query
        
        Returns:
            dict: Query results
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            if query_type == 'recent_trade':
                cursor.execute("""
                    SELECT period, exports, imports, `re-imports`
                    FROM exportss
                    ORDER BY period DESC
                    LIMIT 5
                """)
                results = cursor.fetchall()
            
            elif query_type == 'trade_balance':
                cursor.execute("""
                    SELECT period, 
                           exports, 
                           imports,
                           (exports - imports) as trade_balance
                    FROM exportss
                    ORDER BY period DESC
                    LIMIT 10
                """)
                results = cursor.fetchall()
            
            elif query_type == 'yearly_summary':
                cursor.execute("""
                    SELECT 
                        SUBSTRING(period, 1, 4) as year,
                        SUM(exports) as total_exports,
                        SUM(imports) as total_imports,
                        SUM(exports - imports) as net_balance
                    FROM exportss
                    GROUP BY SUBSTRING(period, 1, 4)
                    ORDER BY year DESC
                """)
                results = cursor.fetchall()
            
            elif query_type == 'latest_stats':
                cursor.execute("""
                    SELECT period, exports, imports, `re-imports`
                    FROM exportss
                    ORDER BY period DESC
                    LIMIT 1
                """)
                results = cursor.fetchone()
            
            else:
                results = {"error": f"Unknown query type: {query_type}"}
            
            cursor.close()
            conn.close()
            
            return results
        
        except Exception as e:
            return {"error": f"Database query failed: {str(e)}"}
    
    def get_currency_info(self, currency_code=None):
        """Get currency information from CSV files"""
        try:
            import pandas as pd
            
            currencies = {
                'USD': 'US Dollar',
                'EUR': 'Euro',
                'CNY': 'Chinese Yuan',
                'TSH': 'Tanzanian Shilling'
            }
            
            if currency_code:
                currencies = {currency_code: currencies.get(currency_code, 'Unknown')}
            
            info = {}
            for code, name in currencies.items():
                try:
                    df = pd.read_csv(f'{code}.csv')
                    latest = df.iloc[-1]
                    info[code] = {
                        'name': name,
                        'latest_rate': float(latest['average_rate']),
                        'latest_date': str(latest['post_date']),
                        'data_points': len(df)
                    }
                except:
                    pass
            
            return info
        
        except Exception as e:
            return {"error": f"Currency data unavailable: {str(e)}"}
    
    def detect_intent(self, user_message):
        """
        Detect user intent from message
        
        Returns:
            str: Intent type (navigation, data_query, explanation, general)
        """
        message_lower = user_message.lower()
        
        # Navigation intents
        if any(word in message_lower for word in ['go to', 'navigate', 'take me', 'show me page', 'open']):
            return 'navigation'
        
        # Data query intents
        if any(word in message_lower for word in ['what is', 'how much', 'show data', 'exports', 'imports', 'trade balance', 'latest']):
            return 'data_query'
        
        # Explanation intents
        if any(word in message_lower for word in ['explain', 'what does', 'how does', 'why', 'meaning of']):
            return 'explanation'
        
        # Currency intents
        if any(word in message_lower for word in ['currency', 'exchange rate', 'usd', 'euro', 'yuan', 'shilling']):
            return 'currency_query'
        
        return 'general'
    
    def format_data_for_context(self, data, data_type):
        """Format database results for AI context"""
        if not data or 'error' in data:
            return "Data unavailable"
        
        if data_type == 'trade_balance':
            formatted = "Recent Trade Balance Data:\n"
            for row in data[:5]:
                formatted += f"- {row['period']}: Exports=${row['exports']}M, Imports=${row['imports']}M, Balance=${row['trade_balance']}M\n"
        
        elif data_type == 'yearly_summary':
            formatted = "Yearly Trade Summary:\n"
            for row in data:
                formatted += f"- {row['year']}: Exports=${row['total_exports']}M, Imports=${row['total_imports']}M, Net=${row['net_balance']}M\n"
        
        elif data_type == 'latest_stats':
            formatted = f"Latest Trade Data ({data['period']}):\n"
            formatted += f"- Exports: ${data['exports']}M\n"
            formatted += f"- Imports: ${data['imports']}M\n"
            formatted += f"- Re-imports: ${data['re-imports']}M\n"
        
        elif data_type == 'currency_info':
            formatted = "Current Exchange Rates:\n"
            for code, info in data.items():
                formatted += f"- {info['name']} ({code}): {info['latest_rate']:.2f} RWF (as of {info['latest_date']})\n"
        
        else:
            formatted = json.dumps(data, indent=2)
        
        return formatted
    
    def generate_response(self, user_message, current_page=None):
        """
        Generate AI response using Gemini
        
        Args:
            user_message: User's question/message
            current_page: Current page user is on (optional)
        
        Returns:
            dict: Response with answer, actions, and metadata
        """
        try:
            if not GEMINI_API_KEY:
                return {
                    'answer': "⚠️ Chatbot is not configured. Please set GEMINI_API_KEY environment variable.",
                    'requires_setup': True
                }
            
            # Detect intent
            intent = self.detect_intent(user_message)
            
            # Gather relevant context data
            context_data = {}
            
            if intent == 'data_query':
                # Fetch relevant trade data
                context_data['latest'] = self.query_trade_data('latest_stats')
                context_data['trade_balance'] = self.query_trade_data('trade_balance')
            
            elif intent == 'currency_query':
                context_data['currencies'] = self.get_currency_info()
            
            # Get platform stats
            platform_stats = self.get_platform_stats()
            
            # Build enhanced context
            enhanced_context = self.system_context + f"\n\n**Current Context:**\n"
            
            if current_page:
                enhanced_context += f"- User is currently on: {current_page}\n"
            
            if platform_stats:
                enhanced_context += f"- Total trade periods in database: {platform_stats.get('total_periods', 'N/A')}\n"
                enhanced_context += f"- Latest data period: {platform_stats.get('latest_period', 'N/A')}\n"
            
            # Add relevant data to context
            for data_type, data in context_data.items():
                formatted = self.format_data_for_context(data, data_type)
                enhanced_context += f"\n**{data_type.replace('_', ' ').title()}:**\n{formatted}\n"
            
            # Create prompt
            prompt = f"""
{enhanced_context}

**User Question:** {user_message}

Provide a helpful, accurate response. If the user is asking about data, reference the specific 
numbers provided above. If they want to navigate, suggest the appropriate page. Keep responses 
concise (2-4 sentences) unless detailed explanation is needed.
"""
            
            # Use google-genai SDK with stable model
            if not self.client:
                return {
                    'answer': "⚠️ Chatbot client not initialized. Please check GEMINI_API_KEY.",
                    'requires_setup': True
                }
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            response_text = response.text
            
            # Extract suggested actions (navigation, queries, etc.)
            suggested_action = None
            if intent == 'navigation':
                # Parse navigation intent
                message_lower = user_message.lower()
                if 'currency' in message_lower:
                    suggested_action = {'type': 'navigate', 'page': 'currency_analysis.html'}
                elif 'trade' in message_lower or 'global' in message_lower:
                    suggested_action = {'type': 'navigate', 'page': 'global_trade_2025.html'}
                elif 'demand' in message_lower or 'prediction' in message_lower:
                    suggested_action = {'type': 'navigate', 'page': 'demand_prediction_2026.html'}
                elif 'youth' in message_lower or 'sme' in message_lower:
                    suggested_action = {'type': 'navigate', 'page': 'youth_sme.html'}
                elif 'policy' in message_lower:
                    suggested_action = {'type': 'navigate', 'page': 'policy_recommendations.html'}
                elif 'home' in message_lower or 'main' in message_lower:
                    suggested_action = {'type': 'navigate', 'page': 'front_page.html'}
            
            return {
                'answer': response_text,
                'intent': intent,
                'suggested_action': suggested_action,
                'timestamp': datetime.now().isoformat(),
                'context_used': bool(context_data)
            }
        
        except Exception as e:
            return {
                'answer': f"I encountered an error: {str(e)}. Please try rephrasing your question or contact support.",
                'error': str(e)
            }
    
    def get_quick_actions(self):
        """Get suggested quick action buttons"""
        return [
            {
                'label': '📊 Latest Trade Data',
                'query': 'What are the latest trade statistics?'
            },
            {
                'label': '💱 Currency Rates',
                'query': 'Show me current exchange rates'
            },
            {
                'label': '📈 Trade Balance Trend',
                'query': 'What is the trade balance trend?'
            },
            {
                'label': '🔮 2026 Predictions',
                'query': 'Tell me about 2026 forecasts'
            },
            {
                'label': '🗺️ Navigate Dashboard',
                'query': 'What sections are available?'
            }
        ]


# Test function
if __name__ == '__main__':
    assistant = RwandaTradeAssistant()
    
    # Test queries
    test_queries = [
        "What are the latest trade statistics?",
        "Show me current exchange rates for USD",
        "Take me to currency analysis page",
        "What is the trade balance trend?"
    ]
    
    print("🤖 Rwanda Trade Assistant Test\n")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n👤 User: {query}")
        response = assistant.generate_response(query, current_page="front_page.html")
        print(f"🤖 Assistant: {response['answer']}")
        print(f"   Intent: {response.get('intent', 'N/A')}")
        if response.get('suggested_action'):
            print(f"   Action: {response['suggested_action']}")
