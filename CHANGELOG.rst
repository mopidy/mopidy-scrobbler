*********
Changelog
*********

v2.0.0rc1 (2019-11-16)
======================

- Require Mopidy >= 3.0.0a4. No major changes required.

- Require Python >= 3.7. No major changes required.

- Require pylast >= 2.2, as that's the first version to support Python 3.7.

- Update project setup.


v1.2.1 (2019-03-10)
===================

- Require pylast < 3, as that version removed support for Python 2.7. (Fixes:
  #30)


v1.2.0 (2018-04-01)
===================

- Require pylast >= 1.6.0, which is the version packed in Debian stable.

- Fix compatability with pylast >= 2, which has removed the ``ScrobblingError``
  exception type.


v1.1.1 (2014-12-29)
===================

- Updated to work with ``None`` as the default value of ``track_no`` in
  Mopidy's ``Track`` model. This was changed in Mopidy 0.19.5. (Fixes: #7)


v1.1.0 (2014-01-20)
===================

- Updated extension API to match Mopidy 0.18.


v1.0.0 (2013-10-08)
===================

- Moved extension out of the main Mopidy project.

- Added test suite.
