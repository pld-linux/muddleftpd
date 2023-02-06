Summary:	muddleftpd - FTP daemon
Summary(pl.UTF-8):	muddleftpd - serwer FTP
Name:		muddleftpd
Version:	1.3.13.1
Release:	10
License:	GPL v2+
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
Patch3:		%{name}-no-common.patch
URL:		http://www.nongnu.org/muddleftpd/
BuildRequires:	mysql-devel
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	texinfo
Requires(post,preun):	/sbin/chkconfig
Requires:	logrotate
Requires:	pam >= 0.79.0
Requires:	rc-scripts
Provides:	ftpserver
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
%patch3 -p1

%{__sed} -i -e '/^CFLAGS=/ s/$/ -fPIC/' modules/auth/*/Makefile.in
%{__sed} -i -e '3i CC=@CC@' modules/auth/authlibsmb/smbval/Makefile.in

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
%{__mv} modules/auth/authlibmud/README modules/auth/authlibmud/README.authlibmud
%{__mv} modules/auth/authlibmysql/README modules/auth/authlibmysql/README.authlibmysql
%{__mv} modules/auth/authlibsmb/README modules/auth/authlibsmb/README.authlibsmb

%{__mv} $RPM_BUILD_ROOT%{_sbindir}/ftpwho $RPM_BUILD_ROOT%{_bindir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/ftp
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/muddleftpd
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/muddleftpd
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/muddleftpd
cp -p %{SOURCE6} $RPM_BUILD_ROOT%{_mandir}/man1/mudpasswd.1

touch $RPM_BUILD_ROOT/var/log/muddleftpd
touch $RPM_BUILD_ROOT/etc/security/blacklist.ftp

install src/ratiotool $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/muddleftpd.conf

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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/muddleftpd
%attr(640,root,root) %ghost /var/log/muddleftpd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/ftp
%attr(754,root,root) /etc/rc.d/init.d/muddleftpd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/muddleftpd
%attr(755,root,root) %{_bindir}/ftpwho
%attr(755,root,root) %{_bindir}/ratiotool
%attr(755,root,root) %{_sbindir}/muddleftpd
%attr(755,root,root) %{_sbindir}/mudlogd
%attr(755,root,root) %{_sbindir}/mudpasswd
%dir %{_libdir}/%{name}
%dir /home/services/ftp
%dir /home/services/ftp/pub
%attr(700,root,ftp) %verify(not mode) %dir /home/services/ftp/upload
%{_mandir}/man1/ftpwho.1*
%{_mandir}/man1/muddleftpd.1*
%{_mandir}/man1/mudpasswd.1*
%{_infodir}/muddleftpd.info*

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
