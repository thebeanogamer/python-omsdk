Name:           python-omsdk
Version:        1.2.509
Release:        %autorelease
Summary:        Example Python library

License:        Apache-2.0
URL:            https://github.com/dell/omsdk
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
Patch0:         setup-omsdk.py.patch

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  sed
BuildRequires:  pyproject-rpm-macros

# Untracked upstream dependencies (https://github.com/dell/omsdk/issues/36)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(wheel)
BuildRequires:  python3dist(pywinrm)

%global _description %{expand:
A python module which provides a convenient example.
This description provides some details.}

%description %_description

%package -n python3-omsdk
Summary:        %{summary}
%py_provides python3-omsdk
%py_provides python3-omdrivers

%description -n python3-omsdk %_description

%prep
%autosetup -p0 -n omsdk-%{version}
mv setup-omsdk.py setup.py
# ipaddress was merged into Python 3.3, so it does not need to de a dependancy
sed -i '/ipaddress>=0/d' setup.py
echo "%{version}" > _version.txt

%generate_buildrequires
%pyproject_buildrequires

# Upstream has shebangs on non-executable files
find omsdk -type f -exec sed -i '/\/usr\/bin\/env python3/d' {} +
find omdrivers -type f -exec sed -i '/\/usr\/bin\/env python3/d' {} +

# Fix line endings without dos2unix
sed -i 's/\r$//' README.md

%build
OMSDK_VERSION=%{version} %pyproject_wheel


%install
%pyproject_install
%pyproject_save_files omsdk omdrivers


%check
# omsdk.listener.sdktrapreceiver tries to start listening as soon as it is imported
# omsdk.sdksnmptrap depends on outdated SNMP support (https://github.com/dell/omsdk/issues/37)
%pyproject_check_import -e 'omsdk.listener.sdktrapreceiver' -e 'omsdk.sdksnmptrap'

%files -n python3-omsdk -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
%autochangelog
