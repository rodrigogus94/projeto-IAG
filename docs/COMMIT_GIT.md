# 📤 Como Fazer Commit e Push para o Git

## 🆕 Inicializar Repositório Git (Primeira Vez)

Se o projeto ainda não tem Git inicializado:

### 1. Inicializar Git

```bash
git init
```

### 2. Configurar Git (se ainda não fez)

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

### 3. Adicionar Remote (se tiver repositório remoto)

```bash
git remote add origin <URL_DO_SEU_REPOSITORIO>
```

Exemplo:
```bash
git remote add origin https://github.com/seu-usuario/projeto-sdk-mk00.git
```

---

## 📋 Passo a Passo para Commit e Push

### 1. Verificar Status

```bash
git status
```

Isso mostrará todos os arquivos modificados, adicionados e removidos.

---

### 2. Adicionar Todas as Mudanças

```bash
git add .
```

Isso adiciona todos os arquivos novos e modificados ao staging.

---

### 3. Verificar o que será commitado

```bash
git status
```

Você deve ver os arquivos listados em verde (prontos para commit).

---

### 4. Fazer o Commit

```bash
git commit -m "Reorganizar projeto em estrutura modular

- Organizar código em src/core e src/config
- Mover testes para pasta tests/
- Mover documentação para pasta docs/
- Mover scripts para pasta scripts/
- Atualizar todos os imports para nova estrutura
- Adicionar scripts auxiliares de execução
- Corrigir imports e paths de dados"
```

**Ou mensagem mais curta:**

```bash
git commit -m "Reorganizar projeto em estrutura modular com pastas"
```

---

### 5. Fazer Push para o Repositório Remoto

#### Se é a primeira vez (criar branch main):

```bash
git branch -M main
git push -u origin main
```

#### Se já existe a branch:

```bash
git push origin main
```

**Ou se sua branch for `master`:**

```bash
git push origin master
```

---

## 📁 Arquivos que DEVEM ser commitados

✅ **Commitar:**
- `src/` - Todo o código fonte
- `tests/` - Todos os testes
- `docs/` - Documentação
- `scripts/` - Scripts utilitários
- `requirements.txt` - Dependências
- `README.md` - Documentação principal
- `.gitignore` - Arquivos ignorados
- `run_app.bat` / `run_app.sh` - Scripts auxiliares

❌ **NÃO commitar (já no .gitignore):**
- `__pycache__/` - Cache Python
- `data/` - Dados gerados (logs, histórico)
- `.env` - Variáveis de ambiente sensíveis
- `*.pyc` - Arquivos compilados Python
- `logs/` - Logs antigos
- `chat_history/` - Histórico antigo

---

## 🔍 Verificar Mudanças Antes do Commit

### Ver diferenças detalhadas:

```bash
git diff
```

### Ver arquivos que serão commitados:

```bash
git diff --cached
```

### Ver resumo das mudanças:

```bash
git status --short
```

---

## 🛡️ Verificar .gitignore

O `.gitignore` já está configurado para ignorar:
- ✅ `__pycache__/` - Cache Python
- ✅ `data/` - Dados gerados
- ✅ `.env` - Variáveis de ambiente
- ✅ `logs/` - Logs
- ✅ `chat_history/` - Histórico antigo

---

## 🔄 Se já existe um repositório remoto

### 1. Verificar branch atual:

```bash
git branch
```

### 2. Verificar remote:

```bash
git remote -v
```

### 3. Atualizar antes de push (recomendado):

```bash
git pull origin main
```

### 4. Fazer push:

```bash
git push origin main
```

---

## ⚠️ Resolver Conflitos

Se houver conflitos ao fazer pull:

```bash
# 1. Fazer pull primeiro
git pull origin main

# 2. Resolver conflitos manualmente nos arquivos
# (o Git marcará os conflitos com <<<<<<, ======, >>>>>>)

# 3. Adicionar arquivos resolvidos
git add .

# 4. Fazer commit
git commit -m "Resolver conflitos"

# 5. Fazer push
git push origin main
```

---

## 📝 Mensagens de Commit Sugeridas

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
- Atualizar .gitignore para nova estrutura
```

### Versão curta:

```
Reorganizar projeto: estrutura modular com pastas
```

---

## ✅ Checklist Antes do Push

- [ ] Todos os arquivos importantes foram adicionados
- [ ] `.gitignore` está configurado corretamente
- [ ] Não há arquivos sensíveis (`.env`, senhas)
- [ ] Testes passam: `python tests/run_tests.py`
- [ ] Aplicação funciona: `streamlit run src/app.py`
- [ ] Mensagem de commit é clara e descritiva
- [ ] Branch está atualizada (se já existe remoto)

---

## 🚀 Comandos Rápidos (Resumo)

```bash
# 1. Ver status
git status

# 2. Adicionar tudo
git add .

# 3. Commit
git commit -m "Reorganizar projeto em estrutura modular"

# 4. Push
git push origin main

# 5. Ver histórico
git log --oneline -5
```

---

## 🆘 Problemas Comuns

### Erro: "fatal: not a git repository"

**Solução:** Execute `git init` primeiro.

### Erro: "remote origin already exists"

**Solução:** O remote já existe, pode pular essa etapa.

### Erro: "failed to push some refs"

**Solução:** 
```bash
git pull origin main --rebase
git push origin main
```

### Erro: "authentication failed"

**Solução:** Configure suas credenciais Git ou use SSH keys.

---

## 📚 Próximos Passos

Após fazer push:

1. Verificar no GitHub/GitLab se os arquivos foram enviados
2. Criar uma tag de versão (opcional):
   ```bash
   git tag -a v1.0.0 -m "Versão reorganizada"
   git push origin v1.0.0
   ```
3. Criar uma release no GitHub (opcional)
