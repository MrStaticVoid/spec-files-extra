#
# spec file for package SFEnodejs
#
# includes module(s): nodejs
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

Summary:	Asynchronous JavaScript Engine  
Name:		SFEnodejs  
Version:	0.4.9
License:	BSD  
Group:		Libraries  
URL:		http://nodejs.org/  
Source:		http://nodejs.org/dist/node-v%{version}.tar.gz  
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

BuildRequires:	SFEc-ares-devel
Requires:	SFEc-ares
Requires:	SUNWgccruntime

%description  
Node's goal is to provide an easy way to build scalable network  
programs. In the above example, the two second delay does not prevent  
the server from handling new requests. Node tells the operating system  
(through epoll, kqueue, /dev/poll, or select) that it should be  
notified when the 2 seconds are up or if a new connection is made --  
then it goes to sleep. If someone new connects, then it executes the  
callback, if the timeout expires, it executes the inner callback. Each  
connection is only a small heap allocation.  

%package devel  
Summary:	Development headers for nodejs  
Group:		Development/Libraries  

%description devel  
Development headers for nodejs.  

%prep  
%setup -q -n node-v%{version}  

%build  
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix} \
	--shared-cares

make -j$CPUS

%install  
rm -rf $RPM_BUILD_ROOT  
make install DESTDIR=$RPM_BUILD_ROOT

%clean  
rm -rf $RPM_BUILD_ROOT  
  
%files  
%defattr(-, root, bin)
%doc AUTHORS ChangeLog LICENSE
%{_bindir}
%{_libdir}/node
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_mandir}

%files devel  
%defattr(-, root, bin)  
%{_bindir}/node-waf
%{_includedir}/node  
%{_libdir}/node/wafadmin/  
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog  
* Thu Jun 30 2011 - Milan Jurik
- bump to 0.4.9
* Thu Mar 24 2011 - Thomas Wagner
- bump to 0.4.3
* Sat Mar 05 2011 - Milan Jurik
- bump to 0.4.2, use internal libev
* Wed Jan 05 2011 - Milan Jurik
- bump to 0.2.6
* Sun Nov 28 2010 - Milan Jurik
- bump to 0.2.5
* Fri Nov 12 2010 - Milan Jurik
- bump to 0.2.4
* Sat Oct 16 2010 - Milan Jurik
- bump to 0.2.3
* Thu Sep 07 2010 - Milan Jurik
- initial spec
