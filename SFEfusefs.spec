#
#
# spec file for package SFEfusefs
#
# includes module(s): fusefs
#
%include Solaris.inc

%define src_name fusefs

%define usr_kernel /usr/kernel
%define drv_base %{usr_kernel}/drv

Name:		SFEfusefs
Summary:	File system in User Space
Version:	2.8.5
URL:		http://sourceforge.net/projects/fuse/files/fuse-2.X/
Source:		%{src_url}/%{version}/fuse-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SUNWonbld

%description
FUSE stands for 'File system in User Space'. It provides a simple
interface to allow implementation of a fully functional file system
in user-space.  FUSE originates from the Linux community and is
included in the Linux kernel (2.6.14+).

%prep
%setup -q -n %{src_name}

%build
export PATH=/opt/onbld/bin/`uname -p`:$PATH
cd kernel
/usr/ccs/bin/make

%install
rm -rf $RPM_BUILD_ROOT
cd kernel
/usr/ccs/bin/make install

cp -r proto/ $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
( retval=0; 
  /usr/sbin/add_drv -m 'fuse 0666 root sys' fuse || retval=1;
  [ "$retval" = 0 ] && ln -s /devices/pseudo/fuse@0:fuse /dev/fuse || retval=1;
  exit $retval
)

%preun
( retval=0;
  /usr/sbin/rem_drv fuse || retval=1;
  [ "$retval" = 0 ] && rm /dev/fuse || retval=1;
  exit $retval
)

%actions
driver name=fuse

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{usr_kernel}
%dir %attr (0755, root, sys) %{drv_base}
%{drv_base}/fuse
%{drv_base}/fuse.conf
%ifarch amd64 sparcv9
%dir %attr (0755, root, sys) %{drv_base}/%{_arch64}
%{drv_base}/%{_arch64}/fuse
%endif

%changelog
* Mon Jun 06 2011 - Ken Mays <kmays2000@igmail.com>
- Bumped to 2.8.5
* Sat Jun 19 2010 - Milan Jurik
- Initial spec
