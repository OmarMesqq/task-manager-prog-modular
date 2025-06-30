import os
import sys
import atexit

# Adiciona o diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Adiciona o diretório pai (web/task_manager_web) ao path
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Adiciona o diretório raiz do Task Manager ao path
task_manager_root = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
sys.path.insert(0, task_manager_root)

# Adiciona o diretório modules ao path
modules_dir = os.path.join(task_manager_root, 'modules')
sys.path.insert(0, modules_dir)

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.routes.task_routes import task_bp
from src.routes.user_routes import user_bp
from src.routes.tag_routes import tag_bp
from src.routes.team_routes import team_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'task_manager_secret_key_2024'

# Habilita CORS para permitir requisições do frontend
CORS(app)

# Registra os blueprints da API
app.register_blueprint(task_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(tag_bp, url_prefix='/api')
app.register_blueprint(team_bp, url_prefix='/api')

# Variável global para o sistema GT
_gt_system = None

# Inicializa o sistema de gerenciamento de tarefas (primeira vez)
try:
    from modules.gerenciamento_tarefas import gt_inicializar, gt_finalizar
    _gt_system = gt_inicializar()
    if _gt_system is None:
        print("❌ Erro: Falha ao inicializar o sistema GT")
        sys.exit(1)
    print("✅ Sistema GT inicializado com sucesso (processo principal)")
    
    def finalizar_gt():
        global _gt_system
        if _gt_system:
            try:
                gt_finalizar(_gt_system)
                _gt_system = None
                print("✅ Sistema GT finalizado com sucesso")
            except Exception as e:
                print(f"⚠️  Erro ao finalizar sistema GT: {e}")
    atexit.register(finalizar_gt)
except ImportError as e:
    print(f"❌ Erro: Não foi possível importar módulos GT: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro inesperado ao inicializar sistema GT: {e}")
    sys.exit(1)

# Torna o sistema disponível globalmente para as rotas
app.config['GT_SYSTEM'] = _gt_system

# Garante inicialização em cada processo do Flask
@app.before_request
def ensure_gt_initialized():
    global _gt_system
    
    # Verifica se o sistema GT está disponível na configuração
    if app.config.get('GT_SYSTEM') is None:
        print("🔄 GT não encontrado na configuração, reinicializando...")
        try:
            from modules.gerenciamento_tarefas import gt_inicializar
            _gt_system = gt_inicializar()
            app.config['GT_SYSTEM'] = _gt_system
            print("🔄 GT (re)inicializado no processo Flask!")
        except Exception as e:
            print(f"❌ Erro ao reinicializar GT: {e}")
            app.config['GT_SYSTEM'] = None

@app.route('/api/health')
def health_check():
    gt_system = app.config.get('GT_SYSTEM')
    if gt_system is None:
        return jsonify({
            'status': 'error',
            'message': 'Sistema GT não inicializado',
            'version': '1.0.0'
        }), 500
    return jsonify({
        'status': 'ok',
        'message': 'Task Manager API is running',
        'version': '1.0.0',
        'gt_system': 'initialized'
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404
    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.teardown_appcontext
def cleanup_gt_system(error):
    if error:
        print(f"⚠️  Erro na aplicação: {error}")

if __name__ == '__main__':
    try:
        print("=" * 60)
        print("🚀 INICIANDO TASK MANAGER WEB")
        print("=" * 60)
        print("📋 Sistema de Gerenciamento de Tarefas")
        print("🌐 Interface Web: http://localhost:5001")
        print("🔗 API Health Check: http://localhost:5001/api/health")
        print("=" * 60)
        app.run(host='0.0.0.0', port=5001, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Encerrando Task Manager Web...")
    except Exception as e:
        print(f"❌ Erro ao executar aplicação: {e}")
    finally:
        pass

