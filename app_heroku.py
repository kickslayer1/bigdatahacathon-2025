"""
Heroku-compatible app configuration
"""
import os
import sys
from pathlib import Path

# Add htmlss directory to path
current_dir = Path(__file__).parent
htmlss_dir = current_dir / "htmlss"
sys.path.insert(0, str(htmlss_dir))

# Import the main app
from app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)