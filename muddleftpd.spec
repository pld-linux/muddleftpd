Summary:	muddleftpd - ftp daemon
Summary(pl):	muddleftpd - serwer ftp
Name:		muddleftpd
Version:	1.3.12.1
Release:	2
License:	GPL
Group:		Daemons
Source0:	http://savannah.nongnu.org/download/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	208d94621a31a76a7e9baaac08463c29
Source1:	ftp.pamd
Source2:	%{name}.logrotate
Source3:	%{name}.init
Source4:	%{name}.sysconfig
Source5:	%{name}.conf
Source6:	%{name}-mudpasswd.1
Patch0:		%{name}-MD5-passwd.patch
URL:		http://www.nongnu.org/muddleftpd/
BuildRequires:	autoconf
BuildRequires:	pam-devel
BuildRequires:	texinfo
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	logrotate
Provides:	ftpserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	ftpserver
Obsoletes:	anonftp
Obsoletes:	bftpd
Obsoletes:	ftpd-BSD
Obsoletes:	heimdal-ftpd
Obsoletes:	linux-ftpd
Obsoletes:	proftpd
Obsoletes:	proftpd-common
Obsoletes:	proftpd-inetd
Obsoletes:	proftpd-standalone
Obsoletes:	pure-ftpd
Obsoletes:	troll-ftpd
Obsoletes:	vsftpd
Obsoletes:	wu-ftpd

%define		_sysconfdir	/etc/muddleftpd
%define		_localstatedir	/var/run

%description
MUDDLEFTPD is a server for the Internet File Transfer Protocol. Normal
FTP servers tend to always want to run with root privileges on the
server host. MUDDLEFTPD is designed to overcome this obstacle without
limiting the available features when running without root privileges.

%description -l pl
MUDDLEFTPD jest serwerem FTP. O ile wi�kszo�� serwer�w FTP chce
uprawnie� roota, MUDDLEFTPD zosta� zaprojektowany tak, aby m�g�
dzia�a� bez tych uprawnie� bez zbytniego ograniczenia mo�liwo�ci.

%prep
%setup -q
%patch0 -p1

%build
rm -f configure
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir},/var/log} \
	$RPM_BUILD_ROOT/etc/{pam.d,logrotate.d,rc.d/init.d,sysconfig,security} \
	$RPM_BUILD_ROOT/home/services/ftp/{pub,upload}

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	INFODIR=$RPM_BUILD_ROOT%{_infodir}

mv -f $RPM_BUILD_ROOT%{_sbindir}/ftpwho $RPM_BUILD_ROOT%{_bindir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/ftp
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/muddleftpd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/muddleftpd
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/muddleftpd
install %{SOURCE6} $RPM_BUILD_ROOT%{_mandir}/man1/mudpasswd.1


touch $RPM_BUILD_ROOT/var/log/muddleftpd
touch $RPM_BUILD_ROOT/etc/security/blacklist.ftp

install src/ratiotool		$RPM_BUILD_ROOT%{_bindir}
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/muddleftpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/chkconfig --add muddleftpd
if [ -f /var/lock/subsys/muddleftpd ]; then
	/etc/rc.d/init.d/muddleftpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/muddleftpd start\" to start muddleftpd daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/muddleftpd ]; then
		/etc/rc.d/init.d/muddleftpd stop 1>&2
	fi
	/sbin/chkconfig --del muddleftpd
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES README TODO doc/*.txt examples
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/muddleftpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/security/blacklist.ftp
%attr(640,root,root) /etc/logrotate.d/*
%attr(640,root,root) %ghost /var/log/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) /etc/sysconfig/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %dir /home/services/ftp
%attr(755,root,root) %dir /home/services/ftp/pub
%attr(700,root,ftp) %verify(not mode) %dir /home/services/ftp/upload
%{_mandir}/man1/*
%{_infodir}/*.info*
