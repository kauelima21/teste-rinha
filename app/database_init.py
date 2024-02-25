import logging
import boto3
import os
import time
from dotenv import load_dotenv


logging.getLogger().setLevel(logging.INFO)
load_dotenv()


dynamodb = boto3.resource(
    'dynamodb',
    region_name='sa-east-1',
    endpoint_url=os.getenv('LOCAL_ENDPOINT', 'http://localhost:8000')
)
client = boto3.client(
    'dynamodb',
    region_name='sa-east-1',
    endpoint_url=os.getenv('LOCAL_ENDPOINT', 'http://localhost:8000')
)

__table_names__ = ['transacoes', 'clientes']


def table_info(table_name):
    info = {
        'transacoes': {
            'TableName': 'transacoes',
            'KeySchema': [
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'cliente_id',
                    'AttributeType': 'N'
                }
            ],
            'BillingMode': 'PAY_PER_REQUEST',
            'GlobalSecondaryIndexes': [
                {
                    'IndexName': 'cliente_id-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'cliente_id',
                            'KeyType': 'HASH'
                        },
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 10,
                        'WriteCapacityUnits': 10
                    }
                }
            ]
        },
        'clientes': {
            'TableName': 'clientes',
            'KeySchema': [
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                }
            ],
            'BillingMode': 'PAY_PER_REQUEST'
        }
    }

    return info[table_name]


def create_table(table_name):
    response = dynamodb.create_table(**table_info(table_name))
    response.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    return table_name


def populate_clients():
    data = [
        {'id': 1, 'limite': 100000, 'saldo': 0},
        {'id': 2, 'limite': 80000, 'saldo': 0},
        {'id': 3, 'limite': 1000000, 'saldo': 0},
        {'id': 4, 'limite': 1000000, 'saldo': 0},
        {'id': 5, 'limite': 500000, 'saldo': 0},
    ]
    table = dynamodb.Table('clientes')
    with table.batch_writer() as batch:
        for cliente in data:
            table.put_item(Item=cliente)


if __name__ == '__main__':
    try:
        logging.info('starting dump...')
        time.sleep(10)
        tables = client.list_tables()['TableNames']
        for name in __table_names__:
            if name not in tables:
                logging.info('creating table...')
                create_table(name)
                if name == 'clientes':
                    logging.info('populating table...')
                    populate_clients()
    except:
        print('O banco ainda nao subiu, pode rodar dnv? :)')
