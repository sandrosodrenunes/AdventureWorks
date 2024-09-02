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

| Tag                         | Description                                                                              |
| --------------------------- | ---------------------------------------------------------------------------------------- |
| `postgres` or `postgres-16` | Esta imagem adapta a versão "light" do banco de dados AdventureWorks para Postgres 16.   |
| `postgres-13`               | Esta imagem adapta a versão "light" do banco de dados AdventureWorks para o Postgres 13. |

> [!TIP]
> Substitua `My_password1` por sua própria senha segura. Observe que a senha _deve_ passar pelos requisitos mínimos de complexidade
> ou você não conseguirá se conectar!

### Postgres

Essa imagem do docker usa as mesmas variáveis de ambiente definidas no [Postgres docker image](https://hub.docker.com/_/postgres).

### Comando para rodar o docker, postgres e a base de dados do AdventureWorks

```
docker run -p 5432:5432 -e 'POSTGRES_PASSWORD=My_password1' -d chriseaton/adventureworks:postgres

```

### Fastapi

### Comando para rodar a aplicação

```
fastapi dev app/main.py

```

### Pytest

### Comando para rodar a bateria de teste.

```
pytest

```

![teste](https://github.com/user-attachments/assets/dfcdafe4-da99-4655-9710-52d9f69e57ff)

Teste 100% em memória!

### Rota para a tarefa 3

```
uvicorn main:app --reload

```

### Tarefa 1:

Create: Rota POST /products/
Read: Rota GET /products/
Update: Rota PUT /products/{id}
Delete: Rota DELETE /products/{id}

![01](https://github.com/user-attachments/assets/b4c33416-ffb8-4dcb-bb5f-02c55b5a4e37)

### Tarefa 2:

Paginação, Filtragem e Ordenação: Adicionar paginação nas rotas de listagem (GET /products/) para retornar um número limitado de produtos por página. Adicionar filtros para permitir busca por atributos específicos (ex: cor, preço) na rota de listagem. Implementar ordenação (ex: ordenar por preço, nome) na rota de listagem.

![02](https://github.com/user-attachments/assets/248af641-b829-4859-9c51-834f27bdc6c4)

![03](https://github.com/user-attachments/assets/33c32a6d-3e5b-454a-8372-e9f037f30952)

### Tarefa 3:

Rotas de Perguntas de Negócio:
Rota 1: GET /sales/top-products/category/{category}
Retorna os 10 produtos mais vendidos (em quantidade) na categoria fornecida.

Rota 2: GET /sales/best-customer
Retorna o cliente com o maior número de pedidos realizados.

Rota 3: GET /sales/busiest-month
Retorna o mês com mais vendas (em valor total).

Rota 4: GET /sales/top-sellers
Retorna os vendedores que tiveram vendas com valor acima da média no último ano fiscal

![categories](https://github.com/user-attachments/assets/03565830-1004-4ee6-9666-a7a0d821f61d)
