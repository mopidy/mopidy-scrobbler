# mopidy-scrobbler

![PyPI - Version](https://img.shields.io/pypi/v/mopidy-scrobbler?link=https://pypi.org/p/mopidy-scrobbler)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/mopidy/mopidy-scrobbler/ci.yml?link=https://github.com/mopidy/mopidy-scrobbler/actions/workflows/ci.yml)
![Codecov](https://img.shields.io/codecov/c/gh/mopidy/mopidy-scrobbler?link=https://codecov.io/gh/mopidy/mopidy-scrobbler)

[Mopidy](https://www.mopidy.com/) extension for scrobbling played tracks to [Last.fm](https://www.last.fm/).

This extension requires a free user account at Last.fm.

## Maintainer wanted

Mopidy-Scrobbler is currently kept on life support by the Mopidy core developers.
It is in need of a more dedicated maintainer.

If you want to be the maintainer of Mopidy-Scrobbler, please:

1. Make 2-3 good pull requests improving any part of the project.

2. Read and get familiar with all of the project's open issues.

3. Send a pull request removing this section and adding yourself as the
   "Current maintainer" in the "Credits" section below. In the pull request
   description, please refer to the previous pull requests and state that
   you've familiarized yourself with the open issues.

   As a maintainer, you'll be given push access to the repo and the authority
   to make releases to PyPI when you see fit.

## Installation

Install by running:

```sh
python3 -m pip install mopidy-scrobbler
```

See https://mopidy.com/ext/scrobbler/ for alternative installation methods.

## Configuration

The extension is enabled by default when it is installed. You just need to add
your Last.fm username and password to your Mopidy configuration file:

```ini
[scrobbler]
username = alice
password = secret
```

The following configuration values are available:

- `scrobbler/enabled`: If the scrobbler extension should be enabled or not.
  Defaults to enabled.
- `scrobbler/username`: Your Last.fm username.
- `scrobbler/password`: Your Last.fm password.

## Project resources

- [Source code](https://github.com/mopidy/mopidy-scrobbler)
- [Issues](https://github.com/mopidy/mopidy-scrobbler/issues)
- [Releases](https://github.com/mopidy/mopidy-scrobbler/releases)

## Development

### Set up development environment

Clone the repo using, e.g. using [gh](https://cli.github.com/):

```sh
gh repo clone mopidy/mopidy-scrobbler
```

Enter the directory, and install dependencies using [uv](https://docs.astral.sh/uv/):

```sh
cd mopidy-scrobbler/
uv sync
```

### Running tests

To run all tests and linters in isolated environments, use
[tox](https://tox.wiki/):

```sh
tox
```

To only run tests, use [pytest](https://pytest.org/):

```sh
pytest
```

To format the code, use [ruff](https://docs.astral.sh/ruff/):

```sh
ruff format .
```

To check for lints with ruff, run:

```sh
ruff check .
```

To check for type errors, use [pyright](https://microsoft.github.io/pyright/):

```sh
pyright .
```

### Making a release

To make a release to PyPI, go to the project's [GitHub releases
page](https://github.com/mopidy/mopidy-scrobbler/releases)
and click the "Draft a new release" button.

In the "choose a tag" dropdown, select the tag you want to release or create a
new tag, e.g. `v0.1.0`. Add a title, e.g. `v0.1.0`, and a description of the changes.

Decide if the release is a pre-release (alpha, beta, or release candidate) or
should be marked as the latest release, and click "Publish release".

Once the releease is created, the `release.yml` GitHub Action will automatically
build and publish the release to
[PyPI](https://pypi.org/project/mopidy-scrobbler/).

## Credits

- Original author: [Stein Magnus Jodal](https://github.com/jodal)
- Current maintainer: None. Maintainer wanted, see section above.
- [Contributors](https://github.com/mopidy/mopidy-scrobbler/graphs/contributors)
