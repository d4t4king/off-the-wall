#!/usr/bin/perl
#
# (c) SmoothWall Ltd, 2006
#
# This script rewrites the IMSpector config

use lib "/usr/lib/smoothwall/";
use header qw( :standard );

my %settings;

&readhash("${swroot}/im/settings", \%imsettings);

open(FILE, "/usr/lib/smoothwall/imspector.conf.in");
my @conf = <FILE>;
close(FILE);
open(FILE, ">${swroot}/im/imspector.conf");
print FILE @conf;

if ($imsettings{'MSN'} eq 'on') {
	print FILE "msn_protocol=on\n"; }
if ($imsettings{'YAHOO'} eq 'on') {
	print FILE "yahoo_protocol=on\n"; }
if ($imsettings{'ICQ'} eq 'on') {
	print FILE "icq_protocol=on\n"; }
if ($imsettings{'IRC'} eq 'on') {
	print FILE "irc_protocol=on\n"; }
	
if ($imsettings{'FILTERING'} eq 'on')
{
	print FILE "badwords_filename=/usr/etc/imspector/badwords.txt\n";
	print FILE "badwords_replace_character=*\n";
}

close(FILE);
