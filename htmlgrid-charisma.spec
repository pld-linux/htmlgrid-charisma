Summary:	Charisma - free, responsive, multiple skin admin template
Name:		htmlgrid-charisma
Version:	1.0.0
Release:	0.5
License:	Apache v2.0
Group:		Applications/WWW
Source0:	https://github.com/usmanhalalit/charisma/archive/master.tar.gz?/charisma.tgz
# Source0-md5:	b0278cac300ee0f6d22c957a124c4b0f
Source1:	apache.conf
Source2:	lighttpd.conf
URL:		http://usman.it/free-responsive-admin-template/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Charisma is a fully featured, free, premium quality, responsive, HTML5
admin template (or backend template) based on Bootstrap from Twitter,
it comes with 9 different themes to suit your style and application
type.

%prep
%setup -qc
mv charisma-master/* .

# samples
rm -r img/gallery

# jquery
rm -v js/jquery{,-1.7.2.min}.js

# jquery-datatables
rm -v js/jquery.dataTables.min.js

# jquery-history
rm -v js/jquery.history.js

# jquery-twitter-bootstrap
rm -vf `grep 2.0.4 {css,js}/bootstrap-* -l | grep -v classic`
rm -v img/glyphicons-halflings*

# jquery-cookie
rm -v js/jquery.cookie.js

# jquery-ui
rm -v js/jquery-ui-1.8.21.custom.min.js
rm -v css/jquery-ui-1.8.21.custom.css
rm -vf img/ui-{bg_,icons_}*

# jquery-uploadify
rm -v js/jquery.uploadify-3.1.min.js
rm -v img/uploadify-cancel.png
rm -v css/uploadify.css

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -a js css img  $RPM_BUILD_ROOT%{_appdir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md license.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%{_appdir}
