#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Resolving Swagger/OpenAPI 2.0 and 3.0.0 Parser
Summary(pl.UTF-8):	Rozwiązujący parser Swagger/OpenAPI 2.0 i 3.0.0
Name:		python3-prance
Version:	25.4.8.0
Release:	1
License:	MIT-like
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/prance/
Source0:	https://files.pythonhosted.org/packages/source/p/prance/prance-%{version}.tar.gz
# Source0-md5:	7c06c29895f709df86e23d70badeb192
URL:		https://pypi.org/project/prance/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.10
BuildRequires:	python3-setuptools >= 1:65.0.1
BuildRequires:	python3-setuptools_scm >= 8.0.1
BuildRequires:	python3-wheel
%if %{with tests}
BuildRequires:	python3-chardet >= 5.2
BuildRequires:	python3-click >= 8.1.8
BuildRequires:	python3-flex >= 6.14.1
BuildRequires:	python3-packaging >= 24.2
BuildRequires:	python3-pyicu >= 2.14
BuildRequires:	python3-pytest >= 8.3.5
BuildRequires:	python3-pytest-cov >= 6.0
BuildRequires:	python3-requests >= 2.32.3
BuildRequires:	python3-ruamel.yaml >= 0.18.10
BuildRequires:	python3-openapi-spec-validator >= 0.7.1
BuildRequires:	python3-swagger-spec-validator >= 3.0.4
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	sphinx-pdg-3 >= 8.1.3
%endif
Requires:	python3-modules >= 1:3.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Prance provides parsers for Swagger/OpenAPI 2.0 and 3.0 API
specifications in Python. It uses flex or openapi_spec_validator to
validate specifications, but additionally resolves JSON references
in accordance with the OpenAPI spec.

%description -l pl.UTF-8
Prance dostarcza parsery Pythona do specyfikacji API Swagger/OpenAPI 2.0
oraz 3.0. Do sprawdzania poprawności specyfikacji wykorzystuje moduły
flex lub openapi_spec_validator, ale dodatkowo rozwiązuje referencje
JSON zgodnie ze specyfikacją OpenAPI.

%package apidocs
Summary:	API documentation for Python prance module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona prance
Group:		Documentation

%description apidocs
API documentation for Python prance module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona prance.

%prep
%setup -q -n prance-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin \
%{__python3} -m pytest tests -k 'not test_convert_defaults and not test_convert_output and not test_convert_petstore_yaml and not test_convert_petstore_json and not test_convert_petstore_yaml_explicit_name and not test_convert_url and not test_convert_spec and not test_convert_parser_lazy_swagger_backend and not test_convert_parser_validated and not test_fetch_url_http'
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__mv} $RPM_BUILD_ROOT%{_bindir}/prance{,-3}
ln -sf prance-3 $RPM_BUILD_ROOT%{_bindir}/prance

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst COMPATIBILITY.rst LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/prance-3
%{_bindir}/prance
%{py3_sitescriptdir}/prance
%{py3_sitescriptdir}/prance-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_modules,_static,api,*.html,*.js}
%endif
