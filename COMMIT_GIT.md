# 📤 Como Fazer Commit e Push para o Git

## ⚡ Comandos Rápidos

Execute estes comandos **na raiz do projeto** (onde está o `README.md`):

```bash
# 1. Verificar status
git status

# 2. Adicionar todos os arquivos
git add .

# 3. Fazer commit
git commit -m "Reorganizar projeto em estrutura modular"

# 4. Adicionar remote (apenas primeira vez - substitua pela URL do seu repositório)
git remote add origin https://github.com/seu-usuario/projeto-sdk-mk00.git

# 5. Fazer push
git push -u origin main
```

---

##  Passo a Passo Completo

###  Se é a primeira vez (novo repositório):

```bash
# 1. Inicializar Git
git init

# 2. Adicionar todos os arquivos
git add .

# 3. Fazer primeiro commit
git commit -m "Reorganizar projeto em estrutura modular

- Organizar código em src/core e src/config
- Mover testes para pasta tests/
- Mover documentação para pasta docs/
- Mover scripts para pasta scripts/
- Atualizar imports para nova estrutura
- Adicionar scripts auxiliares de execução"

# 4. Criar branch main
git branch -M main

# 5. Adicionar remote (substitua pela URL do seu repositório)
git remote add origin https://github.com/seu-usuario/projeto-sdk-mk00.git

# 6. Fazer push
git push -u origin main
```

###  Se já tem Git configurado:

```bash
# 1. Ver status
git status

# 2. Adicionar mudanças
git add .

# 3. Commit
git commit -m "Reorganizar projeto em estrutura modular"

# 4. Push
git push origin main
```

---

##  Arquivos que serão commitados

-  `src/` - Todo o código fonte
-  `tests/` - Todos os testes
-  `docs/` - Documentação
-  `scripts/` - Scripts utilitários
-  `requirements.txt` - Dependências
-  `README.md` - Documentação principal
-  `.gitignore` - Arquivos ignorados
-  `run_app.bat` / `run_app.sh` - Scripts auxiliares
-  `COMMIT_GIT.md` - Este guia

---

##  Arquivos que NÃO serão commitados

O `.gitignore` já está configurado para ignorar:
-  `__pycache__/` - Cache Python
-  `data/` - Dados gerados (logs, histórico)
-  `.env` - Variáveis de ambiente sensíveis
-  `logs/` - Logs antigos
-  `chat_history/` - Histórico antigo
-  `organize_project.py` - Script temporário (opcional)

---

##  Mensagem de Commit Sugerida

### Versão detalhada:

```
Reorganizar projeto em estrutura modular

- Separar código em src/core e src/config
- Organizar testes em pasta tests/
- Centralizar documentação em docs/
- Criar pasta scripts/ para utilitários
- Atualizar imports para nova estrutura
- Corrigir paths de dados (logs, histórico)
- Adicionar scripts auxiliares de execução
```

### Versão curta:

```
Reorganizar projeto em estrutura modular
```

---

##  Verificar antes de commitar

```bash
# Ver o que será commitado
git status

# Ver diferenças detalhadas
git diff --cached
```

---

##  Importante

1. **Execute sempre da raiz do projeto** (onde está o `README.md`)
2. **Verifique o `.gitignore`** - certifique-se de que arquivos sensíveis não serão commitados
3. **Não commite `.env`** - contém informações sensíveis
4. **Não commite `data/`** - são dados gerados

---

##  Problemas Comuns

### "fatal: not a git repository"
```bash
git init
```

### "remote origin already exists"
O remote já existe, pode pular a etapa de adicionar remote.

### "failed to push some refs"
```bash
git pull origin main --rebase
git push origin main
```

### "authentication failed"
Configure suas credenciais Git ou use SSH keys.

---

##  Documentação Completa

Para mais detalhes, veja: `docs/COMMIT_GIT.md`
