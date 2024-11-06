Changelog
=========

v0.5.0 (2024-11-05)
-------------------

- Build GoReSym from source instead of vendoring the binary.
- Support building go-inspector for Linux aarch64/arm64 platform.
- Update GoReSym to v3.0.1

v0.4.0 (2024-10-31)
-------------------

- Use latest scancode-toolkit dependency model from v32.3.0
  Here ``is_resolved`` was renamed to ``is_pinned`` in DependentPackage
- Drop python 3.8 and support python 3.13

v0.3.1 (2024-09-06)
------------------------

- Return nothing if not a Go binary


v0.3.0 (2024-09-05)
------------------------

- Detect Go packages in binaries


v0.2.2 (2024-04-10)
------------------------

- Fix minor readme, image height


v0.2.1 (2024-04-10)
------------------------

- Fix minor readme typo


v0.2.0 (2024-04-09)
------------------------

- Add missing ABOUT file and license for goresym.
- Bump to version GoReSym 2.7.2
- Add support for dependencies and build info


v0.1.0 (2024-04-08)
------------------------

- Add goresym support in go-inspector.
