# Proposta

O Boticário tem várias soluções para ajudar seus revendedores(as) a gerir suas finanças e alavancar suas vendas. Também existem iniciativas para impulsionar as operações de vendas como metas gameficadas e desconto em grandes quantidades de compras.

Agora queremos criar mais uma solução, e é aí que você entra com seu talento ;) A oportunidade proposta é criar um sistema de Cashback, onde o valor será disponibilizado como crédito para a próxima compra da revendedora no Boticário;

Cashback quer dizer “dinheiro de volta”, e funciona de forma simples: o revendedor faz uma compra e seu benefício vem com a devolução de parte do dinheiro gasto no mês seguinte.

Sendo assim o Boticário quer disponibilizar um sistema para seus revendedores(as) cadastrarem suas compras e acompanhar o retorno de cashback de cada um.

# Tecnologias utilizadas
Foi utilizado o framework Flask para a criação do sistema, utilizando banco local sqlite3, porém pode ser trocado por qualquer banco da preferência do usuário desde que seja SQL ou similar (SQL, PostgreSQL, Oracle, MariaDB, etc).

Para os testes foi utilizada a biblioteca pytest, com o total de 42 testes unitários e integração.

Para o sistema de login é utilizado JWT de forma simples. A chave encontra-se na pasta \"environments\".

O sistema possui recuperação de senha. Caso queira ativá-lo, deve-se inserir os dados corretos no \"environment\". Afim de teste foi utilizado o SES da AWS com emails reais dentro e fora da sandbox.

# O sistema contempla
- Perfilamento simples
- Login
- Recuperação de senha
- CRUD de usuário
- CRUD de compras

# O sistema não contempla
- Transações pelo administrador
- Visualiação de dados para múltiplas métricas

# Fluxo de Informação
## Admin

O admin é responsável por:
- cadastrar usuários
- visualizar usuários
- editar usuários
- excluir usuários
- cadastrar novas compras
- visualizar usuários
- editar compras
- excluir compras
- visualizar cashback de qualquer revendedor

## Revendedor
O revendedor é responsável por:
- cadastrar compras APENAS para ele mesmo
- visualizar as próprias compras
- visualizar o próprio cashback mensal


# Inicialização do sistema
Para inicializar o sistema, é necessário:
- Python 3.7 ou superior
- Banco SQL ou similar (caso queira usar sqlite3, apenas não altere o environment)

## Instalação
Como recomendação, sugiro a criação de uma virtual env para não sujar o SO e a pasta de instalação padrão do Python.

Para instalar as dependências, use:
> pip install -r requirements.txt

[Run](run.jpg)

Lembre-se de atualizar o environment com as credenciais de sua preferência


## Run
Para rodar o sistema, use:
> flask run

ou caso queira:
> python application.py

Após rodar o sistema, faça uma requisição para qualquer URL, isso consolida a database.
Ressalto que para o primeiro caso, as tabelas serão criadas automaticamente junto com as seeds de banco para inicializar o projeto.


# Tests
Foram feitos no total de 42 testes unitários e de integração para validar as ações do sistema, com cobertura de 83%.

[Tests](tests.jpg)
[Coverage](cov.jpg)

Para rodar os testes, use:
> pytest tests\\models tests\\resources tests\\helpers --disable-pytest-warnings -v
