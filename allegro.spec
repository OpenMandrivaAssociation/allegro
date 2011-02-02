%define name	allegro
%define version	4.4.1.1
%define alt_version 4.4.1
%define rel	3
%define beta	0
%if %{beta}
%define	release	%mkrel 0.beta%{beta}.%{rel}
%else
%define	release	%mkrel %{rel}
%endif

%define libname		%mklibname %{name} %{major}
%define	develname	%mklibname %{name} -d
%define	testlib		%mklibname allegro-testing %{major}
%define major		4.4

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Game programming library
%if %{beta}
Source0:	http://downloads.sourceforge.net/alleg/allegro/%{name}-%{version}-beta%{beta}.tar.gz
%else
Source0:	http://downloads.sourceforge.net/alleg/allegro/%{name}-%{version}.tar.gz
%endif
Patch2:         allegro-4.2.2-gcc43.patch
Patch4:		allegro-4.4.0.1-format_not_a_string_literal_and_no_format_arguments.patch
License:	Public Domain
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://alleg.sourceforge.net/
BuildRequires:	audiofile-devel
BuildRequires:	libx11-devel
BuildRequires:	libxcursor-devel
Buildrequires:	libxext-devel
BuildRequires:	libxpm-devel
BuildRequires:	libxxf86vm-devel
BuildRequires:	libxxf86dga-devel
BuildRequires:	jackit-devel
BuildRequires:	libpng-devel
BuildRequires:	libogg-devel
BuildRequires:	mesaglu-devel
BuildRequires:	texinfo
BuildRequires:	cmake
%ifarch %ix86
BuildRequires:	svgalib-devel
%endif
Obsoletes:	allegro-testing
Provides:	allegro-testing = %{version}-%{release}
Obsoletes:	allegro-arts-plugin

%description
Allegro is a library of functions for use in computer games

%package -n	%{libname}
Summary:	Game programming library
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}
Provides:	%{testlib} = %{version}-%{release}
Obsoletes:	%{testlib}
Suggests:	%{name} >= %{version}

%description -n	%{libname}
Allegro is a library of functions for use in computer games

%package -n	%{develname}
Summary:	Game programming library
Group:		Development/C++
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{testlib}-devel = %{version}-%{release}
Obsoletes:	allegro-devel %{testlib}-devel
Obsoletes:	%{mklibname allegro 4.2 -d}

%description -n	%{develname}
Allegro is a library of functions for use in computer games.
This package contains files needed to build programs using Allegro.

%package jack-plugin
Summary:        Allegro JACK (Jack Audio Connection Kit) plugin
Group:          System/Libraries
Requires:       %{name} = %{version}-%{release}

%description jack-plugin
This package contains a plugin for Allegro which enables Allegro to playback
sound through JACK (Jack Audio Connection Kit).

%prep
%setup -q
%patch2 -p1
%patch4 -p0

iconv -f iso-8859-1 -t utf-8 docs/src/allegro._tx > docs/src/allegro._tx.tmp
mv docs/src/allegro._tx.tmp docs/src/allegro._tx

%build
%define _disable_ld_no_undefined 1
%ifnarch ix86
export CFLAGS="%{optflags} -fPIC"
%endif

%cmake
%make
find demos examples setup -type f -perm +111 -print | xargs rm -rf


%install
rm -rf %{buildroot}
%make -C build DESTDIR=%buildroot install
install -d -m 755 %{buildroot}%{_mandir}/man3
install -D -m 644 build/docs/man/*3* %{buildroot}%{_mandir}/man3
install -d -m 755 %{buildroot}%{_infodir}
mv %{buildroot}/usr/info/*.info %{buildroot}%{_infodir}
install -D -m 644 allegro.cfg %{buildroot}%{_sysconfdir}/allegrorc
install -d -m 755 %{buildroot}%{_datadir}/allegro
install -D -m 644 keyboard.dat language.dat %{buildroot}%{_datadir}/allegro

rm -rf %{buildroot}/usr/doc

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post -n %{develname}
%_install_info %{name}.info

%preun -n %{develname}
%_remove_install_info %{name}.info

%files
%defattr(-,root,root)
%doc AUTHORS CHANGES THANKS
%doc readme.txt docs/build/unix.txt docs/build/linux.txt
%{_bindir}/colormap
%{_bindir}/dat
%{_bindir}/dat2c
%{_bindir}/dat2s
%{_bindir}/exedat
%{_bindir}/grabber
%{_bindir}/pack
%{_bindir}/pat2dat
%{_bindir}/rgbmap
%{_bindir}/textconv
%{_datadir}/allegro
%{_libdir}/%{name}
##%exclude %{_libdir}/allegro/%{alt_version}/alleg-esddigi.so
%exclude %{_libdir}/allegro/%{alt_version}/alleg-jack.so
%config(noreplace) %{_sysconfdir}/allegrorc

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc *.txt AUTHORS CHANGES THANKS
%doc docs/txt/abi.txt docs/txt/ahack.txt docs/txt/allegro.txt
%doc docs/txt/const.txt docs/txt/faq.txt docs/txt/help.txt
%doc docs/html
%doc demos examples setup
%{_bindir}/%{name}-config
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h
%{_includedir}/allegro/*
%{_includedir}/allegrogl/*
%{_mandir}/man3/*3*
%{_infodir}/allegro.info*

%files jack-plugin
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{alt_version}/alleg-jack.so
