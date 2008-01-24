Summary:	muddleftpd - FTP daemon
Summary(pl.UTF-8):	muddleftpd - serwer FTP
Name:		muddleftpd
Version:	1.3.13.1
Release:	5
License:	GPL
Group:		Daemons
Source0:	http://savannah.nongnu.org/download/muddleftpd/%{name}-%{version}.tar.gz
# Source0-md5:	47cf007466395ce43920f5e60234e107
Source1:	ftp.pamd
Source2:	%{name}.logrotate
Source3:	%{name}.init
Source4:	%{name}.sysconfig
Source5:	%{name}.conf
Source6:	%{name}-mudpasswd.1
Patch0:		%{name}-MD5-passwd.patch
Patch1:		%{name}-DONT_INST_DOC.patch
Patch2:		%{name}-allowed_filenames_fix.patch
URL:		http://www.nongnu.org/muddleftpd/
BuildRequires:	mysql-devel
BuildRequires:	pam-devel
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	texinfo
Requires(post,preun):	/sbin/chkconfig
Requires:	logrotate
Requires:	pam >= 0.79.0
Requires:	rc-scripts
Provides:	ftpserver
Obsoletes:	anonftp
Obsoletes:	bftpd
Obsoletes:	ftpd-BSD
Obsoletes:	ftpserver
Obsoletes:	glftpd
Obsoletes:	heimdal-ftpd
Obsoletes:	krb5-ftpd
Obsoletes:	linux-ftpd
Obsoletes:	proftpd
Obsoletes:	proftpd-common
Obsoletes:	proftpd-inetd
Obsoletes:	proftpd-standalone
Obsoletes:	pure-ftpd
Obsoletes:	troll-ftpd
Obsoletes:	vsftpd
Obsoletes:	wu-ftpd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/muddleftpd
%define		_localstatedir	/var/run

%description
MUDDLEFTPD is a server for the Internet File Transfer Protocol. Normal
FTP servers tend to always want to run with root privileges on the
server host. MUDDLEFTPD is designed to overcome this obstacle without
limiting the available features when running without root privileges.

%description -l pl.UTF-8
MUDDLEFTPD jest serwerem FTP. O ile większość serwerów FTP chce
uprawnień roota, MUDDLEFTPD został zaprojektowany tak, aby mógł
działać bez tych uprawnień bez zbytniego ograniczenia możliwości.

%package authlibmud
Summary:	MUD authentication library for muddleftpd
Summary(pl.UTF-8):	Biblioteka do uwierzytelniania MUD dla muddleftpd
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description authlibmud
This module allows muddleftpd to authenticate against player files on
a mud server.

%description authlibmud -l pl.UTF-8
Ten moduł pozwala muddleftpd uwierzytelniać użytkowników w oparciu o
pliki graczy na serwerze muda.

%package authlibmysql
Summary:	MySQL authentication library for muddleftpd
Summary(pl.UTF-8):	Biblioteka uwierzytelniania MySQL dla muddleftpd
Group:		Daemons
Requires:	%{name} = %{version}-%{release}
# no R:	mysql - database can be remote

%description authlibmysql
This module allows muddleftpd to authenticate using a MySQL server.
This module will read client information from a supplied
table/database within MySQL.

%description authlibmysql -l pl.UTF-8
Ten moduł pozwala muddleftpd uwierzytelniać użytkowników przy użyciu
serwera MySQL. Moduł czyta informacje o kliencie z podanej tabeli/bazy
MySQL.

%package authlibsmb
Summary:	SMB authentication library for muddleftpd
Summary(pl.UTF-8):	Biblioteka do uwierzytelniania SMB dla muddleftpd
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description authlibsmb
This module allows muddleftpd to authenticate using a SMB server.

%description authlibsmb -l pl.UTF-8
Ten moduł pozwala muddleftpd uwierzytelniać użytkowników korzystając z
serwera SMB.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__perl} -pi -e 's/^(CFLAGS=.*)/$1 -fPIC/' modules/auth/*/Makefile.in

%build
%configure \
	MYSQL_LIB_DIR=%{_libdir} \
	--with-authmysql \
	--with-authmud

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir},/var/log} \
	$RPM_BUILD_ROOT/etc/{pam.d,logrotate.d,rc.d/init.d,sysconfig,security} \
	$RPM_BUILD_ROOT/home/services/ftp/{pub,upload} \
	$RPM_BUILD_ROOT%{_libdir}/%{name}

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	INFODIR=$RPM_BUILD_ROOT%{_infodir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}/%{name}

# documentation of modules
mv -f modules/auth/authlibmud/README modules/auth/authlibmud/README.authlibmud
mv -f modules/auth/authlibmysql/README modules/auth/authlibmysql/README.authlibmysql
mv -f modules/auth/authlibsmb/README modules/auth/authlibsmb/README.authlibsmb

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
%service muddleftpd restart "muddleftpd daemon"

%preun
if [ "$1" = "0" ]; then
	%service muddleftpd stop
	/sbin/chkconfig --del muddleftpd
fi

%postun	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO doc/*.txt examples
%attr(750,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/muddleftpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.ftp
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/*
%attr(640,root,root) %ghost /var/log/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %dir /home/services/ftp
%attr(755,root,root) %dir /home/services/ftp/pub
%attr(700,root,ftp) %verify(not mode) %dir /home/services/ftp/upload
%{_mandir}/man1/*
%{_infodir}/*.info*

%files authlibmud
%defattr(644,root,root,755)
%doc modules/auth/authlibmud/README.authlibmud
%attr(755,root,root) %{_libdir}/%{name}/libauthmud.so

%files authlibmysql
%defattr(644,root,root,755)
%doc modules/auth/authlibmysql/README.authlibmysql
%attr(755,root,root) %{_libdir}/%{name}/libauthmysql.so

%files authlibsmb
%defattr(644,root,root,755)
%doc modules/auth/authlibsmb/README.authlibsmb
%attr(755,root,root) %{_libdir}/%{name}/libauthsmb.so
