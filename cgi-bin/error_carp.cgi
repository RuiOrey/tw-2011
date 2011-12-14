#!/usr/bin/perl -wT

use CGI::Carp qw(fatalsToBrowser);

print "Content-type: text/html\n\n";
print "Hello World<br>";

# agora vem um erro (note que falt o "t" em "prin")
prin "Instrucao com erro";

# agora vem instrucao correcta
print "Instrucao correcta";

