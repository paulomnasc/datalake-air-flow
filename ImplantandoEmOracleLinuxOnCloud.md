````markdown
# Setup de Laboratório Airflow + PostgreSQL em Oracle Cloud

Este guia descreve os passos para configurar uma VM na **Oracle Cloud**, preparar rede e rodar **Airflow + PostgreSQL via Docker**.

---

## 1. Criar a instância Oracle Cloud

1. Acesse o console: [https://cloud.oracle.com](https://cloud.oracle.com)  
2. Navegue em **Compute → Instances → Create Instance**  
3. Configure a VM:
   - **Shape:** `VM.Standard.E2.4`  
     - 4 OCPUs  
     - 16 GB RAM  
   - **Sistema operacional:** Ubuntu 22.04 LTS  
   - **Boot Volume:** 50–100 GB SSD (dependendo do uso)  
4. Clique em **Create** para inicializar a instância.
