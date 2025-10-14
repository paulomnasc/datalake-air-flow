# 🚀 Solução Híbrida: Apache Airflow + PostgreSQL + MinIO

Este projeto integra três componentes principais para orquestração de dados e armazenamento:

- **Apache Airflow**: Orquestração de workflows
- **PostgreSQL**: Banco de dados relacional para metadados do Airflow
- **MinIO**: Armazenamento de objetos compatível com S3

A base foi clonada do repositório do Adriano e adaptada para incluir os três serviços integrados. Os artefatos de código (DAGs, scripts, configurações) estão versionados neste repositório.

---

## Configuração mínima de hardware

Os requisitos mínimos de hardware para um Apache Airflow básico são de 10GB de HD, 4GB de RAM e 2 CPUs. 

É importante notar que, para uma implantação em produção, pode ser necessário mais hardware, dependendo da carga de trabalho, e que o Airflow também pode rodar em ambientes como Kubernetes ou nuvem, com requisitos que variam de acordo com a plataforma escolhida. 
Requisitos mínimos (para ambientes de teste/desenvolvimento):

Disco: 10 GB de HD.
Memória: 4 GB de RAM.
Processador (CPU): 2 CPUs (ou VCPUs). 
Requisitos recomendados e considerações adicionais:
Banco de dados: O Airflow precisa de um banco de dados de metadados para funcionar. 
É recomendado um banco de dados como PostgreSQL ou MySQL. 

Ambiente virtual: Para evitar conflitos de dependências, é altamente recomendável usar um ambiente virtual (como o venv ou conda). 
Sistema operacional: Embora o Airflow possa ser instalado em Windows, ele funciona melhor em um ambiente tipo Unix, como o Linux, que pode ser executado nativamente ou através do Subsistema do Windows para Linux (WSL). 

Ambientes de nuvem: Se for usar serviços como Amazon MWAA, os requisitos de hardware são variáveis e o pagamento é por uso. Os custos e recursos dependem do nível de uso. 

## 📁 Estrutura do Projeto

```
airflow-spark-minio-postgres/
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
└── src/
    └── dags/
        └── suas_dags.py
```

---

## ⚙️ Etapas de Implantação

### 1. Clonar o Projeto

```bash
git clone https://github.com/paulomnasc/datalake-air-flow.git
cd datalake-air-flow
```

> Substitua o link acima pelo repositório real, se necessário.

---

### 2. Build e Inicialização dos Containers

```bash
chmod +x entrypoint.sh
docker-compose down --remove-orphans
docker-compose build
docker-compose up -d
```

> Neste momento:
> - O **PostgreSQL** é instanciado com o banco `airflow`, usuário `airflow` e senha `airflow`
> - O **MinIO** é iniciado com o volume `/data` e console web na porta 9001
> - O **Airflow Webserver e Scheduler** são construídos e iniciados com base nas variáveis de ambiente

---

### 2.1 Passo opcional de verificação se o Airflow está Up (opercional)
```bash
docker exec -it airflow-webserver airflow dags list

```

### 3. Inicializar o Banco de Dados do Airflow (! Apenas novas instalações)

```bash
docker exec -it airflow-webserver airflow db init
```

> Esse comando aplica as migrações e cria as tabelas no banco `airflow` do PostgreSQL.

---

### 4. Criar Usuário Admin no Airflow (! Apenas novas instalações)

Via CLI:

```bash
docker exec -it airflow-webserver airflow users create \
  --username admin \
  --firstname Air \
  --lastname Flow \
  --role Admin \
  --email admin@example.com \
  --password admin
```

Ou via DAG já incluída no projeto.

---

## 🌐 Consoles Administrativas e Acesso

| Serviço             | Endereço de Acesso                     | Porta | Usuário / Senha           | Banco de Dados     | Observações                          |
|---------------------|----------------------------------------|-------|----------------------------|--------------------|--------------------------------------|
| **Airflow UI**      | [http://localhost:8085](http://localhost:8085) | 8085  | `admin` / `admin`          | —                  | Criado após `airflow db init` e `users create` |
| **MinIO Console**   | [http://localhost:9001](http://localhost:9001) | 9001  | `admin` / `admin123`| —                  | Interface web de armazenamento S3   |
| **MinIO API S3**    | `http://localhost:9000`                | 9000  | `admin` / `admin123`| —                  | Usado por boto3, S3Hook, etc.        |
| **PostgreSQL**      | via cliente externo ou terminal        | 5432  | `airflow` / `airflow`      | `airflow`          | Banco de metadados do Airflow        |

---

## 🧪 Testes de Acesso

### Airflow:

```bash
curl http://localhost:8085
```

### MinIO:

```bash
curl http://localhost:9001
```

### PostgreSQL via terminal:

```bash
docker exec -it postgres psql -U airflow -d airflow
```

---

## ✅ Status Final

Com essa implantação:

- Airflow está orquestrando suas DAGs com interface acessível
- MinIO está disponível como armazenamento S3 local
- PostgreSQL está persistindo os metadados e acessível via terminal ou cliente gráfico
- Todos os serviços estão integrados e prontos para produção ou desenvolvimento local

### Configurando o Airflow para conectar no MinIO

## 🔗 Conexão Airflow com MinIO (`minio_conn`)

Para que o Airflow consiga enviar arquivos para o MinIO usando `S3Hook`, é necessário configurar uma conexão do tipo **Amazon S3** com os seguintes parâmetros:

### 📋 Detalhes da conexão

- **Conn Id**: `minio_conn`
- **Conn Type**: `Amazon Web Serices`
- **Login**: `admin` *(Access Key do MinIO)*
- **Password**: `admin123` *(Secret Key do MinIO)*

### ⚙️ Campo Extra (JSON)

```json
{
  "host": "http://minio:9000",
  "port": 9000,
  "secure": false
}
```

### Utilidades

### ✅ 6. Reiniciar o Airflow

Se for necessário, reinicie o Airflow:

```bash
docker restart airflow-webserver
```
**O comando mais direto para verificar se o Airflow carregou totalmente é:**

```bash
docker logs <nome_do_container_airflow>
```

Por exemplo, se estiver usando Docker Compose e seu serviço se chama `airflow`, você pode usar:

```bash
docker logs datalake-local_airflow_1
```

---

### 🧩 O que procurar nos logs

Você saberá que o Airflow carregou com sucesso quando encontrar mensagens como:

```
Scheduler started...
Starting webserver at http://0.0.0.0:8080
```

Essas mensagens indicam que tanto o *scheduler* quanto o *webserver* estão ativos e prontos.

---

### ✅ Alternativas úteis

Se estiver usando o Airflow fora de containers, você pode verificar com:

```bash
airflow webserver
```

ou

```bash
airflow scheduler
```

E observar no terminal se os serviços iniciam sem erros.
---

Navegar um recurso com interface amigável 

```bash
mc ls local/lab01/processed/raw/
```
