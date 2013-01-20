#!/usr/bin/perl

#log.pl

use FreezeThaw qw(freeze thaw cmpStr safeFreeze cmpStrHard);
use Switch;
use CGI;
use CGI::Carp qw/fatalsToBrowser warningsToBrowser/;
use CGI::Session( -'ip_match');
use DBI;
use DBD::mysql;
use Digest::SHA1 qw( sha1_hex sha1_base64 );
use constant secretphrase => "asjdiashdoaho34230hy8sdf";
use MIME::Lite::TT;
#use String::Random;
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



sub testuser    {       db_on;
                        $mailu = $q->param('email');
                        $invalid=0;
                        my $sth = $dbh->prepare('SELECT count(*) FROM user WHERE email=?') or die "Dead";
                        @errors=("The following errors were found, please correct:\n");
                        if ($mailu eq "") {
                                        push(@errors, "-Blank email. Please insert a valid email.\n");
                                        $invalid=1;}
                        else    {
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

                                        else            {
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
                        my $secretphrase => "asjdiashdoaho34230hy8sdf";
                my $pass = sha1_base64(($q->param('email')), $q->param('password') , $secretphrase);
                my $sth = $dbh->prepare('INSERT INTO user(name,email,address,city,country,description,password) values (?,?,?,?,?,?,?)') or die 
"Dead";

$sth->execute(($q->param('name')),($q->param('email')),($q->param('address')),($q->param('city')),($q->param('country')),($q->param('description')),$pass 
)
or
die
"Erro";
                        print $q->p,"The user $mailu is now registered!";

                                }
                        db_off;
                        $invalid=1;
                        }




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
                        $q->td(['Description:', $q->textfield(-name=> 'description',-size=>100)]),
                        $q->td(['Password(min. 8 char.):',        $q->password_field(             -name=>'password',
                                                                                -size=>15,
                                                                                -maxlength=>15)]),
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


sub viewusers{                  #mostra utilizadores
        db_on;
        my $sth = $dbh->prepare('SELECT * FROM user') or die "Can't find table from database: $DBI::errstr\n";
        $sth->execute() or die "Can't execute statement: $DBI::errstr\n";

        print "<table border=1>\n";
        print
"<tr><th>Name</th><th>Address</th><th>City</th><th>Country</th><th>Description</th><th>Reputation</th></tr>\n";
        @data=$sth->fetchrow_array();
        while (my @data = $sth->fetchrow_array()){
        print "<tr>";
        print 
"<td>$data[1]</td><td>$data[3]</td><td>$data[4]</td><td>$data[5]</td><td>$data[6]</td><td>$data[7]</td>";

        print   "</tr>\n";               }
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
        print "<tr><th>Reviewer</th><th>Type of vacancy</th><th>Reviewed</th><th>Start 
Date</th><th>EndDate</th><th>Reputation</th><th>Description</th></tr>\n";
#8

	while (my @data = $sth->fetchrow_array()){
	    my $usr=$dbh->prepare('SELECT name FROM user WHERE id_user =?') or die "Can't find table from database: $DBI::errstr\n";
	    $usr->execute($data[1]) or die "Can't execute statement: $DBI::errstr\n";
	    my @dat=$usr->fetchrow_array();
	    
	    my $u1=$dat[0];
	    #print "$u1";
	    $usr->execute($data[2]) or die "Can't execute statement: $DBI::errstr\n";
	    my @dat=$usr->fetchrow_array();
	    my $u2=$dat[0];
	    
	    if ($u1 eq "admin" or $u2 eq "admin"){}
	    else{
        print "<tr>";
	print "<td>$u1</td><td>$data[3]</td><td>$u2</td><td>$data[4]</td><td>$data[5]</td><td>$data[6]</td><td>$data[7]</td>"; 
				
	print	"</tr>\n";		 }
            }            
        print "</tr>\n";
        print "</table>\n";
 
        db_off;
}


sub testpass{		if (!($q->param('emrec') eq "admin")){
			db_on;
			 my $sth = $dbh->prepare('SELECT count(*) FROM user WHERE email=?') or die "Dead";
        	

			$e=$q->param('emrec');
			$sth->execute($e) or die "Can't execute statement: $DBI::errstr\n";
			@data=$sth->fetchrow_array();
			if ($data[0] gt 0) {
			my $email=$e;
			
			my $random_string =  int(rand(9898989)) + 9898998;
			my %params = ( pwd=>"$random_string");

			my $template = <<'TEMPLATE';
                        Your new password:
                        [% pwd %]
                        We advise you to change it as soon as possible. 
TEMPLATE
			
			my $msg = MIME::Lite::TT->new(
				    From => 'admin', 
				    To => $email , 
				    Subject => 'Couch Surfing - Lost Password', 
				    Template => \$template,
				    TmplParams => \%params,); 
		        $msg->send;
		        my $secretphrase => "asjdiashdoaho34230hy8sdf";
                my $pass = sha1_base64(($q->param('emrec')), $random_string , $secretphrase);
                 my $sth = $dbh->prepare('UPDATE user set password=?') or die "Can't find table from database: $DBI::errstr\n";
        

			
			$sth->execute($pass) or die "Can't execute statement: $DBI::errstr\n";
		print "Check you email!";	
	}
	else { print "Invalid Email!";}
}
else { print "Invalid Email!";}
}
sub lostpass{	print	$q->start_form,
                        $q->start_table({-align=>center}),
                        
                        $q->hidden(-name=>'Lost'),
                        
                        $q->td(['Email:',       $q->textfield(-name=> 'emrec')]),
                        $q->td($q->submit(-name=>"Recover Password Now")),
                        $q->p, "You inserted a wrong password.If you wish to get a new one by mail. please confirm your email.";
                        $q->end_table,
                        $q->end_form;
		 }

sub menu1{
	#$id=$session->param("uid");
	#my $name = $session->param("em1");
	print   $q->start_html(-title=>'Couch Surfing - Welcome page',-style=>{-src=>'../css/style.css'}),

		$q->start_div({-id => "topbar"}),
		$q->h1("Couch Surfing - Welcome"),
		  
				$q->start_div({-id => "login_form"}),
					$q->start_form({-id=>"form"}),
						"<label for='em'>Email</label>",
						$q->textfield(-name=> 'em', -id => "email"),
						"<label for='em'>Password</label>",
						$q->password_field(-name=>'pwd', -id => "pwd"),
						$q->submit('Log in'),
					$q->end_form,
				$q->end_div,
		$q->end_div;

				
	print       $q->Tr([
		$q->start_form,
		$q->start_div({-id => "menubar"}), 
		$q->defaults('Home'),
		$q->submit(-name=>'View Users'),
		$q->submit(-name=>'View Vacancies'),
		$q->submit(-name=>'New User'),
		$q->end_div,
		$q->end_form,	
		]);






	my $all_params = $q->Vars;

	if ($invalid == 1 or $invalid2 == 1)
			{        $invalid=0;
				 $invalid2=0;
			}

	else                    {
				foreach $param (keys %$all_params)
					{
					#print $q->h2("$param");
					switch ($param){
								case    "View Users"            { viewusers }
								case    "View Vacancies"        { viewvacancies }
								case    "New User"           	{ adduser }
								case    "Add User"           	{ testuser }
case 	"try"		{print 
				$q->start_table,
				$q->start_form,
				$q->p,"Wrong Username or Password. Please try again.",
				$q->submit(-name=>'Lost Password?'),
				$q->end_form,
				$q->end_table;
				
				}
case 	"Lost Password?"	{lostpass}					
case	"Lost"		{testpass}		else                            { print "" }
							}
					last;
					}
				}
}









$em = $q->param('em');
$pwd =$q->param('pwd');

if ($em ne  "")								#se mail tiver algo verifica se deve ou nao criar sessao
	{	db_on;
		my $pass = sha1_base64( $em, $pwd, $secretphrase);
		$sth = $dbh->prepare('SELECT count(email) FROM user WHERE password=? and email=?') or die "Dead";
  		$sth->execute($pass,$em) or die "Can't execute statement: $DBI::errstr\n";
  		my @data= $sth->fetchrow_array();
		
		if  ($em eq "admin" and $pwd eq "admin")
			{
			$session = new CGI::Session("driver:MySQL",undef, {Handle=>$dbh}) or die CGI::Session->errstr;
   			$session = new CGI::Session() or die CGI::Session->errstr;
			$session->param("em1", $em);
			$sth = $dbh->prepare('SELECT id_user FROM user WHERE email=?') or die "Dead";
  		$sth->execute($em) or die "Can't execute statement: $DBI::errstr\n";
  		my @data= $sth->fetchrow_array();
                        $session->param("uid", $data[0]);
			print $session->header(-location=>'index1.cgi');
			#db_off;
		       }

		else{
  			if (($data[0] gt 0))
			{
			#$session = new CGI::Session("driver:File", $cgi, {Directory=>File::Spec->tmpdir});
			#$sid = $q->cookie("CGISESSID") || undef;
			$session = new CGI::Session("driver:MySQL", undef , {Handle=>$dbh}) or die CGI::Session->errstr;
			$session = new CGI::Session() or die CGI::Session->errstr;
			$session->param("em1",$em);
			$sth = $dbh->prepare('SELECT id_user FROM user WHERE email=?') or die "Dead";
  		$sth->execute($em) or die "Can't execute statement: $DBI::errstr\n";
  		my @data= $sth->fetchrow_array();
			$session->param("uid",$data[0]);
			print $session->header(-location=>'index2.cgi');
			}
		else
			{
			
			print 	$q->header;
			menu1;
		print	$q->end_html;
			#print $q->header(-type=>'text/html',-location=>"index.cgi");		
			#print $q->header(-type=>'text/html');
			lostpass;
			#print "Erro";
			}
	}}

else	{	if($q->param('action') eq 'logout')	#se mail nao estiver preenchido e accção for logout
			{
			$session = CGI::Session->load() or die CGI::Session->errstr;
			$session->delete();
			$session->flush();
			print $session->header(-location=>'index2.cgi');
			}
		else {  if($q->param('action') eq 'logout1')     #se mail nao estiver preenchido e accção for logout
                        {
                        $session = CGI::Session->load() or die CGI::Session->errstr;
                        $session->delete();
                        $session->flush();
                        print $session->header(-location=>'index1.cgi');
                        }

		else					
			{
		print 	$q->header;
		menu1;
		print	$q->end_html;
			}
}}
