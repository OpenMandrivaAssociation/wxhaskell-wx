# The wxhaskell build process has to be split into two steps these
# days, so the previous wxhaslell .src.rpm is now split into two:
# wxhaskell and wxhaskell-wx . It would be better to have
# wxhaskell-core and wxhaskell , but this keeps history better.
# wxhaskell builds the wxcore part. wxhaskell-wx builds the wx part.
# The wx build can't succeed unless the wxcore part has already been
# installed, hence the need for two source packages. -AdamW 2008/08

%define oname	wxhaskell

%define rel	2
%define darcs	20090214
%if %darcs
%define release		%mkrel 0.%{darcs}.%{rel}
%define distname	%{oname}-%{darcs}.tar.lzma
%define dirname		%{oname}
%else
%define release		%mkrel %{rel}
%define distname	%{oname}-src-%{version}.zip
%define dirname		%{oname}-%{version}
%endif

%define ghc_version	%(rpm -q ghc | cut -d- -f2)

Summary:	wxWindows Haskell binding
Name:		%{oname}-wx
Version:	0.11.1
Release: 	%{release}
License:	wxWidgets
Group: 		Development/Other
URL: 		https://wxhaskell.sourceforge.net
Source0: 	http://downloads.sourgeforge.net/%{oname}/%{distname}
BuildRequires:	ghc
BuildRequires:	wxgtku-devel
BuildRequires:	wxhaskell == %{version}
BuildRequires:	haskell-wxcore == %{version}
#BuildRequires:	haskell-macros
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
wxHaskell is a Haskell binding to the portable wxWidgets GUI library.

%package -n haskell-wx
Summary:	Haskell binding for wxGTK2 devel files
Group:		Development/Other
Requires:	haskell-wxcore == %{version}
# for ghc-pkg
Requires(pre):	ghc == %{ghc_version}
Requires(post):	ghc == %{ghc_version}
Obsoletes:	ghc-wxhaskell < %{version}-%{release}
Provides:	ghc-wxhaskell = %{version}-%{release}

%description -n haskell-wx
wxHaskell is a Haskell binding to the portable wxWidgets GUI library.
This package contains the wxhaskell package for ghc.

%define wxdir %{_libdir}/ghc-%{ghc_version}/wx

%prep
%setup -q -n %{dirname}

%build
%if %darcs
chmod 0755 configure
%endif
./configure --hc=ghc-%{ghc_version} --hcpkg=ghc-pkg-%{ghc_version} --libdir=%{wxdir} --with-opengl --wx-config=wx-config-unicode
make wx

%install
rm -rf %{buildroot}
make wx-install-files LIBDIR=%{buildroot}%{wxdir}
cp -p config/wx.pkg %{buildroot}%{wxdir}
sed -i -e "s|\${wxhlibdir}|%{wxdir}|" %{buildroot}%{wxdir}/wx.pkg

# remove object files and generated them at pkg install time
rm %{buildroot}%{wxdir}/wx*.o

# remove wxcore first as we're not building it here
#rm -rf wxcore
#{_cabal_rpm_gen_deps}

%clean
rm -rf %{buildroot}

%post -n haskell-wx
%if %mdkversion < 200900
/sbin/ldconfig
%endif
ghc-pkg-%{ghc_version} update -g %{wxdir}/wx.pkg

%preun -n haskell-wx
if [ "$1" = 0 ]; then
  rm %{wxdir}/wx*.o
  ghc-pkg-%{ghc_version} unregister wx || :
fi

%if %mdkversion < 200900
%postun -n haskell-wx -p /sbin/ldconfig
%endif

%files -n haskell-wx
%defattr(-,root,root,-)
%{wxdir}/imports/Graphics/UI/WX
%{wxdir}/imports/Graphics/UI/WX.hi
%{wxdir}/wx.pkg
%{wxdir}/libwx.a
