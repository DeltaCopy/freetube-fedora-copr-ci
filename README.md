# freetube-fedora-copr-ci
RPM build spec for building FreeTube on the Fedora COPR.

A GitHub actions workflow is scheduled to run daily at 12AM to check the latest version released from https://github.com/FreeTubeApp/FreeTube

If the latest version does not match the version available from the COPR then a new COPR build is triggered remotely.

The COPR project repository is available from: https://copr.fedorainfracloud.org/coprs/deltacopy/freetube

## Active releases available

- Fedora 41
- Fedora 42
- Fedora 43
- Fedora rawhide

# Instructions

Enable the COPR repository then install the package.

<pre>
sudo dnf copr enable deltacopy/freetube
sudo dnf in freetube
</pre>

<h3> COPR build status </h3> 

[![Copr build status](https://copr.fedorainfracloud.org/coprs/deltacopy/freetube/package/freetube/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/deltacopy/freetube/package/freetube/)

<h3> GitHub action workflow status </h3> 

[![FreeTube Fedora COPR build](https://github.com/DeltaCopy/freetube-fedora-copr-ci/actions/workflows/freetube-fedora-copr-ci.yml/badge.svg)](https://github.com/DeltaCopy/freetube-fedora-copr-ci/actions/workflows/freetube-fedora-copr-ci.yml)
