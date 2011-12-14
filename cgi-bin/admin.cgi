#!/usr/bin/perl -wT
#use strict;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI;

use CGI::Session;
use Switch;
use DBI;

push @INC, '.';
#require login;


my $q = CGI -> new; #object CGI
my $session = new CGI::Session("driver:File", undef, {Directory=>'/tmp'});

sub db_on{			#liga a base de dados
	use DBI;
	$db="c0707046";
	$host="twserver.alunos.dcc.fc.up.pt";
	$user="c0707046";
	$password="7iMCU9Mq"; #depois meter ficheiro aparte
	$dbh= DBI->connect( "DBI:mysql:database=$db:host=$host",$user,$password) or die "Can't connect to database: $DBI::errstr\n";
}

sub db_off{$dbh->disconnect;}	#desliga base de dados
sub login_form { # Objecto CGI passado como primeiro argumento 
print 	$q->header(-type => 'text/html'),
        $q->start_html('Login'),
        $q->start_form(-action => $scriptname), # Processado pelo próprio script 
        $q->p('Username:',
        $q->textfield(-name => 'user')),
        $q->p('Password:',
        $q->password_field(-name => 'pass', -default => '', -override => 1)),
        $q->p($q->submit(-value => 'Login')),
        $q->end_form(),
        $q->end_html(); }
        1;






sub adduser{		
			
                print   $q->start_form,
                        $q->start_table({-align=>center}),
                        $q->Tr([
                        $q->hidden(-name=>'adduserflag'),
                        $q->td(['Name:',        $q->textfield(-name=> 'name')]),
                        $q->td(['Email:',       $q->textfield(-name=> 'email')]),
                        $q->td(['Address:',     $q->textfield(-name=> 'address')]),
                        $q->td(['City:',        $q->textfield(-name=> 'city')]),
                        $q->td(['Country:',     $q->textfield(-name=> 'country')]),
                        $q->td(['Description:', $q->textfield(-name=> 'description')]),
                        $q->td(['Password(min. 8 char.):',        $q->password_field(             -name=>'password',
                                                                                -size=>35,
                                                                                -maxlength=>50)]),
                        $q->td(['Confirm the password:',
                                                $q->password_field(    -name=>'password_repeat',
                                                                       -size=>35,
                                                                       -maxlength=>50)]),

                        #$q->td(['Ranking:',scalar(
                        #                       $q->radio_group(-name => 'reputation',-values=>['1','2','3','4','5']))]),

                        $q->td($q->submit(-name=>'Submit')),
                        ]),
                        $q->end_form;

        }


sub testuser	{	db_on;
			$mailu = $q->param('email');
			$invalid=0;
			my $sth = $dbh->prepare('SELECT count(*) FROM user WHERE email=?') or die "Dead";
			@errors=("The following errors were found, please correct:\n");
                	if ($mailu eq "") {
					push(@errors, "-Blank email. Please insert a valid email.\n");
					$invalid=1;}
			else	{
					if ($q->param('email')=~/^(\w|\-|\_|\.)+\@((\w|\-|\_)+\.)+[a-zA-Z]{2,}$/)
                                       				{
     		                                        	push(@errors, "- $mailu is in valid format.\n");                        
								$sth->execute($mailu) or die "Can't execute statement: $DBI::errstr\n";
			        		                my @data= $sth->fetchrow_array();
			 		                        if ($data[0] gt 0)      
									{
                        						push (@errors,"$mailu is already registered!\n");
                                      					$invalid=1;
	     	             						}
               							}
                                        	
                      			else 		{
                                       			push (@errors,"-$mailu is in invalid form.\n");
							$invalid=1;	
                                       			}

			
				}
			
			if ($q->param('password') eq $q->param('password_repeat')) 
					{ 
					if (length($q->param('password')) <=8)
						{
						push(@errors,"-Password must be bigger than 8 characters.\n") ;
						$invalid=1;
						}
					}
			else 		{
					push(@errors,"-Passwords don't match.\n");
					$invalid=1;
					}


			if ($q->param('name') eq "")
					{
					push(@errors,"-Please insert a Name.\n");
					$invalid=1;
					}
                        if ($q->param('address') eq "")
                                        {
                                        push(@errors,"-Please insert a Address.\n");
                                        $invalid=1;
                                        }

                        if ($q->param('city') eq "")
                                        {
                                        push(@errors,"-Please insert a city.");
                                        $invalid=1;
                                        }

                        if ($q->param('country') eq "")
                                        {
                                        push(@errors,"-Please insert a country.");
                                        $invalid=1;
                                        }

			if ($invalid)
				{
				adduser;
				print	$q->start_form,
        	                	$q->start_table({-align=>center});
                	        	#$q->Tr([;
					foreach $msg (@errors){ print $q->p,"$msg";}
				 	#]),
	                        	print $q->end_form;

				}
			else 	{
			my $sth = $dbh->prepare('INSERT INTO user(name,email,address,city,country,description) values (?,?,?,?,?,?)') or die "Dead";
			
$sth->execute(($q->param('name')),($q->param('email')),($q->param('address')),($q->param('city')),($q->param('country')),($q->param('description'))) 
or 
die 
"Erro";			
			print $q->p,"The user $mailu is now registered!";
			
				}
			db_off;
			$invalid=1;
			}


sub resetDB{}

sub viewusers{			#mostra utilizadores
	db_on;
	my $sth = $dbh->prepare('SELECT * FROM user') or die "Can't find table from database: $DBI::errstr\n";
	$sth->execute() or die "Can't execute statement: $DBI::errstr\n";

	print "<table border=1>\n";
	print 
"<tr><th>UserID</th><th>Name</th><th>Email</th><th>Address</th><th>City</th><th>Country</th><th>Description</th><th>Reputation</th></tr>\n"; 
	while (my @data = $sth->fetchrow_array()){
        		print "<tr>";
			foreach $campo (@data){
        			print "<td>$campo</td>";} 
					
			print	"</tr>\n";		 }
	print "</tr>\n"; 
	print "</table>\n"; 		
	#])
			#);
	db_off;
}

sub viewvacancies{                  #mostra utilizadores
        db_on;
        my $sth = $dbh->prepare('SELECT * FROM vacancy') or die "Can't find table from database: $DBI::errstr\n";
        $sth->execute() or die "Can't execute statement: $DBI::errstr\n";
        while (my @data = $sth->fetchrow_array()){
                print   $q->hr,
                        $q->p, "@data \n"; }
        ;
        db_off;
}

sub addvacancy{
                print   $q->start_form,
                        $q->start_table({-align=>center}),
                        $q->Tr([
                        $q->hidden(-name=>'addvacancyflag'),
                        $q->td(['Name:',        $q->textfield(-name=> 'name')]),
                        $q->td(['Email:',       $q->textfield(-name=> 'email')]),
                        $q->td(['Address:',     $q->textfield(-name=> 'address')]),
                        $q->td(['City:',        $q->textfield(-name=> 'city')]),
                        $q->td(['Country:',     $q->textfield(-name=> 'country')]),
                        $q->td(['Description:', $q->textfield(-name=> 'description')]),
                        $q->td(['Password(min.8 char.):',    $q->password_field(             -name=>'password',
                                                                                -size=>35,
                                                                                -maxlength=>50)]),
                        $q->td(['Confirm the password:',
                                                $q->password_field(    -name=>'password_repeat',
                                                                       -size=>35,
                                                                       -maxlength=>50)]),

                        $q->td(['Ranking:',scalar(
                                                $q->radio_group(-name => 'reputation',-values=>['1','2','3','4','5']))]),

                        $q->td($q->submit(-name=>'Submit')),
                        ]),
                        $q->end_form;

}
sub debugvar {                        foreach $param (keys %$all_params)
                                {
                                print "INVALID = $invalid";
                                print "$param: " . $all_params->{$param} . "<BR>";      #teste de parametros
                                print $q->h2("$param");
}}





sub menu1{
print 	$q->header('text/html', -expires => "+30m"),
	$q->start_html(-title=>'Admin page'),
	$q->h1("Administrator Page"),
	$q->Tr([
	$q->start_form,
	$q->defaults('Home'),
	$q->submit(-name=>'View Users'),
	$q->submit(-name=>'New User'),
	$q->submit(-name=>'View Vacancies'),
	$q->submit(-name=>'New Vacancy'),
	$q->submit(-name=>'Restart DB'),
	$q->end_form,
	$q->hr,
	]);




#foreach $key (keys %ENV) {
#	print FH "$key - $ENV{$key}\n";
#}

my $all_params = $q->Vars;

if ($invalid == 1)	{$invalid=0;
			}

else			{
			foreach $param (keys %$all_params)	 
				{
        			print $q->h2("$param");
				switch ($param){	
							case	"View Users"	   	{ viewusers }
							case	"View Vacancies"	{ viewvacancies }
							case	"New User"		{ adduser }
							case	"New Vacancy"		{ addvacancy }
							case	"Restart DB"		{ resetDB}
							case	"adduserflag"		{ testuser }
							else     		   	{ print "lol2\n" }
	       					}
				last; 
				}
			}	
}
menu1;
print $q->end_html;

#if ($q->param()) {
#	;
#    



