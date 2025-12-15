#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-prance.spec)

Summary:	Resolving Swagger/OpenAPI 2.0 and 3.0.0 Parser
Summary(pl.UTF-8):	Rozwiązujący parser Swagger/OpenAPI 2.0 i 3.0.0
Name:		python-prance
# keep 0.16.x here for python2 support
Version:	0.16.2
Release:	1
License:	MIT-like
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/prance/
Source0:	https://files.pythonhosted.org/packages/source/p/prance/prance-%{version}.tar.gz
# Source0-md5:	9b63ee905d8cbad62c14cb39e677eb79
URL:		https://pypi.org/project/prance/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-chardet >= 3.0
BuildRequires:	python-click >= 7.0
BuildRequires:	python-flex >= 6.13
BuildRequires:	python-pytest >= 4.2
BuildRequires:	python-pytest-cov >= 2.6
BuildRequires:	python-openapi-spec-validator >= 0.2.1
BuildRequires:	python-semver >= 2.8
BuildRequires:	python-swagger-spec-validator >= 2.4
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-chardet >= 3.0
BuildRequires:	python3-click >= 7.0
BuildRequires:	python3-flex >= 6.13
BuildRequires:	python3-pyicu >= 2.2
BuildRequires:	python3-pytest >= 4.2
BuildRequires:	python3-pytest-cov >= 2.6
BuildRequires:	python3-openapi-spec-validator >= 0.2.1
BuildRequires:	python3-semver >= 2.8
BuildRequires:	python3-swagger-spec-validator >= 2.4
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-2 >= 1.8
%endif
Requires:	python-modules >= 1:2.7
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

%package -n python3-prance
Summary:	Resolving Swagger/OpenAPI 2.0 and 3.0.0 Parser
Summary(pl.UTF-8):	Rozwiązujący parser Swagger/OpenAPI 2.0 i 3.0.0
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-prance
Prance provides parsers for Swagger/OpenAPI 2.0 and 3.0 API
specifications in Python. It uses flex or openapi_spec_validator to
validate specifications, but additionally resolves JSON references
in accordance with the OpenAPI spec.

%description -n python3-prance -l pl.UTF-8
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
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin \
%{__python} -m pytest tests -k 'not test_convert_defaults and not test_convert_output and not test_canonical and not test_resolver_named and not test_resolver_recursive_files and not test_issue_22_empty_path and not test_fetch_url_http and not test_with_externals_resolve'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin \
%{__python3} -m pytest tests -k 'not test_with_externals_resolve and not test_openapi_spec_validator_issue_5_integer_keys and not test_openapi_spec_validator_validate_success and not test_openapi_spec_validator_validate_failure and not test_openapi_spec_validator_issue_20_spec_version_handling and not test_convert_defaults and not test_convert_output and not test_issue_39_sequence_indices and not test_canonical and not test_resolver_named and not test_resolver_missing_reference and not test_resolver_recursive_objects and not test_resolver_recursive_files and not test_issue_22_empty_path and not test_fetch_url_http' --cov-fail-under=90
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/prance{,-2}
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/prance{,-3}
ln -sf prance-3 $RPM_BUILD_ROOT%{_bindir}/prance
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/prance-2
%{py_sitescriptdir}/prance
%{py_sitescriptdir}/prance-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-prance
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/prance-3
%{_bindir}/prance
%{py3_sitescriptdir}/prance
%{py3_sitescriptdir}/prance-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
