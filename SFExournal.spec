#
# spec file for package SFExournal
#
# includes module: xournal
#

%include Solaris.inc
%define srcname xournal

Name:		SFExournal
Summary:	Note-taking and sketching application
URL:		http://xournal.sourceforge.net
Vendor:		Dennis Auroux
Version:	0.4.5
License:	GPL
Source:		http://downloads.sourceforge.net/%{srcname}/%{srcname}-%{version}.tar.gz
Patch:		xournal-01-inline.diff

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: gnu-make
BuildRequires: autoconf
Requires: gtk2
Requires: libgnomecanvas
Requires: glib2

%description
Xournal is an application for notetaking, sketching, keeping a journal using a
stylus. It is free software (GNU GPL) and runs on Linux (recent distributions)
and other GTK+/Gnome platforms. It is similar to Microsoft Windows Journal or to
other alternatives such as Jarnal, Gournal, and NoteLab.

%prep
%setup -q -n %srcname-%version
%patch -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi
export CFLAGS="%optflags"
export LIBS=-lz

./configure --prefix=%_prefix

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT
gmake desktop-install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/xournal
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/locale
%_datadir/locale/*
%_datadir/%srcname
%dir %attr (-, root, root) %_datadir/mime
%dir %attr (-, root, root) %_datadir/mime/packages
%_datadir/mime/packages/%srcname.xml
%dir %attr (-, root, other) %_datadir/icons
%_datadir/icons/hicolor/scalable
%dir %attr (-, root, root) %_datadir/mimelnk
%dir %attr (-, root, root) %_datadir/mimelnk/application
%_datadir/mimelnk/application/x-xoj.desktop
%dir %attr (-, root, other) %_datadir/applications
%_datadir/applications/xournal.desktop

%changelog
* Tue Oct 12 2010 - Alex Viskovatoff
- Initial spec
