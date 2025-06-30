from flask import current_app

def get_gt_system():
    """
    Obtém o sistema GT da configuração da aplicação Flask.
    
    Returns:
        Dict ou None: Sistema GT em formato dicionário ou None se não estiver disponível
    """
    try:
        # Obtém o sistema GT da configuração
        gt_system = current_app.config.get('GT_SYSTEM')
        
        # Debug: imprime informações sobre o estado
        if gt_system is None:
            print(f"⚠️  GT_SYSTEM é None na configuração")
            print(f"📋 Configurações disponíveis: {list(current_app.config.keys())}")
        else:
            print(f"✅ GT_SYSTEM encontrado: {type(gt_system)}")
            
        return gt_system
    except Exception as e:
        # Se não conseguir acessar current_app, retorna None
        print(f"❌ Erro ao acessar current_app: {e}")
        return None 