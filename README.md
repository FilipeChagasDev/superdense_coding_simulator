# superdense_coding_simulator

Streamlit web app para simular o protocolo de comunicação quântica de codificação superdensa (Superdense Coding).

## 🚀 Como executar localmente

1. Crie e ative um ambiente virtual Python:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o app:
   ```bash
   streamlit run app.py
   ```

## 🌐 Deploy na Streamlit Cloud

### Pré-requisitos
- Conta no [Streamlit Cloud](https://streamlit.io/cloud)
- Repositório GitHub com o código

### Passos para Deploy

1. **Faça push do código para GitHub** (se ainda não fez):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/seu-usuario/superdense_coding_simulator.git
   git push -u origin main
   ```

2. **Acesse Streamlit Cloud**:
   - Vá para [share.streamlit.io](https://share.streamlit.io)
   - Clique em "New app"
   - Selecione seu repositório GitHub
   - Selecione a branch: `main`
   - Defina o caminho do arquivo principal: `app.py`
   - Clique em "Deploy"

3. **Aguarde o deploy** - Streamlit Cloud instalará as dependências e iniciará seu app automaticamente.

### Configuração de Secrets (se necessário)

Se precisar de variáveis de ambiente, crie um arquivo `.streamlit/secrets.toml`:
```toml
# .streamlit/secrets.toml
# Adicione suas variáveis aqui
# Este arquivo NÃO será commitado no git
```

Isso será automaticamente ignorado pelo `.gitignore`.

## 📋 Arquivo de Configuração Streamlit

O arquivo `.streamlit/config.toml` já está configurado com as melhores práticas para Streamlit Cloud:
- `headless = true`: Modo sem interface de navegador
- `enableXsrfProtection = true`: Proteção CSRF ativada
- Tema personalizado com cores otimizadas

## 📚 Sobre Codificação Superdensa

**Superdense Coding** é um protocolo de comunicação quântica que permite transmitir **2 bits clássicos** usando apenas **1 qubit quântico** compartilhado entre Alice e Bob.

### Como Funciona:
1. Bob prepara um par quântico emaranhado (estado de Bell)
2. Alice recebe um qubit e aplica operações unitárias que codificam 2 bits clássicos (00, 01, 10 ou 11)
3. Bob realiza uma medição conjunta (medição de Bell) e recupera os 2 bits originais

### Segurança do Protocolo:
- **Detecção de Espionagem**: Se um interceptador (Eve) medir o qubit antes de Bob, o emaranhamento é quebrado
- **Colapso Quântico**: Qualquer medição não autorizada colapsa o estado
- **Teorema da Não-Clonagem**: Eve não pode copiar o qubit sem deixar rastros

## 🔧 Dependências

- `streamlit`: Framework web interativo
- `qiskit`: Computação quântica
- `qiskit-aer`: Simulador quântico local
- `matplotlib`: Visualização de circuitos
- `pandas`: Manipulação de dados
- `pylatexenc`: Formatação LaTeX

## 📄 Licença

Veja [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

Desenvolvido por **Filipe Chagas Ferraz** ([github.com/filipechagasdev](https://github.com/filipechagasdev))
