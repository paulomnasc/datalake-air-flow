FROM apache/airflow:2.9.1

USER airflow

RUN pip install --no-cache-dir pyspark minio

CMD ["airflow", "webserver"]

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]