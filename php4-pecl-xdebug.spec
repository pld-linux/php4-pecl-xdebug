%define		_modname	xdebug
%define		_status		stable
%define		_sysconfdir	/etc/php4
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
Summary:	%{_modname} - provides functions for functions traces and profiling
Summary(pl.UTF-8):	%{_modname} - funkcje do śledzenia i profilowania funkcji
Name:		php4-pecl-%{_modname}
Version:	2.0.5
Release:	1
License:	BSD style
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	2d87dab7b6c499a80f0961af602d030c
Source1:	%{name}.ini
URL:		http://pecl.php.net/package/xdebug/
BuildRequires:	libedit-devel
BuildRequires:	libtool
BuildRequires:	php4-devel >= 3:4.1.0
BuildRequires:	rpmbuild(macros) >= 1.578
Requires:	%{_sysconfdir}/conf.d
%{?requires_zend_extension}
Conflicts:	ZendOptimizer
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Xdebug extension helps you debugging your script by providing a
lot of valuable debug information. The debug information that Xdebug
can provide includes the following:

- stack and function traces in error messages with:
 - full parameter display for user defined functions
 - function name, file name and line indications
 - support for member functions memory allocation
- protection for infinite recursions

Xdebug also provides:

- profiling information for PHP scripts
- script execution analysis
- capabilities to debug your scripts interactively with a debug client

In PECL status of this package is: %{_status}.

%description -l pl.UTF-8
Rozszerzenie Xdebug pomaga przy odpluskwianiu skryptu dostarczając
dużo wartościowych informacji. Informacje przydatne do śledzenia,
które może zapewnić Xdebug, obejmują:

- śledzenie stosu i funkcji w komunikatach błędów wraz z:
 - pełnym wyświetlaniem parametrów dla funkcji zdefiniowanych przez
   użytkownika
 - nazwami funkcji, nazwami plików i numerami linii
 - obsługą metod klas
- przydzielanie pamięci
- zabezpieczenie przed nieskończoną rekurencją

Xdebug dostarcza także:

- informacje do profilowania skryptów PHP
- analizę wywołań skryptu
- możliwość śledzenia skryptów interaktywnie przy pomocy klienta
  odpluskwiacza

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
chmod +x %{_modname}-%{version}/debugclient/configure
cp %{SOURCE1} %{_modname}.ini
sed -e 's#^;zend_extension.*#zend_extension%{?zend_zts}=%{extensionsdir}/%{_modname}.so#' -i %{_modname}.ini

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}
cd debugclient
#rm -f *.m4
#install /usr/share/automake/{config.*,depcomp} .
#%{__libtoolize}
#%{__aclocal}
#%{__autoconf}
%configure \
	--with-libedit
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-*/debugclient/debugclient $RPM_BUILD_ROOT%{_bindir}/%{_modname}-debugclient
install %{_modname}-*/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
install %{_modname}.ini $RPM_BUILD_ROOT%{_sysconfdir}/conf.d

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-*/{README,NEWS,Changelog,CREDITS,xt.vim}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
%attr(755,root,root) %{_bindir}/*
