Summary: A JNI Wrapper for the Unix pam(8) subsystem and a JAAS bridge
Name: jpam
License: Apache Software License, v. 1.1
URL: http://jpam.sourceforge.net/
Source0: %{name}-%{version}-src.zip
Patch0: bug219916_expired_password_hang.patch
Patch1: %{name}-%{version}-s390x.patch
Patch2: jpam-0.4-ppc.patch
Patch3: jpam-0.4-no_checkstyle.patch
Patch4: jpam-0.4-no-password-prompt.patch
Patch5: jpam-0.4-arm.patch
Version: 0.4
Release: 34%{?dist}

BuildRequires: apache-commons-beanutils >= 1.9
BuildRequires: gcc
BuildRequires: java-1.8.0-openjdk-devel
BuildRequires: make
BuildRequires: pam-devel
%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:      antlr
Requires:      apache-commons-beanutils
Requires:      apache-commons-collections
Requires:      apache-commons-io
Requires:      apache-commons-logging
Requires:      javapackages-tools
Requires:      regexp
BuildRequires: ant
BuildRequires: antlr
BuildRequires: apache-commons-collections
BuildRequires: apache-commons-io
BuildRequires: apache-commons-logging
BuildRequires: checkstyle
BuildRequires: javapackages-tools
BuildRequires: junit
BuildRequires: regexp
%else
Requires:      antlr
Requires:      jakarta-commons-beanutils
Requires:      jakarta-commons-collections
Requires:      jakarta-commons-logging
Requires:      regexp
BuildRequires: ant < 1.9
BuildRequires: ant-nodeps < 1.9
BuildRequires: antlr
BuildRequires: checkstyle
BuildRequires: jakarta-commons-collections
BuildRequires: jakarta-commons-logging
BuildRequires: junit
BuildRequires: regexp
%endif

# ia64 doesnt have a new enough java.
ExcludeArch:  ia64

%description
JPam provides a class to access the Unix pam(8) subsystem from
Java, and wraps it in a JAAS LoginModule

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

rm -Rfv tools/*.jar
build-jar-repository -p tools/ ant antlr commons-beanutils commons-collections commons-logging regexp checkstyle junit

%build
export JAVA_HOME=%{java_home}
%ant shared-object dist-jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 build/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m 644 src/dist/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
# FIXME: Sun's JDK does not search for libraries in /usr/lib, though
# IBM's does. This specfile will work for users with the IBM JRE, but not
# for users of Sun's JRE. Unfortunately, the two JRE's don't have a single
# directory in java.library.path in common.
install -D -m 755 build/gen-src/c/libjpam.so $RPM_BUILD_ROOT/usr/lib/libjpam.so

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr site/documentation/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%{_javadir}/*
/usr/lib/libjpam.so

%doc
%{_docdir}/*

%files javadoc
%{_javadocdir}/%{name}-%{version}

%changelog
* Wed May 03 2017 Michael Mraka <michael.mraka@redhat.com> 0.4-34
- recompile all packages with the same (latest) version of java

* Mon Apr 10 2017 Michael Mraka <michael.mraka@redhat.com> 0.4-33
- expanded (Build)Requires list to make it more readable

* Thu Apr 06 2017 Michael Mraka <michael.mraka@redhat.com> 0.4-32
- new checkstyle requirement

* Wed Apr 05 2017 Michael Mraka <michael.mraka@redhat.com> 0.4-31
- require older ant on RHEL6
- Revert jakarta-* -> apache-* changes

* Tue Apr 04 2017 Michael Mraka <michael.mraka@redhat.com> 0.4-30
- expand removed jar list define

* Tue Apr 04 2017 Michael Mraka <michael.mraka@redhat.com> 0.4-29
- updated RHEL6 Requires after jpackage removal
- consolidate ifs and defines into one place

* Sun Feb 21 2016 Jan Dobes <jdobes@redhat.com> 0.4-28
- adding arm Makefile

* Tue Jun 24 2014 Michael Mraka <michael.mraka@redhat.com> 0.4-27
- update jpam deps for RHEL7

* Wed Jan 08 2014 Tomas Lestach <tlestach@redhat.com> 0.4-26
- ant-nodeps is required on rhel as well

* Wed Jan 08 2014 Tomas Lestach <tlestach@redhat.com> 0.4-25
- differenciate only between actual and older fedora

* Wed Jan 08 2014 Tomas Lestach <tlestach@redhat.com> 0.4-24
- let jpam buildrequire ant
- let jpam build/require javapackages-tools on fc20

* Tue Jan 07 2014 Michael Mraka <michael.mraka@redhat.com> 0.4-23
- there's not ant-nodeps on fc20
- replace legacy name of Tagger with new one

* Fri Mar 15 2013 Michael Mraka <michael.mraka@redhat.com> 0.4-22
- fixed builder definition

* Wed Oct 17 2012 Jan Pazdziora 0.4-21
- 860119 - Remove expected password prompts from PAM_conv, they fail for
  non-English locales.

* Fri Dec 17 2010 Tomas Lestach <tlestach@redhat.com> 0.4-20
- disable checkstyle, since there's a problem with jpackage checkstyle

* Thu May 07 2009 Michael Mraka <michael.mraka@redhat.com> 0.4-19
- package rebuild

* Sat Feb 28 2009 Dennis Gilmore <dgilmore@redhat.com> - 0.4-18
- rebuild to pick up all rhel arches  exclude ia64
- patch in ppc support

* Wed Jan 28 2009 <dennis@ausil.us> 0.4-17
- BR java-devel >= 1.6.0
- remove version file

* Sun Aug 26 2007  <bperkins@redhat.com> 0.4-11
- Applying patch to allow building on Linux s390 and s390x.
  Originally found by Brad Hinson <bhinson@redhat.com>

* Wed Dec 20 2006  <jesusr@redhat.com> 0.4-9
- Applying patch to fix a hang when pam password has expired.
  Bugzilla: 219916

* Mon Apr 18 2005  <dlutter@redhat.com> 0.4-1
- Simplified packaging for version 0.4. libjpam.so is now
  installed into /usr/lib. Set JAVA_HOME

* Mon Apr  11 2005  <jesusr@redhat.com>
- Changed the jvm location to /usr/lib/jvm/java-ibm/ since
  using %{_libdir} causes libjpam to be placed in /usr/lib64
  which doesn't work with the ibm java

* Fri Apr  1 2005  <dlutter@redhat.com>
- Initial build.
