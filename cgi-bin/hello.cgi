#!/usr/bin/perl -wT

print << "END_OF_HTML";
Content-type: text/html

<html>
<head><title>Hello, World!</title></head>
<body>
<h1>About this server</h1>
<ul>
    <li>Server name: $ENV{SERVER_NAME}</li>
    <li>Running on port: $ENV{SERVER_PORT}</li>
    <li>Server software: $ENV{SERVER_SOFTWARE}</li>
    <li>Server protocol: $ENV{SERVER_PROTOCOL}</li>
    <li>CGI revision: $ENV{GATEWAY_INTERFACE}</li>
</ul>
</body>
</html>
END_OF_HTML
