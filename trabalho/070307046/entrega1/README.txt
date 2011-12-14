070307046 - Rui Luis Sousa de Albuquerque d'Orey 
TW 2011/2012 - FCUP
Entrega intermedia

O trabalho até agora tem as 5 funçoes basicas disponiveis :


reinicializar
registar
listar utilizadores
adicionar estadia
listar estadias

A autenticação usa a biblioteca Session.
A password é guardada encriptada na base de dados com sha1.
A manutençao de sessão é na base de dados.

Em anexo estão 3 cgis distintos e com codigo repetido porque nao tive tempo de o modelar:
-index.cgi: cgi para utilizadores por autenticar onde é possivel "loggar",registar, listar utilizadores e estadias; 
-index1.cgi: cgi acessivel só para administrador, onde todas as funções estão acessiveis;
-index2.cgi: cgi acessivel a utilizadores registados "normais", onde todas as funções estão disponiveis excepto "registar".

A funcionalidade "adicionar estadia" é mais personalizavel no modo administrador pois permite criar uma estadia em nome
de outro utilizador(sendo um utilizador "normal" só é permitido criar estadias sendo ele o utilizador principal).

No CGI de boas vindas a tabela de ver utilizadores inibe o email. 
Tentei implementar uma pesquisa no cgi de user "normal" mas não funciona.


Login de administrador 	: admin
Pass			: admin

O login normal é feito com o email que é a chave primaria da base de dados, após registado.