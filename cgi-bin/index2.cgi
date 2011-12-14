#!/usr/bin/perl -wT

#use strict;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI;
use Digest::SHA1 qw( sha1_hex sha1_base64 );
use CGI::Session( -'ip_match');
#use CGI::Session;
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


sub viewusers{			#mostra utilizadores
	db_on;
	my $sth = $dbh->prepare('SELECT * FROM user') or die "Can't find table from database: $DBI::errstr\n";
	$sth->execute() or die "Can't execute statement: $DBI::errstr\n";

	print "<table border=1>\n";
	print 
"<tr><th>UserID</th><th>Name</th><th>Email</th><th>Address</th><th>City</th><th>Country</th><th>Description</th><th>Reputation</th></tr>\n"; 
	@data=$sth->fetchrow_array();
	while (my @data = $sth->fetchrow_array()){
        print "<tr>";
	print "<td>$data[0]</td><td>$data[1]</td><td>$data[2]</td><td>$data[3]</td><td>$data[4]</td><td>$data[5]</td><td>$data[6]</td><td>$data[7]</td>"; 
					
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

sub search{     print   $q->start_form,
                        $q->start_table({-align=>center}),
                        $q->Tr([
                        $q->hidden(-name=>'Search Results'),
                        $q->td(['Keyword:',         $q->textfield(-name=> 'searchf')]),
                                                $q->td(['Search:',
                        $q->radio_group(-name => 'types',-values=>['Reputation','Country','E-mail'],-default=>'Reputation')]),
                        $q->td($q->submit(-name=>'Submit')),
                        ]),

                        $q->end_form;

}

sub searchresults{ 	db_on;
			my $para=($q->param('searchf'));
			if ($q->param('types') eq "Reputation"){  
				my $sth = $dbh->prepare('SELECT * FROM user WHERE reputation=?') or die "Dead";
                 		$sth->execute($para);
                 		print "<table>";
				print "<tr>";
				        while (my @data = $sth->fetchrow_array()){
					       # if ($data[0] eq 1) {}
						#	else{   
								print "<tr>";
      print"<td>$data[0]</td><td>$data[1]</td><td>$data[2]</td><td>$data[3]</td><td>$data[4]</td><td>$data[5]</td><td>$data[6]</td><td>$data[7]</td>";

      								print   "</tr>\n";               
						}
#}
      			print "</tr>\n";
        		print "</table>\n";
			db_off;
			}
			  	elsif ($q->param('types') eq "Country"){
                                my $sth = $dbh->prepare('SELECT * FROM user WHERE country=?') or die "Dead";
                                $sth->execute($para);
                                ;
                                        while (my @data = $sth->fetchrow_array()){
 #                                               if ($data[0] eq 1) {}
                                                #        else{  
						 print "<tr>";
      
print"<td>$data[0]</td><td>$data[1]</td><td>$data[2]</td><td>$data[3]</td><td>$data[4]</td><td>$data[5]</td><td>$data[6]</td><td>$data[7]</td>";

                                                                print   "</tr>\n";
                                                
}
#}
                        print "</tr>\n";
                        print "</table>\n";
                        db_off;
                        }
			else{
			
                                my $sth = $dbh->prepare('SELECT * FROM user WHERE mail=?') or die "Dead";
                                $sth->execute('$para');
				
				#my $id= $data[0];
                               # my $sth = $dbh->prepare('SELECT * FROM vacancy WHERE idu_s=? OR idu_p=?') or die "Dead";
                               # $sth->execute($id,$id);

                                print "<table>\n";
				
                                        while (my @data = $sth->fetchrow_array()){
                            #                    if ($id ne 1) {}
                             #                           else{   
							print "<tr>";
      							#print @data;
print"<td>$data[0]</td><td>$data[1]</td><td>$data[2]</td><td>$data[3]</td><td>$data[4]</td><td>$data[5]</td><td>$data[6]</td><td>$data[7]</td>";

                                                                print   "</tr>\n";
                                                }
#}
                        print "</tr>\n";
                        print "</table>\n";
                        db_off;
                        }
			}

			
			

sub testvacancy    {	db_on;
                        #my $id = $session->param("uid");
                        $mail2=$q->param('email');
                        $invalid2=0;
                        @date1=split(/-/,($q->param('date1')));
                        @date2=split(/-/,($q->param('date2')));
                        
                        my $sth = $dbh->prepare('SELECT count(*) FROM user WHERE email=?') or die "Dead";
                        @errors=("The following errors were found, please correct:\n");
                        if ($mail2 eq "") {
                                        push(@errors, "-Blank email. Please insert a valid email.\n");
                                        $invalid2=1;}
                        else    {
                                   $sth->execute($mail2) or die "Can't execute statement: $DBI::errstr\n";
                                                                my @data= $sth->fetchrow_array();
                                                                if ($data[0] eq 0)
                                                                        {
                                                                        push (@errors,"$mail2 is not registered!\n");
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
                  #print $total;              
                                
                                
                                
                                }
                        db_off;
                        $invalid2=1;
                        }


#db_on;
#my $session = CGI::Session->load;
$session = CGI::Session->load();
$q = new CGI; #object CGI

sub menu1{
$id=$session->param("uid");
my $name = $session->param("em1");
print	$q->start_html(-title=>'Admin page',-style=>{-src=>'../css/style.css'}),
	$q->h1("Couch Surfing - $name"),
	$q->Tr([
	$q->start_form,
	$q->defaults('Home'),
	$q->submit(-name=>'View Users'),
	$q->submit(-name=>'View Vacancies'),
	$q->submit(-name=>'New Vacancy'),
	$q->submit(-name=>'Search'),
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
							case	"New Vacancy"		{ addvacancy }
							case	"Add Vacancy"		{ testvacancy }	
							case	"Search Results"	{ searchresults }
							case	"Search"		{ search }
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
        $session->delete;
        $session->flush;

      	#print "<br/><a href='index.cgi>Login</a>";
  }
  elsif($session->is_empty)
  {	
	#$session->delete;
	#$session->flush;   
print $q->header(-cache_control=>"no-cache, no-store, must-revalidate");
    print $q->h1("Couch Surfing");
	print $q->p,"You have not logged in";
	print $q->p,$q->a({-href=>'index.cgi'},"Login");
#	print "<br/><a href='index.cgi>Login</a>";
  }
  else{


	print $q->header('text/html', -expires => "+30m",-cache_control=>"no-cache, no-store, must-revalidate");
	#print "<h2>Welcome";
	print $q->a({-href=>'index.cgi?action=logout'},"Logout");
	menu1;
	print $q->end_html;
}    



