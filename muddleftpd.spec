Summary:	PROfessional FTP Daemon with apache-like configuration syntax
Summary(pl):	PROfesionalny serwer FTP  
Name:		muddleftpd
Version:	1.3.7
Release:	1
License:	GPL
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	http://www.arach.net.au/~wildfire/muddleftpd/%{name}.%{version}.tar.gz
URL:		http://www.muddleftpd.cx/
BuildRequires:	pam-devel
Requires:	logrotate
Requires:	inetdaemon
Provides:	ftpserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	ftpserver
Obsoletes:	anonftp
Obsoletes:	bftpd
Obsoletes:	ftpd-BSD
Obsoletes:	heimdal-ftpd
Obsoletes:	linux-ftpd
Obsoletes:	pure-ftpd
Obsoletes:	wu-ftpd

%define		_sysconfdir	/etc/ftpd
%define		_localstatedir	/var/run

%description
FIXME

%description -l pl
FIXME

%prep
%setup -q -n %{name}.%{version}

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%post 
touch /var/log/xferlog
awk 'BEGIN { FS = ":" }; { if(($3 < 1000)&&($1 != "ftp")) print $1; }' < /etc/passwd >> %{_sysconfdir}/ftpusers.default
if [ ! -f %{_sysconfdir}/ftpusers ]; then
	( cd %{_sysconfdir}; mv -f ftpusers.default ftpusers )
fi

#%post inetd
#if grep -iEqs "^ServerType[[:space:]]+standalone" %{_sysconfdir}/proftpd.conf ; then
#	cp -a %{_sysconfdir}/proftpd.conf %{_sysconfdir}/proftpd.conf.rpmorig
#	sed -e "s/^ServerType[[:space:]]\+standalone/ServerType			inetd/g" \
#		%{_sysconfdir}/proftpd.conf.rpmorig >%{_sysconfdir}/proftpd.conf
#fi
#if [ -f /var/lock/subsys/rc-inetd ]; then
#	/etc/rc.d/init.d/rc-inetd restart 1>&2
#else
#	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
#fi

#%postun inetd
#if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
#	/etc/rc.d/init.d/rc-inetd reload 1>&2
#fi
#
#%post standalone
#/sbin/chkconfig --add proftpd
#if grep -iEqs "^ServerType[[:space:]]+inetd" %{_sysconfdir}/proftpd.conf ; then
#	cp -a %{_sysconfdir}/proftpd.conf %{_sysconfdir}/proftpd.conf.rpmorig
#	sed -e "s/^ServerType[[:space:]]\+inetd/ServerType			standalone/g" \
#		%{_sysconfdir}/proftpd.conf.rpmorig >%{_sysconfdir}/proftpd.conf
#fi
#if [ -f /var/lock/subsys/proftpd ]; then
#	/etc/rc.d/init.d/proftpd restart 1>&2
#else
#	echo "Run \"/etc/rc.d/init.d/proftpd start\" to start ProFTPD daemon."
#fi
#
#%preun standalone
#if [ "$1" = "0" -a -f /var/lock/subsys/proftpd ]; then
#	/etc/rc.d/init.d/proftpd stop 1>&2
#fi
#/sbin/chkconfig --del proftpd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {ChangeLog,README*}.gz contrib/README.modules.gz
%doc sample-configurations/{virtual,anonymous}.conf.gz 
%doc doc/*html

%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) /etc/logrotate.d/*
%attr(640,root,root) %ghost /var/log/*
%{?!bcond_off_pam:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*}

%attr(640,root,root) %{_sysconfdir}/ftpusers.default
%attr(640,root,root) %ghost %{_sysconfdir}/ftpusers

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*

%{_mandir}/man[158]/*

%dir /home/ftp/pub
%attr(711,root,root) %dir /home/ftp/pub/Incoming
