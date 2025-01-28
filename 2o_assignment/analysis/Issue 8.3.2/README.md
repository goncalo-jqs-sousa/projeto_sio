# Issue 8.3.2 - Users have a method to remove or export their data on demand

A possibilidade de apagar a conta deve estar disponível a todos os utilizadores, pois existem vários motivos de segurança que levem a querer apagar os dados.

No ficheiro init.py foi criado uma route /delete que acede a database e apaga os dados da conta.

Com a informação de que dados irão desaparecer o utilizador pode decidir se pretende eliminar a sua conta com exceção das encomendas.

## Code

![Route](route.png)
