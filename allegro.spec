%define major	4.4
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d
%define _disable_lto 1

Name:		allegro
Version:	4.4.2
Release:	14
Summary:	Game programming library
License:	Public Domain
Group:		System/Libraries
URL:		http://alleg.sourceforge.net/
Source0:	http://downloads.sourceforge.net/alleg/allegro/%{name}-%{version}.tar.gz
# See http://liballeg.org/digmid.html
# For allegro 4.x, apparently we can't use SF2 files, so can't share
# with timidity
Source1:	http://www.eglebbk.dds.nl/program/download/digmid.dat
Patch0:		allegro-4.4.2-doc-install.patch
# build seems to fail when username is build, workaround it
Patch1:		allegro-4.4.2-userbuild.patch
Patch2:		allegro-4.2.2-gcc43.patch
Patch4:		allegro-4.4.0.1-format_not_a_string_literal_and_no_format_arguments.patch
Patch5:		allegro-4.4.2-fix_get_value_gcc_5.patch

BuildRequires:	cmake
BuildRequires:	texinfo
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(audiofile)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(xxf86dga)
%ifarch %ix86
BuildRequires:	svgalib-devel
%endif

%description
Allegro is a library of functions for use in computer games

%package -n	%{libname}
Summary:	Game programming library
Group:		System/Libraries
Requires:	%{name} >= %{version}

%description -n	%{libname}
Allegro is a library of functions for use in computer games

%package -n	%{devname}
Summary:	Game programming library
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
Allegro is a library of functions for use in computer games.
This package contains files needed to build programs using Allegro.

%package jack-plugin
Summary:	Allegro JACK (Jack Audio Connection Kit) plugin
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description jack-plugin
This package contains a plugin for Allegro which enables Allegro to playback
sound through JACK (Jack Audio Connection Kit).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch4 -p0
%patch5 -p1

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
%makeinstall_std -C build
install -d -m 755 %{buildroot}%{_mandir}/man3
install -D -m 644 build/docs/man/*3* %{buildroot}%{_mandir}/man3
install -D -m 644 allegro.cfg %{buildroot}%{_sysconfdir}/allegrorc
install -d -m 755 %{buildroot}%{_datadir}/allegro
install -D -m 644 keyboard.dat language.dat %{buildroot}%{_datadir}/allegro
install -D -m 644 misc/allegro.m4 %{buildroot}%{_datadir}/aclocal/allegro.m4

rm -f %{buildroot}%{_libdir}/*.a

cd %{buildroot}%{_datadir}/allegro
cp %{SOURCE1} patches.dat.bz2
bunzip2 patches.dat.bz2
sed -i -e 's,patches =,patches = %{_datadir}/allegro/patches.dat,' %{buildroot}%{_sysconfdir}/allegrorc

%files
%doc %{_docdir}/%{name}
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
%exclude %{_libdir}/allegro/*/alleg-jack.so
%config(noreplace) %{_sysconfdir}/allegrorc

%files -n %{libname}
%{_libdir}/liballeg.so.%{major}*

%files -n %{devname}
%doc docs/txt/abi.txt docs/txt/ahack.txt docs/txt/allegro.txt
%doc docs/txt/const.txt docs/txt/faq.txt docs/txt/help.txt
%doc docs/html
%doc demos examples setup
%{_bindir}/%{name}-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/allegro.m4
%{_includedir}/*.h
%{_includedir}/allegro
%{_includedir}/allegrogl
%{_mandir}/man3/*3*
%{_infodir}/allegro.info*

%files jack-plugin
%{_libdir}/%{name}/*/alleg-jack.so

