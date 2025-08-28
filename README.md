# 🚀 Automação ZTE Config Upload

Este projeto é uma automação em **Python** que realiza o upload do arquivo `default_config.bin` para roteadores **ZTE** de forma automática.  
A automação utiliza a biblioteca **Playwright** para controlar o navegador e realizar o processo de upload.

---

## 📂 Estrutura do Projeto

```text
.
├── default_config.bin   # Arquivo de configuração padrão a ser enviado
├── main.py              # Script principal da automação
├── LICENSE              # Licença do projeto
└── README.md            # Este arquivo
⚙️ Pré-requisitos
Python 3.8+ instalado

pip atualizado

## Atualize o pip antes de iniciar:

bash
Copiar código
python -m pip install --upgrade pip
🔧 Configuração do Ambiente
1. Clone o repositório
bash
Copiar código
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
2. Crie e ative o ambiente virtual
🔹 Linux / macOS
bash
Copiar código
python3 -m venv .venv
source .venv/bin/activate
🔹 Windows (PowerShell)
bash
Copiar código
python -m venv .venv
.venv\Scripts\Activate
3. Instale as dependências necessárias
bash
Copiar código
pip install playwright
4. Instale o navegador necessário
bash
Copiar código
playwright install chromium
▶️ Executando a Automação
Com o ambiente virtual ativo, execute o script principal:

bash
Copiar código
python main.py
O script abrirá o navegador, acessará o painel do roteador ZTE e fará o upload do arquivo default_config.bin.

📝 Personalização
Antes de executar, edite o arquivo main.py para configurar:

IP do roteador (padrão: 192.168.1.1)

Credenciais de acesso (usuário e senha)

Caminho do arquivo de configuração, se necessário

⚠️ Notas Importantes
Certifique-se de que o roteador está acessível na rede

Verifique se as credenciais padrão foram alteradas no roteador

O processo de upload pode reiniciar o roteador automaticamente

📄 Licença
Este projeto está sob a licença MIT.
Veja o arquivo LICENSE para mais detalhes.

🤝 Contribuições
Contribuições são bem-vindas!
Sinta-se à vontade para abrir issues e pull requests.