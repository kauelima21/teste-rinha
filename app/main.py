import logging
import pytz
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from app.models import Transacao, Cliente
from app.schemas import TransacaoSchema
from dotenv import load_dotenv
from datetime import datetime


logging.getLogger().setLevel(logging.INFO)
load_dotenv()
app = FastAPI()
timezone = pytz.timezone('America/Sao_Paulo')


@app.post('/clientes/{id}/transacoes')
async def post_transactions(id: int, body: TransacaoSchema):
    cliente = Cliente().find_by_id(id)
    if not cliente:
        return JSONResponse(
            {'message': 'O usuario nao existe!'},
            status_code=status.HTTP_404_NOT_FOUND
        )

    new_balance = cliente.saldo + body.valor if body.tipo == 'c' else cliente.saldo - body.valor

    if new_balance < (-cliente.limite):
        return JSONResponse(
            {'message': 'Transacoes nao podem deixar o saldo do cliente menor que o seu limite'},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    cliente.saldo = new_balance
    transacao = Transacao()
    transacao.id = transacao.find().count() + 1
    transacao.cliente_id = id
    transacao.valor = body.valor
    transacao.tipo = body.tipo
    transacao.descricao = body.descricao
    transacao.realizada_em = datetime.now(timezone).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    logging.info('Creating Transaction...')

    error_message = ''
    if transacao.save():
        if cliente.save():
            return JSONResponse(
                {'limite': cliente.limite, 'saldo': cliente.saldo},
                status_code=status.HTTP_200_OK
            )
        transacao.destroy()
        error_message = cliente.error
    else:
        error_message = transacao.error

    return JSONResponse(
        {'message': error_message},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@app.get('/clientes/{id}/extrato')
async def get_extract(id: int):
    cliente = Cliente().find_by_id(id)
    if not cliente:
        return JSONResponse(
            {'message': 'O usuario nao existe!'},
            status_code=status.HTTP_404_NOT_FOUND
        )

    transacoes = (Transacao().query_by(
        'cliente_id',
        id,
        'cliente_id-index'
    ).attributes_to_get('valor,tipo,descricao,realizada_em')
                  .limit(10)
                  .order('realizada_em', False)
                  .fetch())

    response = {
        'saldo': {
            'total': cliente.saldo,
            'data_extrato': datetime.now(timezone).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'limite': cliente.limite,
        },
        'ultimas_transacoes': transacoes,
    }
    return JSONResponse(
        response,
        status_code=status.HTTP_200_OK
    )
