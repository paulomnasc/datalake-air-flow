````markdown
# Setup de Laboratório Airflow + PostgreSQL em Oracle Cloud

Este guia descreve os passos para configurar uma VM na **Oracle Cloud**, preparar rede e rodar **Airflow + PostgreSQL via Docker**.

---

## 0. Criar a instância Oracle Cloud

1. Acesse o console: [https://cloud.oracle.com](https://cloud.oracle.com)  
2. Navegue em **Compute → Instances → Create Instance**  
3. Configure a VM:
   - **Shape:** `VM.Standard.E2.4`  
     - 4 OCPUs  
     - 16 GB RAM  
   - **Sistema operacional:** Ubuntu 22.04 LTS  
   - **Boot Volume:** 50–100 GB SSD (dependendo do uso)  
4. Clique em **Create** para inicializar a instância.


Claro, Cristiane! Aqui está o passo a passo para instalar o Docker no Oracle Linux, formatado em **Markdown compatível com GitHub**:

```markdown
# 🐳 Instalação do Docker no Oracle Linux 8

Este guia mostra como instalar o Docker Engine em uma instância Oracle Linux 8 usando o repositório oficial da Docker.

---

## ✅ Pré-requisitos

- Instância Oracle Linux 8 ativa
- Acesso via terminal com permissões de `sudo`
- Conexão com a internet

---

## 📦 Passo a passo

### 1. Atualize o sistema

```bash
sudo dnf update -y
```

### 2. Instale utilitários necessários

```bash
sudo dnf install -y dnf-utils zip unzip
```

### 3. Adicione o repositório oficial da Docker

```bash
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

> ℹ️ Apesar de mencionar CentOS, esse repositório funciona para Oracle Linux.

### 4. Instale o Docker Engine

```bash
sudo dnf install -y docker-ce docker-ce-cli containerd.io
```

### 5. Inicie e habilite o serviço Docker

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### 6. Verifique se o Docker está funcionando

```bash
docker --version
sudo docker run hello-world
```

### 7. (Opcional) Use Docker sem sudo

```bash
sudo usermod -aG docker $USER
```

> 🔁 Faça logout e login novamente para aplicar a mudança.

---

## 🔍 Verifique a distribuição (opcional)

```bash
cat /etc/os-release
```

---

## 📚 Fontes úteis

- [Instalação via ORACLE-BASE](https://oracle-base.com/articles/linux/docker-install-docker-on-oracle-linux-ol8)
- [Guia Collabnix](https://collabnix.com/how-to-install-docker-on-oracle-linux-a-step-by-step-guide/)

Isso significa que o **Docker Compose não está instalado** na sua máquina Oracle Linux. Vamos resolver isso rapidinho! 🚀

---

## 🛠️ Como instalar o Docker Compose no Oracle Linux

### ✅ Passo 1: Verifique a versão mais recente
```bash
sudo curl -s https://api.github.com/repos/docker/compose/releases/latest | grep tag_name
```

Isso vai mostrar algo como `"tag_name": "v2.24.1"` — copie esse número.

### ✅ Passo 2: Baixe o binário do Docker Compose
Substitua `v2.24.1` pela versão mais recente que você encontrou:

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

### ✅ Passo 3: Dê permissão de execução
```bash
sudo chmod +x /usr/local/bin/docker-compose
```

### ✅ Passo 4: Verifique se funcionou
```bash
docker-compose --version
```

Você deve ver algo como:

```bash
Docker Compose version v2.24.1
```

---

## 💡 Dica extra: Autocompletar no terminal (opcional)

```bash
sudo curl -L https://raw.githubusercontent.com/docker/compose/v2.24.1/contrib/completion/bash/docker-compose -o /etc/bash_completion.d/docker-compose
```

---

Se quiser, posso te ajudar a configurar o `docker-compose.yml` ou subir seu projeto com containers. Só dizer!

