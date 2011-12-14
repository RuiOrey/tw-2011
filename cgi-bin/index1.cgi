#!/usr/bin/perl -wT

#use strict;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI;
use Digest::SHA1 qw( sha1_hex sha1_base64 );
#use CGI::Session;
use CGI::Session( -'ip_match');

use Switch;
use DBI;
use DBD::mysql;
push @INC, '.';
#require login;


sub db_on{			#liga a base de dados
	use DBI;
	$db="c0707046";
	$host="twserver.alunos.dcc.fc.up.pt";
	$user="c0707046";
	$password="7iMCU9Mq"; #depois meter ficheiro aparte
	$dbh= DBI->connect( "DBI:mysql:database=$db:host=$host",$user,$password) or die "Can't connect to database: $DBI::errstr\n";
}

sub db_off{$dbh->disconnect;}	#desliga base de dados

sub adduser{		
			
                print   $q->start_form,
                        $q->start_table({-align=>center}),
                        $q->Tr([
                        $q->hidden(-name=>'Add User'),
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
     		                                        	#push(@errors, "- $mailu is in valid format.\n");                        
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
			my $secretphrase => "asjdiashdoaho34230hy8sdf";
		my $pass = sha1_base64(($q->param('email')), $q->param('password') , $secretphrase);
		my $sth = $dbh->prepare('INSERT INTO user(name,email,address,city,country,description,password) values (?,?,?,?,?,?,?)') or die "Dead";
			
$sth->execute(($q->param('name')),($q->param('email')),($q->param('address')),($q->param('city')),($q->param('country')),($q->param('description')),$pass ) 
or 
die 
"Erro";			
			print $q->p,"The user $mailu is now registered!";
			
				}
			db_off;
			$invalid=1;
			}

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
    print "<table border=1>\n";
        print "<tr><th>VacancyID</th><th>User1ID</th><th>User2ID</th><th>Type of vacancy</th><th>Start 
Date</th><th>EndDate</th>><th>Reputation</th><th>Description</th></tr>\n";

	while (my @data = $sth->fetchrow_array()){
                     print "<tr>";
                        foreach $campo (@data){
                                print "<td>$campo</td>";}

                        print   "</tr>\n";               }
        print "</tr>\n";
        print "</table>\n";
 
        db_off;
}

sub addvacancy{ 
		my $uid= $id;

                print   $q->start_form,
                        $q->start_table({-align=>center}),
                        $q->Tr([
                        $q->hidden(-name=>'Add Vacancy'),
                        $q->td(['Reviewer user email:',         $q->textfield(-name=> 'email1')]),
			$q->td(['Reviewed user email:',       	$q->textfield(-name=> 'email')]),
                        $q->td(['Date Start(yyyy-mm-dd):',      $q->textfield(-name=> 'date1',-size=>10)]),
                        $q->td(['Date End(yyyy-mm-dd):',      $q->textfield(-name=> 'date2',-size=>10)]),
						$q->td(['Kind of vacancy:',
                        $q->radio_group(-name => 'host',-values=>['I hosted','I was hosted'],-default=>'I hosted')]),
						$q->td(['Ranking:',scalar($q->radio_group(-name => 'reputation',-values=>['1','2','3','4','5'],-default=>'3'))]),
                        $q->td(['Description(optional):', $q->textfield(-name=> 'description')]),
						$q->td($q->submit(-name=>'Submit')),
                        ]),

                        $q->end_form;

}

sub testvacancy    {	db_on;
                        #my $id = $session->param("uid");
                        my $mail2=$q->param('email');
                        my $mail1=$q->param('email1');
			$invalid2=0;
                        my @date1=split(/-/,($q->param('date1')));
                        my @date2=split(/-/,($q->param('date2')));
                        my @errors=("The following errors were found, please correct:\n");
                      	my $sth = $dbh->prepare('SELECT count(*) FROM user WHERE email=?') or die "Dead";
                        if ($mail1 eq "") {
                                        push(@errors, "-Blank reviewer user email. Please insert a valid email.\n");
                                        $invalid2=1;}
                        else    {
                                   $sth->execute($mail1) or die "Can't execute statement: $DBI::errstr\n";
                                                                my @data= $sth->fetchrow_array();
                                                                if ($data[0] eq 0)
                                                                        {
                                                                        push (@errors,"$mailu is not registered!\n");
                                                                        $invalid2=1;
                                                                        }
                                                                }


			if ($mail2 eq "") {
                                        push(@errors, "-Blank reviewed user email. Please insert a valid email.\n");
                                        $invalid2=1;}
                        else    {
                                   $sth->execute($mail2) or die "Can't execute statement: $DBI::errstr\n";
                                                                my @data= $sth->fetchrow_array();
                                                                if ($data[0] eq 0)
                                                                        {
                                                                        push (@errors,"$mailu is not registered!\n");
                                                                        $invalid2=1;
                                                                        }
                                                                }

                                

             if ($date1[2] < 1 || $date1[2]> 31 || $date1[1] < 1 || $date1[1]>12 || $date1[0] < 1900 || $date1[0] >2900)
                            {   push(@errors,"-Incorrect start date.\n") ;
                                                $invalid2=1;
                                                }
               if ($date2[2] < 1 || $date2[2]> 31 || $date2[1] < 1 || $date2[1]>12 || $date2[0] < 1900 || $date2[0] >2900)
                            {   push(@errors,"-Incorrect end date.\n") ;
                                                $invalid2=1;
                                                }
               else {if (int($date2[0]) > int($date1[0])) {}
                     else {if ($date2[0] == $date1[0]) 
                        	{if ($date2[1] > $date1[1] ) {}
                           else		{if ($date2[1] == $date1[1]) 
                                		{if   ($date2[2] >= $date1[2]) {}
                            else {push(@errors,"-Start date can't be greater than end date.\n") ;
                                             $invalid2=1;}
						}
					}
				}
			  }
			}
                                       
  
                        if ($invalid2)
                                {
                                addvacancy;
                                print   $q->start_form,
                                        $q->start_table({-align=>center});
                                        #$q->Tr([;
                                        foreach $msg (@errors){ print $q->p,"$msg";}
                                        #]),
                                        print $q->end_form;

                                }
                        else    {
                
                 my $sth = $dbh->prepare('SELECT id_user FROM user WHERE email=?') or die "Dead";
                 $sth->execute($mail2);
                 my @data= $sth->fetchrow_array();
                 $ids=$data[0];
                 my $sth = $dbh->prepare('INSERT INTO vacancy(idu_p,idu_s,type_vacancy,date_start,date_end,description,reputation) values (?,?,?,?,?,?,?)') or die "Dead";
                 if ($q->param('host') eq "I hosted")   { $host="host";}
                 else                                   { $host="hosted";}

$sth->execute(($id),($ids),($host),($q->param('date1')),($q->param('date2')),($q->param('description')),($q->param('reputation')) ) or die "Erro  $DBI::errstr\n";
                        print $q->p,"The user review is now registered!";
                 my $sth = $dbh->prepare('SELECT reputation FROM vacancy WHERE idu_s=?') or die "Dead";
                 $sth->execute($ids);
                 $total=0;
                 $sum=0;
                 while (my @data= $sth->fetchrow_array()){

             		    foreach $pont (@data)

                        	                    {$total=$total + $pont;
                                	            $sum++;}
							}
                 $total=int(($total)/($sum));
                 my $sth = $dbh->prepare('UPDATE user SET reputation=? WHERE id_user=?') or die "Dead";
                 
                 $sth->execute($total,$ids);               
                 # print $total;              
                                
                                
                                
                                }
                        db_off;
                        $invalid2=1;
                        }

sub dbreseted {
db_on;

push @sql,'TRUNCATE TABLE vacancy';
push @sql,'TRUNCATE TABLE user';
push @sql,'TRUNCATE TABLE sessions';
#push @sql,'CREATE TABLE user(id_user MEDIUMINT NOT NULL AUTO_INCREMENT,name VARCHAR(70) NOT NULL,email VARCHAR(70) NOT NULL,address VARCHAR(200) NOT 
#NULL,city VARCHAR(70) NOT NULL,country VARCHAR(70) NOT NULL,description TEXT,reputation INT(1),password CHAR(27) NOT NULL,UNIQUE(email),PRIMARY 
#KEY(id_user))ENGINE INNODB';
#push @sql,'CREATE TABLE vacancy(id_stay MEDIUMINT NOT NULL AUTO_INCREMENT,idu_p	MEDIUMINT NOT NULL,idu_s MEDIUMINT,type_vacancy 
#ENUM(\'host\',\'hosted\'),date_start DATE NOT NULL,date_end DATE NOT NULL,reputation INT(1),description TEXT,PRIMARY KEY(id_stay),CONSTRAINT fk_idp 
#FOREIGN KEY(idu_p) REFERENCES user(id_user),FOREIGN KEY(idu_s) REFERENCES user(id_user))ENGINE INNODB';
#push @sql,'CREATE TABLE sessions (id CHAR(32) NOT NULL UNIQUE,a_session TEXT NOT NULL)';

db_on;
foreach $st (@sql) { 
				
				$sth = $dbh->prepare($st) or die "Cannot prepare: " . $dbh->errstr();
				$sth->execute() or die "Cannot execute: " . $sth->errstr();
				}
my $secretphrase => "asjdiashdoaho34230hy8sdf";
my $pass = sha1_base64("admin", "admin" , $secretphrase);
my $sth = $dbh->prepare('INSERT INTO user(id_user,name,email,address,city,country,description,password) values (0,\'admin\',\'admin\',\'admin\',\'admin\',\'admin\',\'admin\',?)' );
$sth->execute($pass);

#$session->delete;

db_off; 
print "Success! Database Reseted.";
#my $session = CGI::Session->load();
#$session->delete;
#my $session->flush;

}

sub resetDB {  
	print		$q->h2("Are you sure you want to restart all database?"),
        	  	$q->Tr([
        		$q->start_form,
        		$q->defaults('Cancel'),
        		$q->submit(-name=>'Restart the DB'),
			$q->end_form,
			]);
			}

sub debugvar {                        foreach $param (keys %$all_params)
                                {
                                print "INVALID = $invalid";
                                print "$param: " . $all_params->{$param} . "<BR>";      #teste de parametros
                                print $q->h2("$param");
}}

db_on;
my $session = CGI::Session->load();
$q = CGI -> new; #object CGI

sub menu1{
$id=$session->param("uid");
my $name = $session->param("em1");
print	$q->start_html(-title=>'Admin page',-style=>{-src=>'../css/style.css'}),

	$q->h1("Couch Surfing - $name"),
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





my $all_params = $q->Vars;

if ($invalid == 1 or $invalid2 == 1)	
		{	 $invalid=0;
			 $invalid2=0;
		}

else			{
			foreach $param (keys %$all_params)	 
				{
        			print $q->h2("$param");
				switch ($param){	
							case	"View Users"	   	{ viewusers }
							case	"View Vacancies"	{ viewvacancies }
							case	"New User"			{ adduser }
							case	"New Vacancy"		{ addvacancy }
							case	"Restart DB"		{ resetDB}
							case	"Add User"			{ testuser }
							case	"Add Vacancy"		{ testvacancy }	
							case 	"Restart the DB"  	{ dbreseted } 
							else     		   	{ print "error\n" }
	       					}
				last; 
				}
			}	
} 
 
  if($session->is_expired)
  {
	print $q->header(-cache_control=>"no-cache, no-store, must-revalidate");
    print $q->h1("Couch Surfing");
	print "Your has session expired. Please login again.";
      	print "<br/><a href='index.cgi>Login</a>";
  }
  elsif($session->is_empty)
  {
    print $q->header(-cache_control=>"no-cache, no-store, must-revalidate");
    print $q->h1("Couch Surfing");
	print $q->p,"You have not logged in";
	print $q->p,$q->a({-href=>'index.cgi'},"Login");
	#print "<br/><a href='index.cgi>Login</a>";
	#$session->delete;
	#$session->flush;  
}
  else{


	print $q->header('text/html', -expires => "+30m",-cache_control=>"no-cache, no-store, must-revalidate");
	#print "<h2>Welcome";
	print $q->a({-href=>'index.cgi?action=logout1'},"Logout");
	menu1;
	print $q->end_html;
}    



