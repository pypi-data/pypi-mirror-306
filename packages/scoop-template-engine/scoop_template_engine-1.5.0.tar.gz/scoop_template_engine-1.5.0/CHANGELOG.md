# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.5.0] - 2024-11-02
### Added
- Add template for GAMMAS journal.
- Add two templates for letters.
### Changed
- Improve output of `ste list --template`.
### Fixed
- Fix incorrectly escaped journal names.

## [1.4.2] - 2024-09-27
### Added
- Add a timeout for `init.py` scripts
- Catch potential error messages when `ste doc` is invoked.
- Have `ste list --template` report uninitialized templates.
### Changed
- Update the description on PyPI.

## [1.4.1] - 2024-09-26
### Fixed
- Fix template description for Frontiers/fams.
- Convert `bmcart.cls`-based templates to `sn-jnl.cls` and `svjour3.cls`.
- Ensure proper protection for certain `.bib` fields.
### Changed
- Improve typesetting of author affiliations for `amsart.cls`-based templates.
- Run bibgenerator template in draft mode.
- Fix an issue with `@STRING` expansion in `.bib` files.

## [1.4.0] - 2024-09-24
### Added
- Allow user-defined custom schemes.
### Changed
- Change `ste list` logic to enable listing of schemes and templates.

## [1.3.1] - 2024-09-23
### Fixed
- Fix stray \detokenize marks in ETNA template.

## [1.3.0] - 2024-09-15
### Added
- Add template using LaPreprint.
- Add template dumping metadata for arXiv submission.
- Add multiple template listings with various sorting criteria to documentation.
- Add template dumping data read from data file.
### Changed
- Increase the signature's verbosity.
### Fixed
- Honor citations in abstract and appendix files when generating custom `.bib` files.
- Add missing MSC code block to elsarticle.cls templates.
- Truncate author names in running heads where necessary.
- Fix author markup for SIAM and SIAMOnline journals.
- Fix handling of emails with underscores.
- Fix handling of URLs and DOIs with underscores in bibliographies.

## [1.2.0] - 2023-06-23
### Added
- Add template for Springer CSE journal.

## [1.1.3] - 2023-06-23
### Changed
- Allow out-of-directory compilation with custom `.bib` files, e.g., using `latexmk -pdf -outdir=build manuscript-pamm.tex`.

## [1.1.2] - 2023-06-23
### Fixed
- Unexpanded `\detokenize` commands in custom `.bib` files.

## [1.1.1] - 2023-04-30
### Changed
- Review and amend documentation.

## [1.1.0] - 2023-04-29
### Added
- Add `orcid:` key to `authors:`.
### Changed
- Implement `--protectfamilynames` switch into `spbf`.

## [1.0.4] - 2023-04-01
### Changed
- Update `Centre Mersenne/ojmo` resources.

## [1.0.3] - 2023-04-01
### Changed
- Update `Springer/sn-jnl.cls` resources.
### Fixed
- Use `wget` to retrieve SIAM style guides.

## [1.0.2] - 2023-03-07
### Fixed
- Fix version detection in `utilities.py`.

## [1.0.1] - 2023-03-07
### Changed
- Use `wget` to retrieve SIAM resources.

## [1.0.0] - 2023-03-07
### Added
- Initial production release with support of 377 scientific journals.
