%define name	allegro
%define version	4.2.2
%define rel	1
%define beta	0
%if %{beta}
%define	release	%mkrel 0.beta%{beta}.%{rel}
%else
%define	release	%mkrel %{rel}
%endif

%define libname		%mklibname %{name} %{major}
%define	develname	%mklibname %{name} -d
%define	testlib		%mklibname allegro-testing %{major}
%define major		4.2

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Game programming library
%if %{beta}
Source0:	http://sunsite.auc.dk/allegro/%{name}-%{version}-beta%{beta}.tar.gz
%else
Source0:	http://sunsite.auc.dk/allegro/%{name}-%{version}.tar.gz
%endif
License:	Public Domain
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://alleg.sourceforge.net/
BuildRequires:	arts-devel
BuildRequires:	esound-devel
BuildRequires:	audiofile-devel
BuildRequires:	XFree86-devel
BuildRequires:	jackit-devel
BuildRequires:	autoconf
BuildRequires:	texinfo
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

%package -n	%{develname}
Summary:	Game programming library
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{testlib}-devel = %{version}-%{release}
Obsoletes:	allegro-devel %{testlib}-devel
Obsoletes:	%{mklibname allegro 4.2 -d}

%description -n	%{develname}
Allegro is a library of functions for use in computer games.
This package contains files needed to build programs using Allegro.

%package esound-plugin
Summary:        Allegro Enlightened Sound Daemon plugin
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description esound-plugin
This package contains a plugin for Allegro which enables Allegro to playback
sound through the Enlightened Sound Daemon (ESD / esound).

%package arts-plugin
Summary:        Allegro aRts (analog realtime synthesizer) plugin
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description arts-plugin
This package contains a plugin for Allegro which enables Allegro to playback
sound through aRts (analog realtime synthesizer).

%package jack-plugin
Summary:        Allegro JACK (Jack Audio Connection Kit) plugin
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description jack-plugin
This package contains a plugin for Allegro which enables Allegro to playback
sound through JACK (Jack Audio Connection Kit).

%prep
%setup -q
iconv -f iso-8859-1 -t utf-8 docs/src/allegro._tx > docs/src/allegro._tx.tmp
mv docs/src/allegro._tx.tmp docs/src/allegro._tx

%build
%{__autoconf}
%configure2_5x	--enable-shared \
%ifarch %{ix86}
		--enable-pentiumopts \
%endif
		--enable-static
make
#MKDATA_PRELOAD=../../lib/unix/liballeg-%{version}.so DAT=../../tools/dat misc/mkdata.sh
find demo examples setup -type f -perm +111 -print | xargs rm

%install
rm -rf %{buildroot}
%{makeinstall_std} install-man install-info
install -D -m 644 allegro.cfg %{buildroot}%{_sysconfdir}/allegrorc
install -d -m 755 %{buildroot}%{_datadir}/allegro
install -D -m 644 keyboard.dat language.dat %{buildroot}%{_datadir}/allegro

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

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
%exclude %{_libdir}/allegro/%{version}/alleg-esddigi.so
%exclude %{_libdir}/allegro/%{version}/alleg-artsdigi.so
%exclude %{_libdir}/allegro/%{version}/alleg-jackdigi.so
%config(noreplace) %{_sysconfdir}/allegrorc

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so*

%files -n %{develname}
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

%files esound-plugin
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/alleg-esddigi.so

%files arts-plugin
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/alleg-artsdigi.so

%files jack-plugin
%defattr(-,root,root,-)
%{_libdir}/%{name}/%{version}/alleg-jackdigi.so

