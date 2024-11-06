from typing import Dict

TEMPLATES: Dict[str, Dict[str, str]] = {
    'basic': {
        'app/__init__.py': '''
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    return app
''',
        'app/routes/__init__.py': '',
        'app/routes/chat_routes.py': '''
from flask import Blueprint, request, jsonify

bp = Blueprint('chat', __name__)

@bp.route('/chat', methods=['POST'])
def chat():
    return jsonify({'message': 'Hello from chat route!'})
''',
        # ... rest of the template files
        'app/services/__init__.py': '',
        'app/services/openai_service.py': '''
class OpenAIService:
    def __init__(self):
        pass
    
    def chat(self):
        pass
''',
        'app/services/anthropic_service.py': '''
class AnthropicService:
    def __init__(self):
        pass
    
    def chat(self):
        pass
''',
        'app/models/__init__.py': '',
        'app/utils/__init__.py': '',
        'app/utils/error_handlers.py': '''
from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
''',
        'config/__init__.py': '',
        'config/development.py': '''
class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = 'dev'
''',
        'config/production.py': '''
class ProductionConfig:
    DEBUG = False
    SECRET_KEY = 'production-key'
''',
        'config/testing.py': '''
class TestingConfig:
    TESTING = True
    DEBUG = True
''',
        'tests/__init__.py': '',
        'tests/test_routes.py': '''
def test_chat_route(client):
    response = client.post('/chat')
    assert response.status_code == 200
''',
        'tests/test_services.py': '''
def test_openai_service():
    pass

def test_anthropic_service():
    pass
''',
        'requirements.txt': '''
flask
flask-cors
python-dotenv
''',
        'run.py': '''
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
''',
        '.env': '''
OPENAI_API_KEY=your-api-key-here
ANTHROPIC_API_KEY=your-api-key-here
''',
        '.gitignore': '''
__pycache__/
*.pyc
.env
venv/
.pytest_cache/
''',
        'README.md': '''
# Flask API Project

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\\Scripts\\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in your API keys
5. Run the application: `python run.py`
'''
    },
    'full': {},  # Add full template configuration here
}
