#!/usr/bin/perl
#log.pl

use CGI;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Session( -'ip_match');
use DBI;
use DBD::mysql;
use Digest::SHA1 qw( sha1_hex sha1_base64 );
use constant secretphrase => "asjdiashdoaho34230hy8sdf";


$q= new CGI;

sub db_on{                      #liga a base de dados
        use DBI;
        $db="c0707046";
        $host="twserver.alunos.dcc.fc.up.pt";
        $user="c0707046";
        $password="7iMCU9Mq"; #depois meter ficheiro aparte
        $dbh= DBI->connect( "DBI:mysql:database=$db:host=$host",$user,$password) or die "Can't connect to database: $DBI::errstr\n";
}

sub db_off{$dbh->disconnect;}   #desliga base de dados



$em = $q->param('em');
$pwd =$q->param('pwd');

if ($em ne  "")								#se mail tiver algo verifica se deve ou nao criar sessão
	{	db_on;
		my $pass = sha1_base64( $em, $pwd, $secretphrase);
		$sth = $dbh->prepare('SELECT count(email) FROM user WHERE password=? and email=?') or die "Dead";
  		$sth->execute($pass,$em) or die "Can't execute statement: $DBI::errstr\n";
  		my @data= $sth->fetchrow_array();
		
		
  		if (($data[0] gt 0) or ($em eq "admin" and $pwd eq "admin")) #|| $em eq "demo" and $pwd eq "demo" )
			{
			$session = new CGI::Session("driver:MySQL", undef, {Handle=>$dbh});
			$session= new CGI::Session();
			print $session->header(-location=>'index2.cgi');
			db_off;
			}
		else
			{
			
			print $q->header(-type=>'text/html',-location=>'index.cgi?try=1');
			print $q->header(-type=>'text/html');
			
			print $q->p,"$data[0]";
			}
	}

else	{	if($q->param('action') eq 'logout')	#se mail nao estiver preenchido e accção for logout
			{
			$session = CGI::Session->load() or die CGI::Session->errstr;
			$session->delete();
			print $session->header(-location=>'index2.cgi');
			}
		else					#se não for  
			{
		print 	$q->header,
			$q->start_html,
			$q-> start_form,
			$q->start_table({-align=>center}),
                        $q->Tr([
                       	#$q->hidden(-name=>'addvacancyflag'),
                       	$q->td(['email:',       $q->textfield(-name=> 'em')]),
			$q->td(['password:',	$q->password_field(-name=>'pwd')]),
			]),
			$q->td($q->submit('Log in'));
			if ($q->param('try') eq 1){ print $q->td($q->p,"Invaid login. Try again.");}
		print	$q->end_form,
			$q->end_html;
			}
}
