070307046 - Rui Luis Sousa de Albuquerque d'Orey 
TW 2011/2012 - FCUP
Entrega intermedia

O trabalho at� agora tem as 5 fun�oes basicas disponiveis :


reinicializar
registar
listar utilizadores
adicionar estadia
listar estadias

A autentica��o usa a biblioteca Session.
A password � guardada encriptada na base de dados com sha1.
A manuten�ao de sess�o � na base de dados.

Em anexo est�o 3 cgis distintos e com codigo repetido porque nao tive tempo de o modelar:
-index.cgi: cgi para utilizadores por autenticar onde � possivel "loggar",registar, listar utilizadores e estadias; 
-index1.cgi: cgi acessivel s� para administrador, onde todas as fun��es est�o acessiveis;
-index2.cgi: cgi acessivel a utilizadores registados "normais", onde todas as fun��es est�o disponiveis excepto "registar".

A funcionalidade "adicionar estadia" � mais personalizavel no modo administrador pois permite criar uma estadia em nome
de outro utilizador(sendo um utilizador "normal" s� � permitido criar estadias sendo ele o utilizador principal).

No CGI de boas vindas a tabela de ver utilizadores inibe o email. 
Tentei implementar uma pesquisa no cgi de user "normal" mas n�o funciona.


Login de administrador 	: admin
Pass			: admin

O login normal � feito com o email que � a chave primaria da base de dados, ap�s registado.