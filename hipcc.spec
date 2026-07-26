Name:		hipcc
Version:	7.14.0
Release:	1
Summary:	HIP compiler driver (hipcc / hipconfig)
License:	MIT
Group:		Development/Other
URL:		https://github.com/ROCm/llvm-project
# Filtered amd/hipcc from llvm-project @ therock-7.14
Source0:	hipcc-%{version}.tar.gz
# FHS: system /usr/bin/clang++ (unless private ROCm llvm exists); lib64 paths
Patch0:		0001-fhs-system-clang-lib64.patch

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	libstdc++-static-devel

Requires:	clang >= %{rocm_llvm_maj_ver}
# hipcc typically needs hip runtime headers available for useful work
# soft-suggest via Recommends later once rocm-hip exists

ExclusiveArch:	%{x86_64} %{aarch64}

%description
hipcc and hipconfig — compiler drivers that invoke system clang for
HIP device/host compilation.

On OpenMandriva FHS layouts this package patches hipcc to:
- use /usr/bin/clang++ unless a private TheRock/ROCm clang exists at
  $ROCM_PATH/lib/llvm/bin/clang++
- prefer %{_libdir} (lib64 on 64-bit) for HIP libraries and device bitcode
- pass --rocm-path / --rocm-device-lib-path so system clang finds the stack

%prep
%autosetup -n hipcc-%{version} -p0

%cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
# Drop Windows bat wrappers under /usr/hip
rm -rf %{buildroot}/usr/hip
# Tensile / rocBLAS expect ROCm-style amdclang names (system clang on OM)
ln -sfn clang %{buildroot}%{_bindir}/amdclang
ln -sfn clang++ %{buildroot}%{_bindir}/amdclang++

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/hipcc
%{_bindir}/hipconfig
%{_bindir}/amdclang
%{_bindir}/amdclang++
%exclude %{_docdir}/hipcc/*
