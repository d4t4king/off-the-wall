#!/usr/bin/perl
#
# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team

use lib "/usr/lib/smoothwall";
use header qw( :standard );
use smoothd qw( message );
use Cwd;

my (%snortsettings, %checked);

&showhttpheaders();

$snortsettings{'ENABLE_SNORT'} = 'off';
$snortsettings{'ACTION'} = '';
&getcgihash(\%snortsettings);

$errormessage = '';
$extramessage = '';
if ($snortsettings{'ACTION'} eq 'Save & Update rules')
{
	if (defined $snortsettings{'OINK'} && $snortsettings{'OINK'} ne '') 
	{
		if ($snortsettings{'OINK'} !~ /^([\da-f]){40}$/i)
		{
			$errormessage = 'Bad Oink code - must be 40 hex digits';
		}
		else
		{
			my $curdir = getcwd;
			my $url = 'http://www.snort.org/pub-bin/oinkmaster.cgi/' . $snortsettings{'OINK'} . '/snortrules-snapshot-CURRENT.tar.gz';
			chdir "${swroot}/snort/";
			if (open(FD, "/usr/bin/oinkmaster.pl -C ./oinkmaster.conf -o rules -u $url|"))
			{
				while(<FD>) {
					$extramessage .= $_ . "\n";
				}
				close(FD);
	
				if ($extramessage ne '')	
				{
					warn $extramessage;
				}
				else
				{
					$errormessage = "Rules not available - try later";
				}
			}
			else
			{
				$errormessage = "Cannot run oinkmaster.pl";
			}
			chdir $curdir;
		} 
	}
}
if ($snortsettings{'ACTION'} eq $tr{'save'} || $snortsettings{'ACTION'} eq 'Save & Update rules')
{

	&writehash("${swroot}/snort/settings", \%snortsettings);
	if ($snortsettings{'ENABLE_SNORT'} eq 'on')
	{
		&log($tr{'snort is enabled'});
		system ('/bin/touch', "${swroot}/snort/enable");
	}
	else
	{
		&log($tr{'snort is disabled'});
		unlink "${swroot}/snort/enable";
	} 
	my $success = message('snortrestart');

	if (not defined $success) {
		$errormessage = $tr{'smoothd failure'}; }

}

&readhash("${swroot}/snort/settings", \%snortsettings);
$snortsettings{OINK} = '' unless defined $snortsettings{OINK};
$checked{'ENABLE_SNORT'}{'off'} = '';
$checked{'ENABLE_SNORT'}{'on'} = '';
$checked{'ENABLE_SNORT'}{$snortsettings{'ENABLE_SNORT'}} = 'CHECKED';

&openpage($tr{'intrusion detection system'}, 1, '', 'services');

&openbigbox('100%', 'LEFT');

&alertbox($errormessage);

print "<FORM METHOD='POST'>\n";

&openbox($tr{'intrusion detection system2'});
print <<END
<TABLE WIDTH='100%'>
<TR>
	<TD WIDTH='25%' CLASS='base'>Snort:</TD>
	<TD WIDTH='25%'><INPUT TYPE='checkbox' NAME='ENABLE_SNORT' $checked{'ENABLE_SNORT'}{'on'}></TD>
	<TD WIDTH='25%'>&nbsp;</TD>
	<TD WIDTH='35%'>&nbsp;</TD>
</TR>
</TABLE>
END
;
&closebox();

print <<END
<DIV ALIGN='CENTER'>
<TABLE WIDTH='60%'>
<TR>
	<TD ALIGN='CENTER'><INPUT TYPE='submit' NAME='ACTION' VALUE='$tr{'save'}'></TD> 
</TR>
</TABLE>
</DIV>
END
;

my $ruleage = int(-M "${swroot}/snort/rules/VRT-License.txt");
&openbox('Rules retreval:');
print <<END
<TABLE WIDTH='100%'>
<TR>
	<TD WIDTH='25%'>Oink code:</TD>
	<TD WIDTH='75%'><INPUT TYPE='text' NAME='OINK' SIZE=42 MAXLENGTH=42 VALUE=$snortsettings{OINK}></TD>
</TR>
<TR>
	<TD>Rule age in days:</TD><TD>$ruleage</TD>
</TR>
</TABLE>
END
;

&closebox();

print <<END
<DIV ALIGN='CENTER'>
<TABLE WIDTH='60%'>
<TR>
	<TD ALIGN='CENTER'><INPUT TYPE='submit' NAME='ACTION' VALUE='Save & Update rules'></TD> 
</TR>
</TABLE>
</DIV>
END
;

print "</FORM>\n";

&alertbox('add', 'add');

&closebigbox();

&closepage();

