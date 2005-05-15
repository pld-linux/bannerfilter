# TODO:
# - separate package with www-files
%include	/usr/lib/rpm/macros.perl
Summary:	A redirect script for the Squid proxy to block ad banners
Summary(pl):	Skrypt dla Squida przekierowuj±cy w celu blokowania bannerów reklamowych
Name:		bannerfilter
Version:	1.31
Release:	1
Epoch:		1
License:	GPL v2
Group:		Applications/System
Source0:	http://phroggy.com/files/unix/%{name}-%{version}.tar.gz
# Source0-md5:	329a8a6e2b04b21a6f77a365e62e0881
Source1:	%{name}.cron
Patch0:		%{name}-conf.patch
URL:		http://phroggy.com/bannerfilter/
BuildRequires:	rpm-perlprov >= 3.0.3-18
Requires:	squid
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_http_dir	/home/services/httpd/html/bannerfilter

%description
BannerFilter is a redirect script for the Squid proxy server, designed
to block advertising banners on the Web. Unlike most other solutions,
it also automatically closes popup windows.

%description -l pl
BannerFilter to skrypt przekierowuj±cy dla serwera proxy Squid,
przeznaczony do blokowania bannerów reklamowych na WWW. W
przeciwieñstwie do innych rozwi±zañ, dodatkowo automatycznie zamyka
wyskakuj±ce okienka.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/squid/%{name},%{_sysconfdir}/cron.daily/,%{_sbindir},%{_http_dir}}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily/bannerfilter
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
%attr(740,root,root) /etc/cron.daily/bannerfilter
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/squid/*.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/squid/%{name}/*.data
%attr(750,root,squid) %dir %{_sysconfdir}/squid/%{name}
%{_http_dir}
