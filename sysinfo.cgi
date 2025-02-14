#!/usr/bin/perl

#
# Authentic Theme 17.31 (https://github.com/qooob/authentic-theme)
# Copyright 2016 Ilia Rostovtsev <programming@rostovtsev.ru>
# Licensed under MIT (https://github.com/qooob/authentic-theme/blob/master/LICENSE)
#

#use strict;
#use warnings;

BEGIN { push( @INC, ".." ); }
use WebminCore;
&ReadParse();
&init_config();

do "authentic-theme/authentic-lib.cgi";

our %text = &load_language($current_theme);
our %text = ( &load_language('virtual-server'), %text );
our %text = ( &load_language('server-manager'), %text );

&header($title);

print '<div id="wrapper" class="page __sytem_information" data-notice="'
    . (
    (   -f $root_directory . '/authentic-theme/update'
            && $get_user_level == 0
    )
    ? _post_install()
    : '0'
    ) . '">' . "\n";
print '<div class="container-fluid col-lg-10 col-lg-offset-1">' . "\n";

if ( $get_user_level != 4 ) {
    print
        '<div id="system-status" class="panel panel-default" style="margin-bottom: 5px">'
        . "\n";
    print '<div class="panel-heading">' . "\n";
    print '<h3 class="panel-title">' . &text('body_header0') . (
        (          $get_user_level != 2
                && $get_user_level != 3
                && &foreign_available("webmin")
        )
        ? '<a href="/?updated" target="_top" data-href="'
            . $gconfig{'webprefix'}
            . '/webmin/edit_webmincron.cgi" data-refresh="system-status" class="btn btn-success pull-right" style="margin:-6px -11px; color: white;"><i class="fa fa-refresh"></i></a>
        <button type="button" class="btn btn-primary" style="display: none; visibility: hidden" data-toggle="modal" data-target="#update_notice"></button>'
        : ''
        )
        . '
    </h3>' . "\n";

    print '</div>';
    print '<div class="panel-body">' . "\n";
}

# Get system info to show
my @info = &list_combined_system_info( { 'qshow', 1 } );

if ( $get_user_level == 0 || $get_user_level == 4 ) {

    if ( $get_user_level != 4 ) {

        my ($cpu_percent,        $mem_percent,
            $virt_percent,       $disk_percent,
            $host,               $os,
            $webmin_version,     $virtualmin_version,
            $cloudmin_version,   $authentic_theme_version,
            $local_time,         $kernel_arch,
            $cpu_type,           $cpu_temperature,
            $hdd_temperature,    $uptime,
            $running_proc,       $load,
            $real_memory,        $virtual_memory,
            $disk_space,         $package_message,
            $csf_title,          $csf_data,
            $csf_remote_version, $authentic_remote_version
        ) = get_sysinfo_vars();

        # Easypie charts
        if ( __settings('settings_sysinfo_easypie_charts') ne 'false' ) {
            print_easypie_charts( $cpu_percent, $mem_percent, $virt_percent,
                $disk_percent );
        }

        print '<table class="table table-hover">' . "\n";

        # Hostname
        if ($host) {
            &print_table_row( &text('body_host'), $host, 'sysinfo_host' );
        }

        # Operating system
        if ($os) {
            &print_table_row( &text('body_os'), $os, 'sysinfo_os' );
        }

        # Webmin version
        &print_table_row( &text('body_webmin'), $webmin_version,
            'sysinfo_webmin_version' );

        # Virtualmin version
        if ($virtualmin_version) {
            print_table_row( $text{'right_virtualmin'},
                $virtualmin_version, 'sysinfo_virtualmin_version' );
        }

        # Cloudmin version
        if ($cloudmin_version) {
            print_table_row( $text{'right_vm2'}, $cloudmin_version,
                'sysinfo_cloudmin_version' );
        }

        # Theme version
        if ($authentic_theme_version) {
            &print_table_row( $text{'theme_version'},
                $authentic_theme_version, 'sysinfo_authentic_theme_version' );
        }

        #System time
        &print_table_row( &text('body_time'), $local_time,,
            'sysinfo_local_time' );

        # Kernel and arch
        if ($kernel_arch) {
            &print_table_row( &text('body_kernel'), $kernel_arch,
                'sysinfo_kernel_arch' );
        }

        # CPU Type and cores
        if ($cpu_type) {
            &print_table_row( $text{'body_cpuinfo'}, $cpu_type,
                'sysinfo_cpu_type' );
        }

        # Temperatures
        if ($cpu_temperature) {
            &print_table_row( $text{'body_cputemps'}, $cpu_temperature,
                'sysinfo_cpu_temperature' );
        }
        if ($hdd_temperature) {
            &print_table_row( $text{'body_drivetemps'},
                $hdd_temperature, 'sysinfo_hdd_temperature' );
        }

        # System uptime
        if ($uptime) {
            &print_table_row( $text{'body_uptime'}, $uptime,
                'sysinfo_uptime' );
        }

        # Running processes
        if ($running_proc) {
            &print_table_row( $text{'body_procs'}, $running_proc,
                'sysinfo_running_proc' );
        }

        # Load averages
        if ($load) {
            &print_table_row( $text{'body_cpu'}, $load, 'sysinfo_load' );
        }

        # Real memory details
        if ($real_memory) {
            &print_table_row( $text{'body_real'}, $real_memory,
                'sysinfo_real_memory' );
        }

        # Virtual memory details
        if ($virtual_memory) {
            &print_table_row( $text{'body_virt'}, $virtual_memory,
                'sysinfo_virtual_memory' );
        }

        # Local disk space
        if ($disk_space) {
            &print_table_row(
                $text{'body_disk'}, $disk_space, 'sysinfo_disk_space'

            );
        }

        # ConfigServer Security & Firewall version
        if ( $csf_title && $csf_data ) {
            &print_table_row(
                $csf_title, $csf_data, 'sysinfo_csf_data'

            );
        }

        # Package updates
        if ($package_message) {
            &print_table_row( $text{'body_updates'}, $package_message,
                'sysinfo_package_message' );
        }
        print '</table>' . "\n";

        # Print System Warning
        print_sysinfo_warning(@info);

        print '</div>';    # Panel Body
        print '</div>';    # Panel Default
    }

    print_extended_sysinfo(@info);

}
elsif ( $get_user_level == 2 ) {

    # Domain owner
    # Show a server owner info about one domain
    $ex = virtual_server::extra_admin();
    if ($ex) {
        $d = virtual_server::get_domain($ex);
    }
    else {
        $d = virtual_server::get_domain_by( "user", $remote_user, "parent",
            "" );
    }

    print '<table class="table table-hover">' . "\n";

    &print_table_row( $text{'right_login'}, $remote_user );

    &print_table_row( $text{'right_from'}, $ENV{'REMOTE_HOST'} );

    # Print Virtualmin version
    if ($has_virtualmin) {
        my $__virtual_server_version
            = $virtual_server::module_info{'version'};
        $__virtual_server_version =~ s/.gpl//igs;
        &print_table_row( $text{'right_virtualmin'},
            $__virtual_server_version );
    }
    else {
        &print_table_row( $text{'right_virtualmin'}, $text{'right_not'} );
    }

    # Print Theme version/updates
    get_authentic_version();

    # Build response message
    if ( $remote_version <= $installed_version ) {
        $authentic_theme_version
            = '' . $text{'theme_name'} . ' ' . $installed_version;
    }
    else {
        $authentic_theme_version
            = ''
            . $text{'theme_name'} . ' '
            . $installed_version . '. '
            . $text{'theme_update_available'} . ' '
            . $remote_version
            . '&nbsp;&nbsp;<a class="btn btn-xs btn-info" style="padding:0 6px; line-height: 12px; height:15px;font-size:11px" target="_blank" href="https://github.com/qooob/authentic-theme/blob/master/CHANGELOG.md"><i class="fa fa-pencil-square-o" style="padding-top:1px">&nbsp;</i>'
            . ''
            . $text{'theme_changelog'} . '</a>';
    }
    &print_table_row( $text{'theme_version'}, $authentic_theme_version );

    # Print domain name
    $dname
        = defined(&virtual_server::show_domain_name)
        ? &virtual_server::show_domain_name($d)
        : $d->{'dom'};
    &print_table_row( $text{'right_dom'}, $dname );

    @subs = ( $d, virtual_server::get_domain_by( "parent", $d->{'id'} ) );
    @reals = grep { !$_->{'alias'} } @subs;
    @mails = grep { $_->{'mail'} } @subs;
    ( $sleft, $sreason, $stotal, $shide )
        = virtual_server::count_domains("realdoms");
    if ( $sleft < 0 || $shide ) {
        &print_table_row( $text{'right_subs'}, scalar(@reals) );
    }
    else {
        &print_table_row( $text{'right_subs'},
            text( 'right_of', scalar(@reals), $stotal ) );
    }

    @aliases = grep { $_->{'alias'} } @subs;
    if (@aliases) {
        ( $aleft, $areason, $atotal, $ahide )
            = virtual_server::count_domains("aliasdoms");
        if ( $aleft < 0 || $ahide ) {
            &print_table_row( $text{'right_aliases'}, scalar(@aliases) );
        }
        else {
            &print_table_row( $text{'right_aliases'},
                text( 'right_of', scalar(@aliases), $atotal ) );
        }
    }

    # Users and aliases info
    $users = virtual_server::count_domain_feature( "mailboxes", @subs );
    ( $uleft, $ureason, $utotal, $uhide )
        = virtual_server::count_feature("mailboxes");
    $msg = @mails ? $text{'right_fusers'} : $text{'right_fusers2'};
    if ( $uleft < 0 || $uhide ) {
        &print_table_row( $msg, $users );
    }
    else {
        &print_table_row( $msg, text( 'right_of', $users, $utotal ) );
    }

    if (@mails) {
        $aliases = virtual_server::count_domain_feature( "aliases", @subs );
        ( $aleft, $areason, $atotal, $ahide )
            = virtual_server::count_feature("aliases");
        if ( $aleft < 0 || $ahide ) {
            &print_table_row( $text{'right_faliases'}, $aliases );
        }
        else {
            &print_table_row( $text{'right_faliases'},
                text( 'right_of', $aliases, $atotal ) );
        }
    }

    # Databases
    $dbs = virtual_server::count_domain_feature( "dbs", @subs );
    ( $dleft, $dreason, $dtotal, $dhide )
        = virtual_server::count_feature("dbs");
    if ( $dleft < 0 || $dhide ) {
        &print_table_row( $text{'right_fdbs'}, $dbs );
    }
    else {
        &print_table_row( $text{'right_fdbs'},
            text( 'right_of', $dbs, $dtotal ) );
    }

    if ( !$sects->{'noquotas'}
        && virtual_server::has_home_quotas() )
    {
        # Disk usage for all owned domains
        $homesize = virtual_server::quota_bsize("home");
        $mailsize = virtual_server::quota_bsize("mail");
        ( $home, $mail, $db ) = virtual_server::get_domain_quota( $d, 1 );
        $usage = $home * $homesize + $mail * $mailsize + $db;
        $limit = $d->{'quota'} * $homesize;
        if ($limit) {
            &print_table_row( $text{'right_quota'},
                text( 'right_of', nice_size($usage), &nice_size($limit) ),
                3 );
        }
        else {
            &print_table_row( $text{'right_quota'}, nice_size($usage), 3 );
        }
    }

    if (  !$sects->{'nobw'}
        && $virtual_server::config{'bw_active'}
        && $d->{'bw_limit'} )
    {
        # Bandwidth usage and limit
        &print_table_row(
            $text{'right_bw'},
            &text(
                'right_of',
                &nice_size( $d->{'bw_usage'} ),
                &text(
                    'edit_bwpast_' . $virtual_server::config{'bw_past'},
                    &nice_size( $d->{'bw_limit'} ),
                    $virtual_server::config{'bw_period'}
                )
            ),
            3
        );
    }

    print '</table>' . "\n";

    # New features for domain owner
    #show_new_features(0);

    print '</div>';    # Panel Body
    print '</div>';    # Panel Default

    print_extended_sysinfo(@info);
}
elsif ( $get_user_level == 3 ) {
    print '<table class="table table-hover">' . "\n";

    # Host and login info
    &print_table_row( &text('body_host'), &get_system_hostname() );

    # Operating System Info
    if ( $gconfig{'os_version'} eq '*' ) {
        $os = $gconfig{'real_os_type'};
    }
    else {
        $os = $gconfig{'real_os_type'} . ' ' . $gconfig{'real_os_version'};
    }
    &print_table_row( &text('body_os'), $os );

    # Usermin version
    &print_table_row( &text('body_usermin'), &get_webmin_version() );

    # Theme version/updates
    get_authentic_version();

    # Build response message
    if ( $remote_version <= $installed_version ) {
        $authentic_theme_version
            = '' . $text{'theme_name'} . ' ' . $installed_version;
    }
    else {
        $authentic_theme_version
            = ''
            . $text{'theme_name'} . ' '
            . $installed_version . '. '
            . $text{'theme_update_available'} . ' '
            . $remote_version
            . '&nbsp;&nbsp;<a class="btn btn-xs btn-info" style="padding:0 6px; line-height: 12px; height:15px;font-size:11px" target="_blank" href="https://github.com/qooob/authentic-theme/blob/master/CHANGELOG.md"><i class="fa fa-pencil-square-o" style="padding-top:1px">&nbsp;</i>'
            . ''
            . $text{'theme_changelog'} . '</a>';
    }
    &print_table_row( $text{'theme_version'}, $authentic_theme_version );

    #System Time
    $tm = localtime( time() );
    if ( &foreign_available("time") ) {
        $tm = '<a href=' . $gconfig{'webprefix'} . '/time/>' . $tm . '</a>';
    }
    &print_table_row( &text('body_time'), $tm );

    print '</table>' . "\n";

    print '</div>';    # Panel Body
    print '</div>';    # Panel Default

    print_extended_sysinfo(@info);
}

# End of page

print '</div>' . "\n";
print '</div>' . "\n";
&footer();
