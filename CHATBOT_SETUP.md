# AI Chatbot Setup Guide

## Overview
The Rwanda Trade Intelligence Dashboard now includes an AI-powered chatbot assistant that helps users:
- Navigate the platform
- Answer questions about trade data
- Get instant insights
- Access currency information
- View latest statistics

## Features
✅ Context-aware responses based on current page  
✅ Database query capabilities  
✅ Quick action buttons for common queries  
✅ Floating chat widget on all pages  
✅ Typing indicators and smooth animations  
✅ Navigation suggestions with clickable links  

## Setup Instructions

### 1. Get a Free Gemini API Key

The chatbot uses Google's Gemini API (free tier with generous limits):

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### 2. Set Environment Variable

**For Local Development:**

Windows PowerShell:
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

Windows CMD:
```cmd
set GEMINI_API_KEY=your-api-key-here
```

Linux/Mac:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**For Heroku Deployment:**

```bash
heroku config:set GEMINI_API_KEY="your-api-key-here" --app rwanda-trade-dashboard-fc1d68703baa
```

Or via Heroku Dashboard:
1. Go to: https://dashboard.heroku.com/apps/rwanda-trade-dashboard-fc1d68703baa/settings
2. Click "Reveal Config Vars"
3. Add new config var:
   - KEY: `GEMINI_API_KEY`
   - VALUE: `your-api-key-here`
4. Click "Add"

### 3. Test Locally

```bash
cd htmlss
python chatbot_assistant.py
```

This will run test queries and verify the chatbot is working.

### 4. Deploy to Heroku

```bash
git add .
git commit -m "Add AI chatbot assistant with Gemini API"
git push heroku main
```

## Usage

### For Users:
1. Click the blue AI chat button (bottom-right corner)
2. Type your question or click a quick action button
3. Chat with the assistant naturally
4. Click suggested navigation links to jump to pages

### Example Queries:
- "What are the latest trade statistics?"
- "Show me current exchange rates"
- "Take me to currency analysis"
- "What is the trade balance trend?"
- "Explain how demand prediction works"
- "Show me 2026 forecasts"

### For Developers:

**Backend API:**
- `POST /api/chatbot/query` - Send chat message
  ```json
  {
    "message": "What are the latest trade stats?",
    "current_page": "front_page.html"
  }
  ```

- `GET /api/chatbot/quick_actions` - Get quick action buttons

**Frontend Widget:**
- Automatically initialized on all main pages
- Access via: `window.tradeAssistant`
- Methods:
  - `sendMessage()` - Send user message
  - `navigateTo(page)` - Navigate to page
  - `toggleChat()` - Open/close chat window

## API Limits (Free Tier)

Gemini API free tier provides:
- **60 requests per minute**
- **1,500 requests per day**
- Sufficient for hundreds of users

If you need more, consider:
- Upgrade to paid tier
- Implement rate limiting per user
- Add caching for common queries

## Troubleshooting

**Chatbot shows "not configured" error:**
- Verify GEMINI_API_KEY is set correctly
- Check environment variables: `heroku config --app rwanda-trade-dashboard-fc1d68703baa`
- Restart Heroku dynos after setting config vars

**Chatbot not responding:**
- Check browser console for errors (F12)
- Verify user is authenticated (chatbot requires login)
- Check Heroku logs: `heroku logs --tail --app rwanda-trade-dashboard-fc1d68703baa`

**Database queries failing:**
- Ensure JawsDB connection is working
- Check app.py database configuration
- Verify tables exist: exportss, users

## File Structure

```
htmlss/
├── chatbot_assistant.py      # Backend AI logic
├── chatbot_widget.js          # Frontend chat UI
├── app.py                     # Flask API endpoints
└── [all HTML pages]           # Include chatbot widget
```

## Security Notes

- API key stored as environment variable (not in code)
- Chatbot requires user authentication
- All queries pass through Flask session check
- No sensitive data exposed to AI (only aggregated statistics)

## Future Enhancements

Potential improvements:
- Add conversation history persistence
- Implement user feedback (thumbs up/down)
- Add voice input/output
- Create admin analytics dashboard
- Multi-language support (Kinyarwanda, French)
- Export chat conversations
- Advanced data visualization generation

## Support

For issues or questions:
1. Check Heroku logs
2. Review browser console errors
3. Test API endpoints directly
4. Contact development team

---

**Status:** ✅ Ready for Deployment  
**Version:** 1.0  
**Last Updated:** November 20, 2025
