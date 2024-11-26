Name:           AADT
Version:        2.0.11.1
Release:        1%{?dist}
Summary:        Active Directoy Tool for creating and managing Active Directory users
License: GPLv3+
URL: http://github.com/BradHeff
Source0: %{name}-%{version}.tar.gz

BuildRequires: python3

%description
Active Directory tool to manage users

%install
mkdir -p %{buildroot}/usr/local/bin/
mkdir -p %{buildroot}/usr/share/pixmaps/
mkdir -p %{buildroot}/usr/share/applications/
mkdir -p %{buildroot}/usr/share/Arxis_AD_Tool/



cp %{_topdir}/BUILD/AADT/AADT %{buildroot}/usr/local/bin/AADT
cp %{_topdir}/BUILD/AADT/Arxis_AD_Tool.desktop %{buildroot}/usr/share/applications/Arxis_AD_Tool.desktop
cp %{_topdir}/BUILD/AADT/Arxis.png %{buildroot}/usr/share/pixmaps/Arxis.png
cp %{_topdir}/BUILD/AADT/.keep %{buildroot}/usr/share/Arxis_AD_Tool/.keep

%files

/usr/local/bin/AADT
/usr/share/applications/Arxis_AD_Tool.desktop
/usr/share/Arxis_AD_Tool/.keep
/usr/share/pixmaps/Arxis.png


%changelog
* Mon Nov 25 2024 Brad Heffernan <brad.heffernan83@outlook.com>
- 
