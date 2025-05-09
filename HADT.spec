Name:           HADT
Version:        2.0.15.1
Release:        1%{?dist}
Summary:        Active Directoy Tool for creating and managing Active Directory users
License: GPLv3+
URL: https://github.com/BradHeff/Horizon_AD_User_tool
Source0: %{name}-%{version}.tar.gz

BuildRequires: python3
Requires:      python3, python3-tkinter, python3-pillow, python3-pillow-tk, python3-pip


%description
Active Directory tool to manage users

%install
mkdir -p %{buildroot}/usr/local/bin/
mkdir -p %{buildroot}/usr/lib/Horizon_AD_Tool/
mkdir -p %{buildroot}/usr/share/pixmaps/
mkdir -p %{buildroot}/usr/share/applications/



cp %{_topdir}/BUILD/HADT/HADT %{buildroot}/usr/local/bin/HADT
cp %{_topdir}/BUILD/HADT/Horizon_AD_Tool.desktop %{buildroot}/usr/share/applications/Horizon_AD_Tool.desktop
cp %{_topdir}/BUILD/HADT/Horizon.png %{buildroot}/usr/share/pixmaps/Horizon.png
cp %{_topdir}/BUILD/HADT/Functions.py %{buildroot}/usr/lib/Horizon_AD_Tool/Functions.py
cp %{_topdir}/BUILD/HADT/Main.py %{buildroot}/usr/lib/Horizon_AD_Tool/Main.py
cp %{_topdir}/BUILD/HADT/Gui.py %{buildroot}/usr/lib/Horizon_AD_Tool/Gui.py
cp %{_topdir}/BUILD/HADT/icon.py %{buildroot}/usr/lib/Horizon_AD_Tool/icon.py
cp %{_topdir}/BUILD/HADT/syncer.json %{buildroot}/usr/lib/Horizon_AD_Tool/syncer.json


%post
pip3 install --user pillow ttkbootstrap ldap3 flask pyOpenSSL configparser_crypt requests tinyaes tkthread git+https://github.com/psf/black
chmod +x /usr/local/bin/HADT

%files

/usr/local/bin/HADT
/usr/share/applications/Horizon_AD_Tool.desktop
/usr/lib/Horizon_AD_Tool/icon.py
/usr/lib/Horizon_AD_Tool/Gui.py
/usr/lib/Horizon_AD_Tool/Functions.py
/usr/lib/Horizon_AD_Tool/Main.py
/usr/lib/Horizon_AD_Tool/syncer.json
/usr/share/pixmaps/Horizon.png


%changelog
* Mon May 9 2025 Brad Heffernan <brad.heffernan83@outlook.com>
- 
