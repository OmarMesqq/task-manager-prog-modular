"""
Arquivo de entrada para a aplicação Flask
"""
from src.main import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 