## SRinha de Backend, Segunda Edição: 2024/Q1 - Controle de Concorrência - Teste de container

### Stack:

- `Nginx` para o balanceamento de carga
- `Dynamodb` para o banco de dados
- `Python` e `FastApi` para implementacao da api
- [repositorio da api](https://github.com/kauelima21/teste-rinha)

Usei o dynamodb pois eh o banco que uso no trabalho e queria testar, nao vou subir isso para a rinha...

Apos subir os containers, para criar e popular as tabelas, rode o seguinte comando:
```sh
docker exec app1 python app/database_init.py
```
