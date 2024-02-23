from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from models import Transacao, Cliente
from schemas import TransacaoSchema
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
app = FastAPI()


@app.post('/clientes/{id}/transacoes')
async def get_transactions(id: int, body: TransacaoSchema):
    cliente = Cliente().find_by_id(id)
    if not cliente:
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
            None,
            status_code=status.HTTP_200_OK
        )

    return JSONResponse(
        {'message': transacao.error},
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

    transacoes = Transacao().query_by(
        'cliente_id',
        id,
        'cliente_id-index'
    ).attributes_to_get('valor,tipo,descricao,realizada_em').limit(10).order('realizada_em', False).fetch()

    response = {
        'saldo': {
            'total': int(cliente.saldo),
            'data_extrato': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'limite': int(cliente.limite),
        },
        'ultimas_transacoes': transacoes,
    }
    return JSONResponse(
        response,
        status_code=status.HTTP_200_OK
    )
