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
	print $q->start_form;
	print $q->submit(-name=>'Highest Rated',-id=>"login_form2");
	print $q->end_form;
	
	if ($q->param('Highest Rated'))
	{
	$sth = $dbh->prepare('SELECT * FROM user order by reputation DESC') or die "Can't find table from database: $DBI::errstr\n";
	}
	else{
	$sth = $dbh->prepare('SELECT * FROM user') or die "Can't find table from database: $DBI::errstr\n";}
	$sth->execute() or die "Can't execute statement: $DBI::errstr\n";

	print "<table border=1>\n";
	print 
"<tr><th>Name</th><th>Email</th><th>Address</th><th>City</th><th>Country</th><th>Description</th><th>Reputation</th></tr>\n"; 
	
	while (my @data = $sth->fetchrow_array()){
        if ($data[1] ne "admin"){
        print "<tr>";
	print "<td>$data[1]</td><td>$data[2]</td><td>$data[3]</td><td>$data[4]</td><td>$data[5]</td><td>$data[6]</td><td>$data[7]</td>"; 
					
	print	"</tr>\n";		 
	}}
	
	print "</tr>\n"; 
	print "</table>\n"; 		
	#])
			#);
	db_off;
}

sub usereditval{		#verificações edição de dados
		
db_on;
                        my $mailu = $session->param('em1');
                        $invalid=0;
                        
                        my $secretphrase => "asjdiashdoaho34230hy8sdf";
                my $passold = sha1_base64($mailu,($q->param('passwordold')),$secretphroase);
                        $sth = $dbh->prepare('SELECT password FROM user WHERE email=?') or die "Dead";
                                                       
                        @errors=("The following errors were found, please correct:\n");
                        if ($mailu eq "") {
                                        push(@errors, "-Blank email. Please insert a valid email.\n");
                                        $invalid=1;}
                        else    {	$sth->execute($mailu);
                        		@data=$sth->fetchrow_array();
                                       
                                                                if ("$data[0]" ne "$passold")
                                                                        {
                                                                        push (@errors,"$mailu has another password!\n");
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
                        else            {
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
                                print   $q->start_form,
                                        $q->start_table({-align=>center});
                                        #$q->Tr([;
                                        foreach $msg (@errors){ print $q->p,"$msg";}
                                        #]),
                                        print $q->end_form;

                                }
                        else    {
                        
                my $pass = sha1_base64(($mailu), $q->param('password') , $secretphrase);
                my $sth = $dbh->prepare('UPDATE user SET name=?,address=?,city=?,country=?,description=?,password=? WHERE email=?') or die 
"Dead";

$sth->execute(($q->param('name')),($q->param('address')),($q->param('city')),($q->param('country')),($q->param('description')),$pass,$mailu) or
die
"Erro  $DBI::errstr\n";
                        print $q->p,"The user $mailu is now updated!";

                                }
                        db_off;
                        $invalid=1;
                        


}

sub useredit{				#editar utilizador

                print   $q->start_form,
                        $q->start_table({-align=>center}),
                        $q->Tr([
                        $q->hidden(-name=>'Change User'),
                        $q->td(['Name:',        $q->textfield(-name=> 'name')]),
                        $q->td(['Address:',     $q->textfield(-name=> 'address')]),
                        $q->td(['City:',        $q->textfield(-name=> 'city')]),
                        $q->td(['Country:',     $q->textfield(-name=> 'country')]),
                        $q->td(['Description:', $q->textfield(-name=> 'description',-size=>100)]),
                         $q->td(['Retype your old password:',        $q->password_field(             -name=>'passwordold',
                                                                                -size=>15,
                                                                                -maxlength=>15)]),
                        $q->td(['Nem Password(min. 8 char.):',        $q->password_field(             -name=>'password',
                                                                                -size=>15,
                                                                                -maxlength=>15)]),
                        $q->td(['Confirm new password:',
                                                $q->password_field(    -name=>'password_repeat',
                                                                       -size=>35,
                                                                       -maxlength=>50)]),

                        #$q->td(['Ranking:',scalar(
                        #                       $q->radio_group(-name => 'reputation',-values=>['1','2','3','4','5']))]),

                        $q->td($q->submit(-name=>'Submit')),
                        ]),
                        $q->end_form;

        }


sub testeditvac{		#validação de ediçao de estadia e conclusão 
	my $vac_id=$q->param("Submit Vacancy");
	 $sth = $dbh->prepare('SELECT idu_s FROM vacancy WHERE id_stay=?') or die "Cant find table from database: $DBI::errstr\n";
        
        $sth->execute($vac_id) or die "Cant execute statement: $DBI::errstr\n";
        my @data=$sth->fetchrow_array();
        $idantigo=$data[0];
        
        my $id = $session->param("uid");
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
                                                                if (($data[0] eq 0) || ($mail2 eq "admin"))
                                                                        {
                                                                        push (@errors,"-$mail2 is not registered!\n");
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
               else {	$d1=$q->param('date1');
               		$d2=$q->param('date1');
               		if ("$d2" ge "$d1") {}
                    
                            else {push(@errors,"-Start date can't be greater than end date.\n") ;
                                             $invalid2=1;}
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
                 my $sth = $dbh->prepare('UPDATE vacancy SET idu_p=?,idu_s=?,type_vacancy=?,date_start=?,date_end=?,description=?,reputation=? WHERE id_stay=?')  or die "Dead";
                 if ($q->param('host') eq "I hosted")   { $host="host";}
                 else                                   { $host="hosted";}
			
			
			if (!($id == $ids)){
$sth->execute(($id),($ids),($host),($q->param('date1')),($q->param('date2')),($q->param('description')),($q->param('reputation')),$vac_id ) or die "Erro  $DBI::errstr\n";
                       # print $q->p,"The user review is now registered!";
                 
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
                  
                 $sth = $dbh->prepare('UPDATE user SET reputation=? WHERE user.id_user=?') or die "Dead";
                 
                 $sth->execute($total,$ids);  
                 my $sth = $dbh->prepare('SELECT reputation FROM vacancy WHERE idu_s=?') or die "Dead";
                 $sth->execute($idantigo);
                 $total=0;
                 $sum=0;
                 while (my @data= $sth->fetchrow_array()){

             		    foreach $pont (@data)

                        	                    {$total=$total + $pont;
                                	            $sum++;}
							}
							
			
                 $total=int(($total)/($sum));
                  
                 $sth = $dbh->prepare('UPDATE user SET reputation=? WHERE user.id_user=?') or die "Dead";
                 
                 $sth->execute($total,$idantigo);  
                 
                              
                  print $q->p,"The user review is now changed!";
                  #print $total;              
                                
                                
                                }
                         else  {      
                         		addvacancy;
                                print   $q->start_form,
                                        $q->start_table({-align=>center});
                                        #$q->Tr([;
                                        print $q->p,"You cannot review yourself!";
                                        #]),
                                        print $q->end_form;
 }
 	}							
 
                         db_off;
                        $invalid2=1;
                        }
        
        





sub editvac{
	db_on;
        my $id = $session->param("uid");
        my $vacid=$q->param("Vacancy Editing");
        print $vacid;
        $sth = $dbh->prepare('SELECT count(*) FROM vacancy WHERE idu_p=? and id_stay=?') or die "Cant find table from database: $DBI::errstr\n";
        
        $sth->execute($id,$vacid) or die "Cant execute statement: $DBI::errstr\n";
	my @data=$sth->fetchrow_array();
	if (($data[0] eq 0) || ($data[2] eq "admin")){
	print ("That vacancy review wasn't created by you");
	changevacancie;}
	else {
	       my $sth = $dbh->prepare('SELECT idu_s FROM vacancy where idu_p=? and id_stay=?') or die "Cant find table from database: $DBI::errstr\n";
        
        $sth->execute($id,$vacid) or die "Cant execute statement: $DBI::errstr\n";
	my @data=$sth->fetchrow_array();
		my $em2= $data[0];
	print   $q->start_form,
                        $q->start_table({-align=>center}),
                        $q->Tr([
                        $q->hidden(-name=>'Submit Vacancy',-value=>"$vacid"),
                        $q->td(['Reviewed user email:',       	$q->textfield(-name=> 'email')]),
                       
                        $q->td(['Date Start(yyyy-mm-dd):',
								$q->textfield(-name=> 'date1',-size=>10, -id => 'date1')]),
                        $q->td(['Date End(yyyy-mm-dd):',
								$q->textfield(-name=> 'date2',-size=>10, -id => 'date2')]),
						
						$q->td(['Kind of vacancy:',
                        $q->radio_group(-name => 'host',-values=>['I hosted','I was hosted'],-default=>'I hosted')]),
						$q->td(['Ranking:',scalar($q->radio_group(-name => 'reputation',-values=>['1','2','3','4','5'],-default=>'3'))]),
                        $q->td(['Description(optional):', $q->textfield(-name=> 'description')]),
						$q->td($q->submit(-name=>'Submit')),
                        ]),

                        $q->end_form;
	
	
	}
}

sub changevacancie{
		print	$q->start_form(-name=>"Vacancy Edition");
print              $q->td(['Select ID of Vacancy to Edit:',         $q->textfield(-name=> 'Vacancy Editing'),	$q->submit(-name=>"Select")	]);
                   $q->end_form;	
                  #mostra utilizadores
        db_on;
        my $sth = $dbh->prepare('SELECT * FROM vacancy') or die "Can't find table from database: $DBI::errstr\n";
        $sth->execute() or die "Can't execute statement: $DBI::errstr\n";
    print "<table border=1>\n";
    print "<tr><th>VacancyID</th><th>Email User 2</th><th>Type of vacancy</th><th>Start
Date</th><th>End Date</th><th>Reputation</th><th>Description</th></tr>\n";

        while (my @data = $sth->fetchrow_array()){
          my $usr=$dbh->prepare('SELECT email FROM user WHERE id_user =?') or die "Can't find table from database: $DBI::errstr\n";
	    $usr->execute($data[1]) or die "Can't execute statement: $DBI::errstr\n";
	    my @dat=$usr->fetchrow_array();
	    
	    my $u1=$dat[0];
	    #print "$u1";
	    $usr->execute($data[2]) or die "Can't execute statement: $DBI::errstr\n";
	    my @dat=$usr->fetchrow_array();
	    my $id = $session->param("uid");
	    my $u2=$dat[0];if (($u1 eq admin) or ($u2 eq admin)){} 
	    else {           
	     if ($id==$data[1]){
	     print "<tr>";
print "<td>$data[0]</td><td>$u2</td><td>$data[3]</td><td>$data[4]</td><td>$data[5]</td><td>$data[6]</td><td>$data[7]</td>"; 
 			
}
                        print   "</tr>\n";               }}
        print "</tr>\n";
        print "</table>\n";

        db_off;

}

sub viewvacancies{                  #mostra utilizadores
        db_on;
        my $sth = $dbh->prepare('SELECT * FROM vacancy') or die "Can't find table from database: $DBI::errstr\n";
        $sth->execute() or die "Can't execute statement: $DBI::errstr\n";
    print "<table border=1>\n";
    print "<tr><th>VacancyID</th><th>Email User 1</th><th>Email User 2</th><th>Type of vacancy</th><th>Start
Date</th><th>End Date</th><th>Reputation</th><th>Description</th></tr>\n";

        while (my @data = $sth->fetchrow_array()){
          my $usr=$dbh->prepare('SELECT email FROM user WHERE id_user =?') or die "Can't find table from database: $DBI::errstr\n";
	    $usr->execute($data[1]) or die "Can't execute statement: $DBI::errstr\n";
	    my @dat=$usr->fetchrow_array();
	    
	    my $u1=$dat[0];
	    #print "$u1";
	    $usr->execute($data[2]) or die "Can't execute statement: $DBI::errstr\n";
	    my @dat=$usr->fetchrow_array();
	    my $id = $session->param("uid");
	    my $u2=$dat[0];if (($u1 eq admin) or ($u2 eq admin)){} 
	    else {           
	     print "<tr>";
print "<td>$data[0]</td><td>$u1</td><td>$u2</td><td>$data[3]</td><td>$data[4]</td><td>$data[5]</td><td>$data[6]</td><td>$data[7]</td>"; 
				
}
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
                       
                        $q->td(['Date Start(yyyy-mm-dd):',
								$q->textfield(-name=> 'date1',-size=>10, -id => 'date1')]),
                        $q->td(['Date End(yyyy-mm-dd):',
								$q->textfield(-name=> 'date2',-size=>10, -id => 'date2')]),
						
						$q->td(['Kind of vacancy:',
                        $q->radio_group(-name => 'host',-values=>['I hosted','I was hosted'],-default=>'I hosted')]),
						$q->td(['Ranking:',scalar($q->radio_group(-name => 'reputation',-values=>['1','2','3','4','5'],-default=>'3'))]),
                        $q->td(['Description(optional):', $q->textfield(-name=> 'description')]),
						$q->td($q->submit(-name=>'Submit')),
                        ]),

                        $q->end_form;

}

sub search{     		#formulário da pesquisa
		print   $q->start_form,
                        $q->start_table({-align=>center}),
                        $q->Tr([
                        $q->hidden(-name=>'Search Results'),
                        $q->td(['Keyword:',         $q->textfield(-name=> 'searchf')]),
                                                $q->td(['Search:',
                        $q->radio_group(-name => 'types',-values=>['User by Reputation','User by Country','Vacancy by E-mail'],-default=>'User by Reputation')]),
                        $q->td($q->submit(-name=>'Submit')),
                        ]),

                        $q->end_form;

}

sub searchresults{ 		#resultados da pesquisa
			db_on;
			my $para=($q->param('searchf'));
			my $param=($q->param('types'));
			if ($q->param('types') eq "User by Reputation"){  
				my $sth = $dbh->prepare('SELECT * FROM user WHERE reputation=?') or die "Dead";
                 		$sth->execute($para);
                 		print $q->h2("$param: $para");
                 		print "<table>";
				print "<tr>";
				        while (my @data = $sth->fetchrow_array()){
					       if ($data[0] == 1) {}
							else{   
								print "<tr>";
      print"<td>$data[1]</td><td>$data[2]</td><td>$data[3]</td><td>$data[4]</td><td>$data[5]</td><td>$data[6]</td><td>$data[7]</td>";

      								print   "</tr>\n";               }
						}
#}
      			print "</tr>\n";
        		print "</table>\n";
			db_off;
			}
			  	elsif ($q->param('types') eq "User by Country"){
                                my $sth = $dbh->prepare('SELECT * FROM user WHERE country=?') or die "Dead";
                                $sth->execute($para);
                                print $q->h2("$param: $para");
                                print "<table>";
				print "<tr>";
                                
                                        while (my @data = $sth->fetchrow_array()){
                                                if ($data[0] == 1) {}
                                                        else{  
						 print "<tr>";
      
print"<td>$data[1]</td><td>$data[2]</td><td>$data[3]</td><td>$data[4]</td><td>$data[5]</td><td>$data[6]</td><td>$data[7]</td>";

                                                                print   "</tr>\n";
                                                
}
}
                        print "</tr>\n";
                        print "</table>\n";
                        db_off;
                        }
			else{
			print $q->h2("$param: $para");
			 print "<table border=1>\n";
    print "<tr><th>Email User 1</th><th>Type of vacancy</th><th>Email User 2</th><th>Start
Date</th><th>End Date</th><th>Reputation</th><th>Description</th></tr>\n";
			
                                my $sth1 = $dbh->prepare('SELECT * FROM user WHERE email=?') or die "Dead";
                                $sth1->execute($para);
				my @data = $sth1->fetchrow_array();
				my $sid=$data[0];
				;
                               my $sth = $dbh->prepare('SELECT * FROM vacancy WHERE idu_s=? OR idu_p=?') or die "Dead";
                               $sth->execute($sid,$sid);

                               
				
                                        while (my @data = $sth->fetchrow_array()){
                                                if ($sid == 1) {}
                                                        else{   
							my $usr=$dbh->prepare('SELECT email FROM user WHERE id_user =?') or die "Can't find table from database: $DBI::errstr\n";
	    $usr->execute($data[1]) or die "Can't execute statement: $DBI::errstr\n";
	    my @dat=$usr->fetchrow_array();
	    
	    my $u1=$dat[0];
	    #print "$u1";
	    $usr->execute($data[2]) or die "Can't execute statement: $DBI::errstr\n";
	    my @dat=$usr->fetchrow_array();
	    
	    my $u2=$dat[0];
	    if (($u1 eq admin) or ($u2 eq admin)){} 
	    else {            print "<tr>";
print "<td>$u1</td><td>$data[3]</td><td>$u2</td><td>$data[4]</td><td>$data[5]</td><td>$data[6]</td><td>$data[7]</td>"; 
			print"</tr>";	

                                                }}
}
                        
                        print "</tr>\n";
                        print "</table>\n";
                        db_off;
                        }
			}

			
			

sub testvacancy    {	db_on;
                        my $id = $session->param("uid");
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
                                                                if (($data[0] eq 0) || ($mail2 eq "admin"))
                                                                        {
                                                                        push (@errors,"-$mail2 is not registered!\n");
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
               else {	$d1=$q->param('date1');
               		$d2=$q->param('date1');
               		if ("$d2" ge "$d1") {}
                    
                            else {push(@errors,"-Start date can't be greater than end date.\n") ;
                                             $invalid2=1;}
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
			
			
			if (!($id == $ids)){
$sth->execute(($id),($ids),($host),($q->param('date1')),($q->param('date2')),($q->param('description')),($q->param('reputation')) ) or die "Erro  $DBI::errstr\n";
                       # print $q->p,"The user review is now registered!";
                 
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
                  
                 $sth = $dbh->prepare('UPDATE user SET reputation=? WHERE user.id_user=?') or die "Dead";
                 
                 $sth->execute($total,$ids);               
                  print $q->p,"The user review is now registered!";
                  #print $total;              
                                
                                
                                }
                         else  {      
                         		addvacancy;
                                print   $q->start_form,
                                        $q->start_table({-align=>center});
                                        #$q->Tr([;
                                        print $q->p,"You cannot review yourself!";
                                        #]),
                                        print $q->end_form;
 }
 	}							
 
                         db_off;
                        $invalid2=1;
                        }




sub menu1
{
    my $id=$session->param("uid");
    my $name = $session->param("em1");

    
    $logout_link = $q->a({-href => 'index.cgi?action=logout'}, "Logout");

    print $header,
    
    $q->start_div({-id => "topbar"}),
		$q->h1("Couch Surfing - $name"),
		  
				$q->start_div({-id => "login_form"}),
					$q->start_form({-id=>"form"}),
						$logout_link,
						
					$q->end_form,
				$q->end_div,
		$q->end_div,
    
		      
          $q->Tr([
              $q->start_form,
              $q->start_div({-id => "menubar"}),  
              $q->defaults('Home'),
              $q->submit(-name=>'View Users'),
              $q->submit(-name=>'Edit User'),
              $q->submit(-name=>'View Vacancies'),
              $q->submit(-name=>'Edit Vacancies'),
              $q->submit(-name=>'New Vacancy'),
              $q->submit(-name=>'Search'),
              $->end_div,
              $q->end_form]);





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
case "Highest Rated"	{ viewusers }	
case "Edit Vacancies"	{changevacancie}					
case "Vacancy Editing" {editvac}
case "Submit Vacancy" 	{ testeditvac }
case "Edit User"	{useredit}
case "Change User"	{usereditval}
else     		   	{ print "error\n" }
	       					}
				last; 
				}
			}	
} 
 
									
		db_on;
#my $session = CGI::Session->load;
$session = CGI::Session->load();
$q = new CGI; #object CGI
		 $header = $q->start_html(
        -title => 'Chouch Surfing',
        -style => [
            {-src => '../css/style.css'},
            {-src => '../css/calendarview.css'}],
        -script => [
            {-language => 'javascript', -src => '../js/prototype.js'},
            {-language => 'javascript', -src => '../js/calendarview.js'},
            {-language => 'javascript', -src => '../js/onload.js'}]
    );
							 
 
  if($session->is_expired)
  {
	print $q->header(-cache_control=>"no-cache, no-store, must-revalidate");
    print $q->h1("Couch Surfing");
	print "Your has session expired. Please login again.";
        $session->delete;
        $session->flush;

      	#print "<br/><a href='index.cgi>Login</a>";
  }
  elsif(($session->is_empty) || ($session->param("em1") eq "admin"))
  {
	
    print $q->header(-cache_control=>"no-cache, no-store, must-revalidate"),
    $header,
    $q->start_div({-id => "topbar"}),
		$q->h1("Couch Surfing"),
		  
				$q->start_div({-id => "login_form"}),
					$q->start_form({-id=>"form"});
	print $q->p,$q->a({-href=>'index.cgi'},"Login");    				
	print $q->end_div;
	print $q->end_div;
	print $q->p,"You have not logged in";

	#print "<br/><a href='index.cgi>Login</a>";
	#$session->delete;
	#$session->flush;  

  }
  else{


	print $q->header('text/html', -expires => "+30m",-cache_control=>"no-cache, no-store, must-revalidate");
	#print "<h2>Welcome";
	menu1;
	print $q->end_html;
}    



