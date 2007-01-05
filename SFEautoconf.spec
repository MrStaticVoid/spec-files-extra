#
# spec file for package SFEautoconf
#
# includes module(s): GNU autoconf
#
%include Solaris.inc

Name:                    SFEautoconf
Summary:                 GNU autoconf - scripts and macros for configuring source code packages
Version:                 2.61
Source:			 http://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEm4

%prep
%setup -q -n autoconf-%version

%build
export PATH=/usr/bin:$PATH
export M4=/usr/bin/m4
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix}			\
	    --libexecdir=%{_libexecdir}         \
	    --mandir=%{_mandir}                 \
	    --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info

# Note: do not try to use parallel build, it will break with broken deps
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/autoconf
%{_datadir}/info
%dir %attr (0755, root, root) %{_datadir}/emacs
%dir %attr (0755, root, root) %{_datadir}/emacs/site-lisp
%{_datadir}/emacs/site-lisp/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Fri Jan 05 2007 - daymobrew@users.sourceforge.net
- Bump to 2.61.
* Wed Sep  6 2006 - laca@Sun.com
- disable parallel build as it breaks the build
* Sun Jan 18 2006 - laca@sun.com
- rename to SFEgawk; update summary
- remove -share pkg
- make /usr/gnu/bin/awk a symlink to /usr/bin/gawk
* Thu Apr  6 2006 - damien.carbery@sun.com
- Move Build/Requires to be listed under base package to be useful.
* Sun Dec  4 2005 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec
