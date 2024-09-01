# Hackathon SantoDigital - 08/2024 Desafio II

Neste desafio, você deverá desenvolver uma API REST usando o framework de sua escolha (preferencialmente FastAPI) para interagir com o banco de dados AdventureWorks.
Sua API deve ser capaz de executar as seguintes tarefas, além de implementar funcionalidades avançadas para garantir segurança, eficiência e manutenibilidade.

## Funcionalidades Básicas

Create: Rota POST /products/
Read: Rota GET /products/
Update: Rota PUT /products/{id}
Delete: Rota DELETE /products/{id}

Validação de Dados
Paginação, Filtragem e Ordenação
Manipulação de Transações
Testes Unitários e de Integração
Criação de Logs
Documentação Automática Swagger

### Tarefa 2:

Testes Unitários: Criar testes unitários para cada rota da API (POST /products/, GET /products/, GET /products/{id}, PUT /products/{id}, DELETE /products/{id}).
Verificar se cada rota está funcionando corretamente com entradas válidas. Verificar se cada rota lida

### Postgres

No momento, apenas as tabelas e os dados são totalmente implementados, mas devem ser convertidos com precisão em tipos de dados postgres (incluindo geografia).
Algumas visualizações (especificamente, as que usam XML e 'CROSS APPLY') foram omitidas.

No functions, custom types, or stored procedures are included.

| Tag                         | Description                                                                              |
| --------------------------- | ---------------------------------------------------------------------------------------- |
| `postgres` or `postgres-16` | Esta imagem adapta a versão "light" do banco de dados AdventureWorks para Postgres 16.   |
| `postgres-13`               | Esta imagem adapta a versão "light" do banco de dados AdventureWorks para o Postgres 13. |

> [!TIP]
> Substitua `My_password1` por sua própria senha segura. Observe que a senha _deve_ passar pelos requisitos mínimos de complexidade
> ou você não conseguirá se conectar!

### Postgres

Essa imagem do docker usa as mesmas variáveis de ambiente definidas no [Postgres docker image](https://hub.docker.com/_/postgres).

```
docker run -p 5432:5432 -e 'POSTGRES_PASSWORD=My_password1' -d chriseaton/adventureworks:postgres

```

### Fastapi

```
fastapi dev app/main.py

```

### pytest

```
pytest

```
