import os
import subprocess
import requests

SPARK_HOME = os.getenv('SPARK_HOME')
if not SPARK_HOME or 'spark2' in SPARK_HOME or 'spark-3.0' in SPARK_HOME or 'spark-3.1' in SPARK_HOME:
    os.environ['SPARK_HOME'] = "/opt/spark/spark-3.3.0-bin-hadoop2"
    os.environ['SPARK_CONF_DIR'] = "/opt/spark/spark-3.3.0-bin-hadoop2/conf"

HADOOP_CONF_DIR = os.getenv('HADOOP_CONF_DIR')
if not HADOOP_CONF_DIR:
    os.environ['HADOOP_CONF_DIR'] = "/etc/hadoop/conf/"

JAVA_HOME = os.getenv('JAVA_HOME')
if not JAVA_HOME:
    os.environ['JAVA_HOME'] = "/usr/jdk64/jdk1.8.0_112"

HADOOP_HOME = os.getenv('HADOOP_HOME')
if not HADOOP_HOME:
    os.environ['HADOOP_HOME'] = "/usr/hdp/3.1.0.0-78/hadoop"

ARROW_LIBHDFS_DIR = os.getenv("ARROW_LIBHDFS_DIR")
if not ARROW_LIBHDFS_DIR:
    os.environ['ARROW_LIBHDFS_DIR'] = "/usr/hdp/3.1.0.0-78/usr/lib/"

try:
    os.environ['CLASSPATH'] = subprocess.check_output("$HADOOP_HOME/bin/hadoop classpath --glob", shell=True).decode(
        'utf-8')
except:
    pass

LIST_JARS = os.getenv('LIST_JARS')
if not LIST_JARS:
    LIST_JARS = """hdfs:///shared/jars/hotpot_2.12-0.0.4-WRITE.jar,hdfs:/shared/jars/datahub-spark-lineage-0.10.11-SNAPSHOT.jar"""

HADOOP_HOST = os.getenv('HADOOP_HOST')
if not HADOOP_HOST:
    HADOOP_HOST = "hdfs://hdfs-cluster.datalake.bigdata.local"
HADOOP_PORT = os.getenv('HADOOP_PORT')
if not HADOOP_PORT:
    HADOOP_PORT = 8020

HIVE_IP_NODES1 = os.getenv('HIVE_IP_NODES1')
if not HIVE_IP_NODES1:
    HIVE_IP_NODES1 = "thrift://master01-dc9c14u40.bigdata.local:9083"
HIVE_IP_NODES2 = os.getenv('HIVE_IP_NODES2')
if not HIVE_IP_NODES2:
    HIVE_IP_NODES2 = "thrift://master02-dc9c14u41.bigdata.local:9083"

no_proxy = os.getenv('no_proxy')
if no_proxy:
    if "git.cads.live,vault.cads.live" in no_proxy:
        pass
    else:
        os.environ['no_proxy'] = os.getenv('no_proxy') + "," + "git.cads.live,vault.cads.live"
else:
    os.environ['no_proxy'] = "git.cads.live,vault.cads.live"


def get_token():
    auth_header = {
        'role_id': 'd70c0b96-6dea-011b-cca8-9b5fe5a5c8a0',
        'secret_id': '42b7a8eb-ed92-5c02-2d2b-d8e3483ab7df'
    }

    # generate token
    try:
        r = requests.post('http://vault.cads.live/v1/auth/approle/login', data=auth_header, timeout=3)
        token = r.json()['auth']['client_token']
    except:
        token = ''
    return token


vault_url = 'http://vault.cads.live/'
secret_path = 'data-platform/data/spark-sdk'
api_url = f'{vault_url}/v1/{secret_path}'

headers = {
    'X-Vault-Token': get_token(),
}

try:
    response = requests.get(api_url, headers=headers, timeout=3)

    data = response.json()
    secret_data = data['data']
    GMS_AUTH_TOKEN = data['data']['data']['GMS_AUTH_TOKEN']
    GMS_URL_KEY = data['data']['data']['GMS_URL_KEY']
except Exception as e:
    GMS_AUTH_TOKEN = ''
    GMS_URL_KEY = 'http://ccatalog-gms.cads.live'

import os
from urllib.parse import urlparse

domain = urlparse(GMS_URL_KEY).netloc
no_proxy = os.getenv('no_proxy')

if no_proxy:
    if f"{domain},git.cads.live,vault.cads.live" in no_proxy:
        pass
    else:
        os.environ['no_proxy'] = os.getenv('no_proxy') + "," + f"{domain},git.cads.live,vault.cads.live"
else:
    os.environ['no_proxy'] = domain + "," + "git.cads.live,vault.cads.live"


def get_spark_home():
    import os
    return os.getenv("SPARK_HOME")


def read_spark_default_conf(spark_dir):
    with open(spark_dir) as f:
        txt = f.read()
    lines = txt.strip().split('\n')
    conf = {}

    # Iterate through each line and split at the first occurrence of whitespace character
    for line in lines:
        if ' ' in line:
            key, value = line.split(None, 1)
            conf[key.strip()] = value.strip()
    return conf


def get_hive_ip():
    SPARK_HOME = get_spark_home()
    SPARK_CONF_DIR = SPARK_HOME + '/conf/spark-defaults.conf'
    if os.path.exists(SPARK_CONF_DIR):
        spark_conf = read_spark_default_conf(spark_dir=SPARK_CONF_DIR)
        if 'spark.hadoop.hive.metastore.uris' in spark_conf:
            return spark_conf['spark.hadoop.hive.metastore.uris']  # .replace("thrift://", "")
        else:
            return HIVE_IP_NODES1

    return HIVE_IP_NODES1
