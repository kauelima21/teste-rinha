import logging
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from app.models import Transacao, Cliente
from app.schemas import TransacaoSchema
from dotenv import load_dotenv
from datetime import datetime


logging.getLogger().setLevel(logging.INFO)
load_dotenv()
app = FastAPI()


@app.post('/clientes/{id}/transacoes')
async def get_transactions(id: int, body: TransacaoSchema):
    c = Cliente()
    cliente = c.find_by_id(id)
    if not cliente:
        logging.info(c.error)
        return JSONResponse(
            {'message': 'O usuario nao existe!'},
            status_code=status.HTTP_404_NOT_FOUND
        )

    transacao = Transacao()
    transacao.id = transacao.find().count() + 1
    transacao.cliente_id = id
    transacao.valor = body.valor
    transacao.tipo = body.tipo
    transacao.descricao = body.descricao
    transacao.realizada_em = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    cliente.saldo = cliente.saldo + body.valor if body.tipo == 'c' else cliente.saldo - body.valor

    if transacao.save() and cliente.save():
        return JSONResponse(
            {'limite': cliente.limite, 'saldo': cliente.saldo},
            status_code=status.HTTP_200_OK
        )

    return JSONResponse(
        {'message': transacao.error},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@app.get('/clientes/{id}/extrato')
async def get_extract(id: int):
    c = Cliente()
    cliente = c.find_by_id(id)
    if not cliente:
        logging.info(c.error)
        return JSONResponse(
            {'message': 'O usuario nao existe!'},
            status_code=status.HTTP_404_NOT_FOUND
        )

    transacoes = Transacao().query_by(
        'cliente_id',
        id,
        'cliente_id-index'
    ).attributes_to_get('valor,tipo,descricao,realizada_em').limit(10).order('realizada_em', False).fetch()

    response = {
        'saldo': {
            'total': cliente.saldo,
            'data_extrato': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'limite': cliente.limite,
        },
        'ultimas_transacoes': transacoes,
    }
    return JSONResponse(
        response,
        status_code=status.HTTP_200_OK
    )
