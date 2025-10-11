# 🚀 Solução Híbrida: Apache Airflow + PostgreSQL + MinIO

Este projeto integra três componentes principais para orquestração de dados e armazenamento:

- **Apache Airflow**: Orquestração de workflows
- **PostgreSQL**: Banco de dados relacional para metadados do Airflow
- **MinIO**: Armazenamento de objetos compatível com S3

A base foi clonada do repositório do Adriano e adaptada para incluir os três serviços integrados. Os artefatos de código (DAGs, scripts, configurações) estão versionados neste repositório.

---

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

### 2.1 Passo opcional de verificação
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
| **MinIO Console**   | [http://localhost:9001](http://localhost:9001) | 9001  | `minioadmin` / `minioadmin`| —                  | Interface web de armazenamento S3   |
| **MinIO API S3**    | `http://localhost:9000`                | 9000  | `minioadmin` / `minioadmin`| —                  | Usado por boto3, S3Hook, etc.        |
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
