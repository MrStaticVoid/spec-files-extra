#
# spec file for package faac
#
# includes module(s): faac
#

Summary:	Reference encoder and encoding library for MPEG2/4 AAC
Name:		SFEfaac
Version:	1.28
License:	LGPLv2+
Group:		Applications/Multimedia
URL:		http://www.audiocoding.com/
Source:		%{sf_download}/faac/faac-src/faac-%{version}.tar.gz
Patch1:		faac-01-mp4v2.diff
Patch2:		faac-02-wall.diff
Patch3:		faac-03-stdc.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n faac-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%{optflags} -I/usr/include/mp4v2"
export CXXFLAGS="%{cxx_optflags} -I/usr/include/mp4v2"
export LDFLAGS="-lmp4v2 -lm"

sh bootstrap

./configure --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --disable-static \
    --with-mp4v2

make -j$CPUS


%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Jun 21 2012 - James Lee <jlee@thestaticvoid.com>
- Linking with libmp4v2 requires libCrun 
* Mon Oct 17 2011 - Milan Jurik
- revert previous change to unbreak build
* Sat Aug 13 2011 - Thomas Wagner
- fix build by:
- use /usr/bin/libtoolize and not new SFE version from /usr/gnu/bin/
- use CC/CXX /usr/gnu/bin/gcc g++
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Thu Jun 18 2010 - Milan Jurik
- Initial version
