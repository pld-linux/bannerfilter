# TODO:
# - separate package with www-files
# - add cron-job file to update
%include	/usr/lib/rpm/macros.perl
Summary:	A redirect script for the Squid proxy to block ad banners
Name:		bannerfilter
Version:	1.21
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://phroggy.com/files/unix/%{name}-%{version}.tar.gz
Patch0:		%{name}-conf.patch
URL:		http://phroggy.com/bannerfilter/
BuildArch:	noarch
BuildRequires:	rpm-perlprov >= 3.0.3-18
Requires:	squid
%requires_eq	perl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_http_dir	/home/services/httpd/html/bannerfilter

%description
BannerFilter is a redirect script for the Squid proxy server, designed
to block advertising banners on the Web. Unlike most other solutions,
it also automatically closes popup windows.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/squid/%{name},%{_sbindir},%{_http_dir}}

install bannerfilter.conf $RPM_BUILD_ROOT%{_sysconfdir}/squid
install redirector.pl $RPM_BUILD_ROOT%{_sbindir}/redirector
install update.sh $RPM_BUILD_ROOT%{_sbindir}/%{name}-update
install www/* $RPM_BUILD_ROOT%{_http_dir}
install *.data $RPM_BUILD_ROOT%{_sysconfdir}/squid/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "Add to your squid config following line:"
echo "redirect_program %{_sbindir}/redirector"

%files
%defattr(644,root,root,755)
%doc CHANGES README TODO
%attr(755,root,root) %{_sbindir}/redirector
%attr(755,root,root) %{_sbindir}/%{name}-update
%config(noreplace)  %verify(not size mtime md5) %{_sysconfdir}/squid/*.conf
%config(noreplace)  %verify(not size mtime md5) %{_sysconfdir}/squid/%{name}/*.data
%attr(750,root,squid) %dir %{_sysconfdir}/squid/%{name}
%{_http_dir}/*
