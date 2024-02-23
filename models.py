from dynolayer import DynoLayer


class Transacao(DynoLayer):
    def __init__(self):
        super().__init__(
            'transacoes',
            ['valor', 'tipo', 'descricao', 'cliente_id', 'realizada_em'],
            'id',
            False
        )


class Cliente(DynoLayer):
    def __init__(self):
        super().__init__(
            'clientes',
            ['limite', 'saldo'],
            'id',
            False
        )
