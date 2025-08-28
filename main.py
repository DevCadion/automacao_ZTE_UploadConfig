from playwright.sync_api import sync_playwright
import time
import os
import subprocess
import sys
import platform

def check_ping(ip_address):
    """Verifica se o IP está respondendo ao ping"""
    try:
        system = platform.system()
        if system == "Windows":
            # -n: number of echo requests, -w: timeout in milliseconds
            command = ["ping", "-n", "2", "-w", "2000", ip_address]
        else:
            # -c: count, -W: timeout in seconds
            command = ["ping", "-c", "2", "-W", "2", ip_address]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Erro ao verificar ping: {e}")
        return False

def upload_config_playwright():
    ROUTER_URL = "http://192.168.1.1/"
    USUARIO = "multipro"
    SENHA = "multipro"
    ARQUIVO_CFG = "default_config.bin"  # Arquivo no mesmo diretório
    DELAY = 500  # 0.5 segundos entre ações

    # Verificar se arquivo existe no diretório atual
    if not os.path.exists(ARQUIVO_CFG):
        print(f"❌ Arquivo não encontrado: {os.path.abspath(ARQUIVO_CFG)}")
        return False

    try:
        with sync_playwright() as p:
            # Configurar browser
            browser = p.chromium.launch(
                headless=False,
                slow_mo=DELAY  # Delay entre ações
            )
            
            context = browser.new_context(
                accept_downloads=True,
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = context.new_page()
            page.set_default_timeout(30000)
            
            # Acessar roteador
            print("🌐 Acessando roteador...")
            page.goto(ROUTER_URL, wait_until='networkidle')
            print("✅ Página carregada")
            
            # Login
            print("🔐 Fazendo login...")
            page.fill("#Frm_Username", USUARIO)
            page.fill("#Frm_Password", SENHA)
            page.click("input[type='submit']")
            
            page.wait_for_load_state('networkidle')
            time.sleep(1)
            print("✅ Login realizado")

            # Verificar assistente
            print("🔍 Verificando se há assistente...")
            try:
                sair_button = page.locator("#Btn_Close")
                sair_button.wait_for(state='visible', timeout=3000)
                
                if sair_button.is_visible():
                    print("⚠️ Assistente detectado, clicando em 'Sair'...")
                    sair_button.click()
                    time.sleep(1)
                    print("✅ Assistente fechado!")
                    
            except Exception as e:
                print("✅ Nenhum assistente detectado")
            
            # Navegação
            print("🧭 Navegando para gerenciamento...")
            page.click("#mgrAndDiag")
            page.wait_for_load_state('networkidle')
            time.sleep(1)
            
            page.click("#devMgr")
            page.wait_for_load_state('networkidle')
            time.sleep(1)
            
            page.click("#defCfgMgr")
            page.wait_for_load_state('networkidle')
            time.sleep(1)
            print("✅ Navegação concluída")

            # Expandir seção
            print("📂 Expandindo seção...")
            try:
                config_section = page.locator("#DefConfUploadBar")
                config_section.wait_for(state='visible', timeout=5000)
                
                class_attribute = config_section.get_attribute('class') or ''
                if 'collapsibleBarExp' not in class_attribute:
                    print("🔽 Expandindo seção...")
                    config_section.click()
                    time.sleep(1)
                    print("✅ Seção expandida!")
                    
            except Exception as e:
                print(f"⚠️ Não foi possível expandir seção: {e}")

            # Upload
            print("📤 Preparando upload...")
            success = False
            
            # Tentar métodos de upload
            methods = [
                lambda: page.locator("#defConfigUpload").set_input_files(ARQUIVO_CFG),
                lambda: page.evaluate("""document.querySelector('#defConfigUpload').style.display='block'""") or \
                        page.locator("#defConfigUpload").set_input_files(ARQUIVO_CFG)
            ]
            
            for i, method in enumerate(methods, 1):
                try:
                    method()
                    print(f"✅ Upload realizado via método {i}!")
                    success = True
                    break
                except Exception as e:
                    print(f"❌ Método {i} falhou: {e}")
            
            if not success:
                print("❌ Todos os métodos de upload falharam")
                browser.close()
                return False

            # Clicar no botão de upload
            print("🔄 Clicando no botão de upload...")
            try:
                page.click("#Btn_Upload")
                time.sleep(1)
                print("✅ Botão de upload clicado!")
            except Exception as e:
                print(f"❌ Erro ao clicar no botão: {e}")
                # Tentar via JS
                page.evaluate("""document.querySelector('#Btn_Upload').click()""")
                print("✅ Botão clicado via JavaScript!")
                time.sleep(1)

            # Confirmação OK
            print("✅ Clicando no botão OK...")
            try:
                confirm_button = page.locator("#confirmOK")
                confirm_button.wait_for(state='visible', timeout=5000)
                confirm_button.click()
                time.sleep(1)
                print("✅ Botão OK clicado!")
            except Exception as e:
                print(f"⚠️ Botão OK não encontrado: {e}")

            # Verificar sucesso
            print("⏳ Aguardando resposta...")
            time.sleep(3)
            
            try:
                success_msg = page.text_content(".succHint")
                print(f"✅ Sucesso: {success_msg}")
            except:
                print("⚠️ Mensagem de sucesso não encontrada")

            # Fechar browser
            browser.close()
            print("🎉 Processo concluído com sucesso!")
            return True
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

def main_loop():
    """Loop principal que monitora os IPs"""
    print("🔄 Iniciando loop de automação de roteador")
    print("📡 Monitorando IPs 192.168.0.1 e 192.168.1.1")
    print("⏹️  Pressione Ctrl+C para parar")
    
    last_action_time = 0
    cooldown = 60  # Esperar 60 segundos entre execuções
    
    try:
        while True:
            current_time = time.time()
            
            # Verificar se estamos no IP 192.168.1.1 e pronto para ação
            if check_ping("192.168.1.1"):
                print("✅ 192.168.1.1 respondendo ao ping")
                
                # Verificar cooldown
                if current_time - last_action_time >= cooldown:
                    print("🚀 Iniciando processo de upload...")
                    if upload_config_playwright():
                        last_action_time = current_time
                        print(f"⏳ Aguardando {cooldown} segundos para próxima execução...")
                    else:
                        print("❌ Falha no processo, tentando novamente mais tarde...")
                else:
                    remaining = cooldown - (current_time - last_action_time)
                    print(f"⏰ Em cooldown: {int(remaining)} segundos restantes")
            
            # Se estamos no IP 192.168.0.1, esperar mudar para 192.168.1.1
            elif check_ping("192.168.0.1"):
                print("🔁 IP 192.168.0.1 detectado, aguardando mudança para 192.168.1.1...")
            
            else:
                print("🌐 Nenhum IP respondendo, aguardando...")
            
            # Esperar 5 segundos entre verificações
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n🛑 Programa interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro no loop principal: {e}")

if __name__ == "__main__":
    # Verificar se estamos no diretório correto
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📁 Diretório atual: {current_dir}")
    
    # Verificar se o arquivo de configuração existe
    config_file = "default_config.bin"
    if not os.path.exists(config_file):
        print(f"❌ Arquivo {config_file} não encontrado no diretório atual")
        print("💡 Certifique-se de que o arquivo está na mesma pasta do script")
    else:
        print(f"✅ Arquivo {config_file} encontrado")
    
    # Iniciar loop principal
    main_loop()
