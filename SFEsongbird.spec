#
# spec file for package SFEsongbird
#
# includes module(s): songbird
#
# Owner: alfred
#

%include Solaris.inc

# use --with-debug to enable debug build.
# default: non-debug build
%define with_debug %{?_with_debug:1}%{?!_with_debug:0}

# use --without-vendor-binary to build your own XULRunner/zlib/taglib.
# default: build with vendor binary
%define without_vendor_binary %{?_without_vendor_binary:1}%{?!_without_vendor_binary:0}

%if %with_debug
%define build_type debug
%else
%define build_type release
%endif

Name:          SFEsongbird
Summary:       The desktop media player mashed-up with the Web.
Version:       0.5
Source:        http://releases.mozilla.com/sun/songbird-%{version}-solaris-patched.tar.bz2
%if %without_vendor_binary
Source1:       http://releases.mozilla.com/sun/xulrunner-20080211-for-songbird-05.tar.bz2
%else
%if %with_debug
Source1:       http://releases.mozilla.com/sun/solaris-vendor-binaries/songbird-vendor-binary-solaris-i386-20080211-for-05-debug.tar.bz2
%else
Source1:       http://releases.mozilla.com/sun/solaris-vendor-binaries/songbird-vendor-binary-solaris-i386-20080211-for-05.tar.bz2
%endif
%endif
URL:           http://www.songbirdnest.com/
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWbzip
BuildRequires: SUNWgtar

%description
Songbird provides a public playground for Web media mash-ups by providing developers with both desktop and Web APIs, developer resources and fostering Open Web media standards.

%prep
%setup -q -n %name-%version -c -a1
%if %without_vendor_binary
%else
mv solaris-i386 songbird%version/dependencies/
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif

%if %without_vendor_binary
# Build the vendor libraries(zlib, taglib)
cd songbird%version/dependencies/vendor/zlib
./songbird_zlib_make.sh
cd ../taglib/
./songbird_taglib_make.sh
cd ../../../../mozilla
%endif

export LDFLAGS="-z ignore -L%{_libdir} -L/usr/sfw/lib -R'\$\$ORIGIN:\$\$ORIGIN/..' -R%{_libdir}/mps"
export CFLAGS="-xlibmil"
export CXXFLAGS="-norunpath -xlibmil -xlibmopt -features=tmplife -lCrun -lCstd"
%if %with_debug
%else
%ifarch sparc
export CFLAGS="$CFLAGS -xO5"
export CXXFLAGS="$CXXFLAGS -xO5"
%else
export CFLAGS="$CFLAGS -xO4"
export CXXFLAGS="$CXXFLAGS -xO4"
%endif
%endif

%if %without_vendor_binary
# Build XULRunner
cat << "EOF" > .mozconfig
MOZILLA_OFFICIAL=1
export MOZILLA_OFFICIAL

BUILD_OFFICIAL=1
export BUILD_OFFICIAL

mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/compiled/xulrunner
ac_add_options --prefix=%{_prefix}
ac_add_options --libdir=%{_libdir}
ac_add_options --mandir=%{_mandir}
ac_add_options --enable-application=xulrunner
ac_add_options --with-xulrunner-stub-name=songbird
%if %with_debug
ac_add_options --enable-debug
ac_add_options --disable-optimize
%else
ac_add_options --enable-optimize
ac_add_options --disable-debug
%endif
ac_add_options --disable-tests
ac_add_options --disable-auto-deps
ac_add_options --disable-crashreporter
ac_add_options --disable-javaxpcom
ac_add_options --disable-installer
ac_add_options --enable-extensions=default,inspector,venkman
ac_add_options --disable-dbus

mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options MOZ_DEBUG_SYMBOLS=1
EOF

mkdir -p compiled/xulrunner

make -f client.mk build_all

# Package XULRunner
cd ../songbird%version

mkdir -p dependencies/solaris-i386/mozilla/%build_type
mkdir -p dependencies/solaris-i386/xulrunner/%build_type

cd tools/scripts
./make-mozilla-sdk.sh ../../../mozilla ../../../mozilla/compiled/xulrunner ../../dependencies/solaris-i386/mozilla/%build_type
./make-xulrunner-tarball.sh ../../../mozilla/compiled/xulrunner/dist/bin ../../dependencies/solaris-i386/xulrunner/%build_type xulrunner.tar.gz

cd ../../
%else
cd songbird%version
%endif

# Build Songbird
%if %with_debug
%else
export SB_ENABLE_INSTALLER=1
export SONGBIRD_OFFICIAL=1
%endif

export SB_ENABLE_JARS=1
export LD=CC
export PATH=/usr/gnu/bin:$PATH

%if %with_debug
make -f songbird.mk debug
%else
make -f songbird.mk
%endif

%install
/bin/rm -rf $RPM_BUILD_ROOT

cd %{_builddir}/%name-%version/songbird%version/compiled
mkdir -p $RPM_BUILD_ROOT/usr/lib
mkdir -p $RPM_BUILD_ROOT/usr/bin
cp -R dist $RPM_BUILD_ROOT/usr/lib/songbird-%version
touch $RPM_BUILD_ROOT/usr/lib/songbird-%version/extensions/rubberducky@songbirdnest.com/chrome.manifest
touch $RPM_BUILD_ROOT/usr/lib/songbird-%version/extensions/basic-layouts@songbirdnest.com/chrome.manifest
cd $RPM_BUILD_ROOT/usr/bin
ln -s ../lib/songbird-%version/songbird .

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/songbird
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/songbird-%{version}

%changelog
* Sun Apr 13 2008 - alfred.peng@sun.com
- add option --without-vendor-binary. use the vendor binary by default
  to speed the build process.
* Thu Apr 10 2008 - alfred.peng@sun.com
- created
