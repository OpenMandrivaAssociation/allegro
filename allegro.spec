%define name	allegro
%define version	4.2.0
%define rel	3
%define beta	0
%if %{beta}
%define	release	%mkrel 0.beta%{beta}.%{rel}
%else
%define	release	%mkrel %{rel}
%endif
%define libname	%mklibname %{name} %{major}
%define	libname_devel	%mklibname %{name} %{major} -d
%define	testlib	%mklibname allegro-testing %{major}
%define major	4.2

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Game programming library
%if %{beta}
Source0:	http://sunsite.auc.dk/allegro/%{name}-%{version}-beta%{beta}.tar.bz2
%else
Source0:	http://sunsite.auc.dk/allegro/%{name}-%{version}.tar.bz2
%endif
License:	Public Domain
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://alleg.sourceforge.net/
BuildRequires:	arts-devel esound-devel audiofile-devel XFree86-devel
BuildRequires:	jackit-devel 
%ifarch %ix86
BuildRequires:	svgalib-devel
%endif
Obsoletes:	allegro-testing
Provides:	allegro-testing = %{version}-%{release}

%description
Allegro is a library of functions for use in computer games

%package -n	%{libname}
Summary:	Game programming library
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}
Provides:	%{testlib} = %{version}-%{release}
Obsoletes:	%{testlib}

%description -n	%{libname}
Allegro is a library of functions for use in computer games

%package -n	%{libname_devel}
Summary:	Game programming library
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	allegro-devel %{testlib}-devel = %{version}-%{release}
Obsoletes:	allegro-devel %{testlib}-devel

%description -n	%{libname_devel}
Allegro is a library of functions for use in computer games.
This package contains files needed to build programs using Allegro.

%prep
%setup -q

%build
%{__autoconf}
%configure	--enable-shared \
		--enable-static \
%ifarch %{ix86}
		--enable-pentiumopts
%endif
make
MKDATA_PRELOAD=../../lib/unix/liballeg-%{version}.so DAT=../../tools/dat misc/mkdata.sh
find demo examples setup -type f -perm +111 -print | xargs rm

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std} install-man install-info
install -D -m 644 allegro.cfg %{buildroot}%{_sysconfdir}/allegrorc
install -d -m 755 %{buildroot}%{_datadir}/allegro
install -D -m 644 keyboard.dat language.dat %{buildroot}%{_datadir}/allegro

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libname}-devel
%_install_info %{name}.info

%preun -n %{libname}-devel
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
%config(noreplace) %{_sysconfdir}/allegrorc

%files -n %{libname}
%defattr(-,root,root)
%doc readme.txt
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/%{name}

%files -n %{libname_devel}
%defattr(-,root,root)
%doc readme.txt todo.txt
#docs/txt/* docs/html/* demo/* examples/* setup/*
%doc docs/txt/abi.txt docs/txt/ahack.txt docs/txt/allegro.txt
%doc docs/txt/const.txt docs/txt/faq.txt docs/txt/help.txt
%doc docs/html
%doc demo examples setup
%{_bindir}/%{name}-config
%{_libdir}/*.a
%{_includedir}/*
%{_mandir}/*/*
%{_infodir}/allegro.info*
%{_datadir}/aclocal/allegro.m4

