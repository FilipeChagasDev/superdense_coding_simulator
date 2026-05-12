# Guia de Deployment - Streamlit Cloud

Este guia fornece instruções detalhadas para fazer deploy da aplicação Superdense Coding Simulator na Streamlit Cloud.

## 📋 Pré-requisitos

- Conta no GitHub com o repositório do projeto
- Conta no [Streamlit Cloud](https://streamlit.io/cloud) (gratuita!)
- Ter feito push do código para o GitHub

## 🚀 Passos para Deploy

### 1. Preparar o Repositório GitHub

Certifique-se de que todos os arquivos necessários estão no repositório:

```
superdense_coding_simulator/
├── app.py                    # Arquivo principal
├── requirements.txt          # Dependências
├── README.md                 # Documentação
├── .streamlit/
│   └── config.toml          # Configuração Streamlit
├── .gitignore               # Arquivos ignorados
└── LICENSE                  # Licença (opcional)
```

### 2. Acessar Streamlit Cloud

1. Vá para [share.streamlit.io](https://share.streamlit.io)
2. Clique no botão **"New app"** (canto superior direito)
3. Se não estiver logado, faça login com sua conta GitHub

### 3. Configurar o Deploy

Na página de criação de novo app:

1. **Repository**: Selecione `FilipeChagasDev/superdense_coding_simulator`
2. **Branch**: Selecione `main`
3. **Main file path**: Defina como `app.py`

### 4. Verificar URL do App

Após clicar em "Deploy", o Streamlit Cloud irá:
- Instalar as dependências do `requirements.txt`
- Iniciar o servidor
- Fornecer uma URL pública para seu app

Exemplo: `https://seu-app-name-streamlit.app`

## 🔧 Configurações Importantes

### Performance

O arquivo `.streamlit/config.toml` já existe com otimizações:

```toml
[server]
headless = true                    # Modo sem interface de navegador
enableXsrfProtection = true        # Proteção contra CSRF
maxUploadSize = 200                # Tamanho máximo de upload (MB)

[client]
showErrorDetails = false           # Não mostra detalhes de erro em produção
```

### Cache

A aplicação utiliza `@st.cache_resource` e `@st.cache_data` para otimizar a performance:
- `get_simulator()`: Cacheado como recurso (reutilizado entre sessões)
- `build_superdense_coding_circuit()`: Cacheado como dados (reutilizado para mesmos parâmetros)

## 🔐 Variáveis de Ambiente (se necessário)

Para adicionar variáveis de ambiente (API keys, etc.):

1. Crie um arquivo `.streamlit/secrets.toml` **localmente** (não commit no Git):
   ```toml
   # .streamlit/secrets.toml
   api_key = "seu_api_key_aqui"
   ```

2. No Streamlit Cloud:
   - Vá para configurações do app (⚙️)
   - Navegue até "Secrets"
   - Adicione suas variáveis

3. No código, acesse com:
   ```python
   api_key = st.secrets["api_key"]
   ```

## 🐛 Troubleshooting

### App não inicia
- Verifique o `requirements.txt` para versões compatíveis
- Veja os logs do deployment em "Manage app" → "Logs"

### Erro: `ModuleNotFoundError`
- Adicione a dependência ao `requirements.txt`
- Remova a cópia anterior do app em "Manage app" → "Reboot app"

### Performance lenta
- O simulator de Qiskit pode demorar em máquinas virtuais
- Reduza o número máximo de shots no app
- Use `@st.cache_data` para operações determinísticas

### Memory limit exceeded
- Streamlit Cloud tem limite de memória (~1GB)
- Reduza o tamanho do número de shots
- Considere usar simuladores menores

## 📦 Atualizar a Aplicação

Quando fazer mudanças no código:

1. Commitar e fazer push para o GitHub:
   ```bash
   git add .
   git commit -m "Descrição das mudanças"
   git push origin main
   ```

2. Streamlit Cloud automaticamente detectará as mudanças e fará redeploy

## 🌍 Domínio Customizado (Plano Pro)

Se usar o plano Pro do Streamlit Cloud, você pode configurar um domínio customizado.

## 📚 Recursos Adicionais

- [Documentação Streamlit Cloud](https://docs.streamlit.io/streamlit-cloud)
- [Streamlit Configuration](https://docs.streamlit.io/library/advanced-features/configuration)
- [Qiskit Documentation](https://qiskit.org/documentation/)

## ✅ Checklist Final

- [ ] Código está no GitHub
- [ ] `requirements.txt` atualizado com todas as dependências
- [ ] `.streamlit/config.toml` configurado
- [ ] `.gitignore` contém `.streamlit/secrets.toml`
- [ ] README.md tem instruções claras
- [ ] Testou localmente com `streamlit run app.py`
- [ ] Fez deploy na Streamlit Cloud com sucesso

---

**Pronto!** Seu app está agora acessível online! 🎉
