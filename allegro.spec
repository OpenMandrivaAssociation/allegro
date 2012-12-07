%define major		4.4
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d
%define testlib		%mklibname allegro-testing %{major}

Name:		allegro
Version:	4.4.2
Release:	2
Summary:	Game programming library
License:	Public Domain
Group:		System/Libraries
URL:		http://alleg.sourceforge.net/
Source0:	http://downloads.sourceforge.net/alleg/allegro/%{name}-%{version}.tar.gz
Patch0:		allegro-4.4.2-doc-install.patch
# build seems to fail when username is build, workaround it
Patch1:		allegro-4.4.2-userbuild.patch
Patch2:		allegro-4.2.2-gcc43.patch
Patch4:		allegro-4.4.0.1-format_not_a_string_literal_and_no_format_arguments.patch
BuildRequires:	pkgconfig(audiofile)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(xxf86dga)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(glu)
BuildRequires:	texinfo
BuildRequires:	cmake
%ifarch %ix86
BuildRequires:	svgalib-devel
%endif
Provides:	allegro-testing = %{version}-%{release}

%description
Allegro is a library of functions for use in computer games

%package -n	%{libname}
Summary:	Game programming library
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}
Provides:	%{testlib} = %{version}-%{release}
Suggests:	%{name} >= %{version}

%description -n	%{libname}
Allegro is a library of functions for use in computer games

%package -n	%{develname}
Summary:	Game programming library
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{testlib}-devel = %{version}-%{release}

%description -n	%{develname}
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
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc docs/txt/abi.txt docs/txt/ahack.txt docs/txt/allegro.txt
%doc docs/txt/const.txt docs/txt/faq.txt docs/txt/help.txt
%doc docs/html
%doc demos examples setup
%{_bindir}/%{name}-config
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h
%{_includedir}/allegro
%{_includedir}/allegrogl
%{_mandir}/man3/*3*
%{_infodir}/allegro.info*

%files jack-plugin
%{_libdir}/%{name}/*/alleg-jack.so


%changelog
* Thu Feb 23 2012 Bernhard Rosenkraenzer <bero@bero.eu> 4.4.2-2
+ Revision: 779900
- Fix directory ownership of /usr/include subdirs

* Sat May 28 2011 Funda Wang <fwang@mandriva.org> 4.4.2-1
+ Revision: 680454
- cleanup spec
- update to new version 4.4.2

* Wed Feb 02 2011 Funda Wang <fwang@mandriva.org> 4.4.1.1-3
+ Revision: 634994
- rebuild
- tighten BR

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 4.4.1.1-2mdv2011.0
+ Revision: 609968
- rebuild

* Thu Mar 18 2010 Emmanuel Andry <eandry@mandriva.org> 4.4.1.1-1mdv2010.1
+ Revision: 525103
- New version 4.4.1.1

* Thu Dec 31 2009 Emmanuel Andry <eandry@mandriva.org> 4.4.0.1-1mdv2010.1
+ Revision: 484572
- New version 4.4.0.1 (backward compatible with 4.2.x)
- rediff P4
- drop esd support (not build, dropped upstream ?)
- use cmake
- update files list

* Fri Dec 25 2009 Jérôme Brenier <incubusss@mandriva.org> 4.2.3-1mdv2010.1
+ Revision: 482185
- bugfix version 4.2.3
- drop P0, P1 and P3 (merged in the new source)
- fix url of sources

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 4.2.2-5mdv2010.0
+ Revision: 436639
- rebuild

* Mon Jan 26 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.2.2-4mdv2009.1
+ Revision: 333582
- compile with -fPIC for x86_64
- Patch4: fix build with -Werror=format-security
- disable arts plugin
- use %%define _disable_ld_no_undefined, --disable-asm on x86_64 has same effect

  + Emmanuel Andry <eandry@mandriva.org>
    - fix autoconf with P1 from gentoo
    - fix gcc43 build with P2 and P3 from fedora

  + Götz Waschk <waschk@mandriva.org>
    - fix devel package group

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 11 2008 Frederic Crozat <fcrozat@mandriva.com> 4.2.2-3mdv2008.1
+ Revision: 186319
- lib package suggests main package, to get alsa plugin (Mdv bug #38436)

* Tue Jan 29 2008 Colin Guthrie <cguthrie@mandriva.org> 4.2.2-2mdv2008.1
+ Revision: 159681
- Apply upstream patch to handle unsigned samples in alsa (pulseaudio bug #113)

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Sat Oct 27 2007 Adam Williamson <awilliamson@mandriva.org> 4.2.2-1mdv2008.1
+ Revision: 102464
- whoops, use Mandriva group names for the plugin packages, not Fedora
- buildrequires texinfo
- fix a badly thought out %%if statement on the part of the previous packager, which led to no 'make' command being issued on x86-64...
- move non-library files from lib package to main package (obey lib policy)
- adopt a couple of things from Fedora:
  	+ convert man and info pages to UTF-8
  	+ package esound, arts and jack plugins separately to avoid unnecessary dependencies
- minor clean ups
- new devel policy
- new version 4.2.2
- import allegro


* Wed Jun 28 2006 Lenny Cartier <lenny@mandriva.com> 4.2.0-3mdv2007.0
- rebuild

* Fri Dec  2 2005 Götz Waschk <waschk@mandriva.org> 4.2.0-2mdk
- don't build with svgalib on x86_64

* Wed Nov 09 2005 Guillaume Bedot <littletux@mandriva.org> 4.2.0-0.1mdk
- 4.2 final release !
- dropped gcc4 patch (applied upstream)

* Tue Aug 09 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 4.2.0-0.beta4.1mdk
- as no packages no longer use 4.0, update to new 4.2 and merge with testing package
- build with jack and svgalib support too
- fix requires-on-release
- fix short-circuitting
- change major to 4.2 (wrong use of major in lib?)

* Sat Jul 30 2005 Guillaume Bedot <littletux@mandriva.org> 4.0.3-7mdk
- rebuild for cooker / 2006
- buildrequires on gcc3.3
- Patch0: asm patch from allegro-testing package

* Sat Dec 25 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 4.0.3-6mdk
- rebuild
- cosmetics

* Tue Aug 17 2004 Lenny Cartier <lenny@mandrakesoft.com> 4.0.3-5mdk
- rebuild

* Sat Jul 12 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 4.0.3-4mdk
- rebuild

* Mon Jun 16 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 4.0.3-3mdk
- buildrequires
- cosmetics

* Sun May 04 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 4.0.3-2mdk
- rebuild for rpm 4.2.0
- use %%mklibname for devel package too
- remove commented out configure stuff to satisfy rpmlint
- added man pages to devel package

* Fri Apr 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 4.0.3-1mdk
- 4.0.3 final

* Sat Mar 29 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 4.0.3-0.rc2.1mdk
- 4.0.3-rc2
- enable parallell builds as it works now
- rm -rf buildroot in install stage in stead of prep stage
- use macro for autoconf
- fix the usage of optimize flags
- use %%mklibname macro

* Sat Mar  8 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 4.0.3-0.rc1.1mdk
- 4.0.3-rc1

* Sun Dec 29 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 4.0.3-0.beta1.1mdk
- 4.0.3-beta1
- Fix Provides/Requires
- remove BuildRequires glibc-static

* Sun Dec 01 2002  Lenny Cartier <lenny@mandrakesoft.com> 4.0.2-3mdk
- fix file list

* Wed Jul 10 2002 Lenny Cartier <lenny@mandrakesoft.com> 4.0.2-2mdk
- update buildrequires 

* Mon Jul 08 2002 Lenny Cartier <lenny@mandrakesoft.com> 4.0.2-1mdk
- 4.0.2

* Mon Apr 08 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 4.0.1-2mdk
- let include in non-versioned dir

* Mon Apr 01 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 4.0.1-1mdk
- 4.0.1
- dropped patch
- moved allegro-config to devel package

* Mon Mar 11 2002 Lenny Cartier <lenny@mandrakesoft.com> 4.0.0-4mdk
- regenerate patch from Levi Ramsey to fix allegro.h

* Thu Mar 07 2002 Lenny Cartier <lenny@mandrakesoft.com> 4.0.0-3mdk
- fix(again) file section (thx Yannick Roehlly)

* Wed Jan 30 2002 Lenny Cartier <lenny@mandrakesoft.com>  4.0.0-2mdk
- fix files section

* Mon Dec 17 2001 Lenny Cartier <lenny@mandrakesoft.com>  4.0.0-1mdk
- 4.0.0

* Tue Oct 02 2001 Lenny Cartier <lenny@mandrakesoft.com>  3.9.38-1mdk
- 3.9.38

* Mon May 14 2001 Lenny Cartier <lenny@mandrakesoft.com>  3.9.36-1mdk
- updated to 3.9.36

* Wed Feb 28 2001 Lenny Cartier <lenny@mandrakesoft.com>  3.9.34-1mdk
- updated by Vlatko Kosturjak <kost@linux-mandrake.com> 3.9.34-1mdk
	- support for new version
	- removed patch
- use egcs

* Thu Jan 04 2001 David BAUDENS <baudens@mandrakesoft.com> 3.9.33-3mdk
- ExcludeArch: PPC
- Fix devel description
- Spec clean up

* Thu Jan 04 2001 Lenny Cartier <lenny@mandrakesoft.com> 3.9.33-2mdk
- rebuild

* Wed Sep 27 2000 Pixel <pixel@mandrakesoft.com> 3.9.33-1mdk
- initial spec
