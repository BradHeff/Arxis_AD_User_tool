Name:           AADT
Version:        2.0.11.1
Release:        1%{?dist}
Summary:        Active Directoy Tool for creating and managing Active Directory users
License: GPLv3+
URL: https://github.com/BradHeff/Horizon_AD_User_tool
Source0: %{name}-%{version}.tar.gz

BuildRequires: python3
Requires:      python3, python3-tkinter, python3-pillow-tk, python3-pip


%description
Active Directory tool to manage users

%install
mkdir -p %{buildroot}/usr/local/bin/
mkdir -p %{buildroot}/usr/lib/Arxis_AD_Tool/
mkdir -p %{buildroot}/usr/share/pixmaps/
mkdir -p %{buildroot}/usr/share/applications/
mkdir -p %{buildroot}/usr/share/Arxis_AD_Tool/



cp %{_topdir}/BUILD/AADT/AADT %{buildroot}/usr/local/bin/AADT
cp %{_topdir}/BUILD/AADT/Arxis_AD_Tool.desktop %{buildroot}/usr/share/applications/Arxis_AD_Tool.desktop
cp %{_topdir}/BUILD/AADT/Arxis.png %{buildroot}/usr/share/pixmaps/Arxis.png
cp %{_topdir}/BUILD/AADT/.keep %{buildroot}/usr/share/Arxis_AD_Tool/.keep
cp %{_topdir}/BUILD/AADT/Functions.py %{buildroot}/usr/lib/Arxis_AD_Tool/Functions.py
cp %{_topdir}/BUILD/AADT/Main.py %{buildroot}/usr/lib/Arxis_AD_Tool/Main.py
cp %{_topdir}/BUILD/AADT/Gui.py %{buildroot}/usr/lib/Arxis_AD_Tool/Gui.py
cp %{_topdir}/BUILD/AADT/icon.py %{buildroot}/usr/lib/Arxis_AD_Tool/icon.py


%post
pip3 install --user pillow ttkbootstrap ldap3 flask pyOpenSSL configparser_crypt requests tinyaes tkthread git+https://github.com/psf/black
chmod +x /usr/local/bin/AADT

%files

/usr/local/bin/AADT
/usr/share/applications/Arxis_AD_Tool.desktop
/usr/share/Arxis_AD_Tool/.keep
/usr/lib/Arxis_AD_Tool/icon.py
/usr/lib/Arxis_AD_Tool/Gui.py
/usr/lib/Arxis_AD_Tool/Functions.py
/usr/lib/Arxis_AD_Tool/Main.py
/usr/share/pixmaps/Arxis.png


%changelog
* Mon Nov 25 2024 Brad Heffernan <brad.heffernan83@outlook.com>
- 
