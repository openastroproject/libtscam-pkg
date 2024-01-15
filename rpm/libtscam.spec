%define debug_package %{nil}

Name:           libtscam
Version:        1.55.24239
Release:        0
Summary:        Teleskop Service camera support library
License:	GPLv2+
Prefix:         %{_prefix}
Provides:       libtscam = %{version}-%{release}
Obsoletes:      libtscam < 1.55.24239
Source:         libtscam-%{version}.tar.gz
Patch0:         pkg-config.patch
Patch1:         udev-rules.patch

%description
libtscam is a user-space driver for Teleskop Service astronomy cameras.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libtscam-devel = %{version}-%{release}
Obsoletes:      libtscam-devel < 1.55.24239

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build

sed -e "s!@LIBDIR@!%{_libdir}!g" -e "s!@VERSION@!%{version}!g" < \
    libtscam.pc.in > libtscam.pc

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}/etc/udev/rules.d
mkdir -p %{buildroot}%{_includedir}

case %{_arch} in
  x86_64)
    cp x64/libtscam.bin %{buildroot}%{_libdir}/libtscam.so.%{version}
		cp tscam.h %{buildroot}%{_includedir}
    ;;
  *)
    echo "unknown target architecture %{_arch}"
    exit 1
    ;;
esac

ln -sf %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so.1
cp *.pc %{buildroot}%{_libdir}/pkgconfig
cp 70-ts-cameras.rules %{buildroot}/etc/udev/rules.d

%post
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%postun
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%files
%{_libdir}/*.so.*
%{_sysconfdir}/udev/rules.d/*.rules

%files devel
%{_includedir}/tscam.h
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Jan 6 2024 James Fidell <james@openastroproject.org> - 1.55.24239-0
- Initial RPM release

