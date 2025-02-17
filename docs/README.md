<div align="center">
  <h1><b>colab-assist</b></h1>
  <p>
    Google Colab workflow utilities
  </p>
</div>

---

[![Test PyPI][pypi-badge]][pypi]
[![Documentation][readthedocs-badge]][readthedocs]
[![Issues][issues-badge]][issues]

[![CI workflow status][ci-workflow-badge]][ci-workflow]
[![Release workflow status][release-workflow-badge]][release-workflow]
[![Test coverage][codecov-badge]][codecov]


## About

- __colab-assist__ is a small package that shares the utility functions that
  I find useful for my development workflows on [Google Colab](https://colab.google).

- Actually, this is also a semi-mock project that I use to learn Python open-source development.
  [Feedbacks, pointers, and feature suggestions](https://github.com/dd-n-kk/colab-assist/issues/)
  are much appreciated!


## Usage

### Experimenting your private Python package on Colab

1. Develop your package any way you like and push it to your private GitHub repo.

2. Make a repo-specific [personal access token (PAT)](https://is.gd/qWZkuT).

3. Store the PAT as a [Colab Secret](https://stackoverflow.com/a/77737451):

    ![Colab Secrets demo](assets/imgs/colab_secrets.png)

4. On Colab:
    ```py
    import colab_assist as A
    ```

    - Install → experiment → push → resintall:
      ```py
      # Install your private package
      A.install("$my_token@me/my_pkg@feat/foo")

      # Experiment
      from my_pkg import foo
      foo()

      # Update the repo

      # Reinstall updated package
      A.install("$my_token@me/my_pkg@feat/foo")

      # Reimport updated functions/classes without needing to restart Colab session
      foo = A.reload(foo)
      foo()
      ```

    - Or clone → experiment → push → pull:
      ```py
      # Clone your private package and automatically add it to `sys.path`
      A.clone("$my_token@me/my_pkg@feat/foo", x="p")

      # Experiment
      from my_pkg import foo
      foo()

      # Update the repo

      # Pull the update
      A.pull("my_pkg")

      # Reimport updated functions/classes without needing to restart Colab session
      foo = A.reload(foo)
      foo()

      # Or restart the Colab session with `sys.path` automatically recovered
      A.restart()

      import colab_assist as A  # Import `colab_assist` recovers previously extended `sys.path`
      from my_pkg import foo  # The clone is now again importable
      foo()

      # Terminate the Colab runtime with your clones automatically cleaned up
      A.end()
      ```

### Text file creation and editing

```py
# Create `foo.txt` at working directory and call `google.colab.files.view()` to edit it
A.edit("foo.txt", x="c")
```


## Dependencies & Installation

- Although currently colab-assist lists no dependencies,
  it is intended to __only be installed and used in a Google Colab environment__.
  The reason not to explicitly list dependencies for now is that
  at least one depedency ([`google-colab`](https://github.com/googlecolab/colabtools))
  is bespoke for Colab and not hosted on PyPI.
  However, colab-assist is designed to install and run just fine on a fresh Colab instance.

- You can install colab-assist very quickly with pre-installed uv on Colab:
  ``` { .yaml .copy }
  !uv pip install --system -q colab-assist
  ```
  Or with pip:
  ``` { .yaml .copy }
  %pip install -q colab-assist
  ```


## License

- [MIT license](https://github.com/dd-n-kk/colab-assist/blob/main/LICENSE)


## Acknowledgements

- [Google Colaboratory](https://github.com/googlecolab/colabtools)
- [uv](https://github.com/astral-sh/uv)
- [MkDocs](https://github.com/mkdocs/mkdocs)
- [Material for MkDocs](https://github.com/squidfunk/mkdocs-material)
- [mkdocstrings](https://github.com/mkdocstrings/mkdocstrings)
- [git-cliff](https://github.com/orhun/git-cliff)
- [shields](https://github.com/badges/shields)


[pypi-badge]: https://img.shields.io/pypi/v/colab-assist?style=for-the-badge&logo=pypi&logoColor=white&label=PYPI
[pypi]: https://pypi.org/project/colab-assist
[readthedocs-badge]: https://img.shields.io/readthedocs/colab-assist?style=for-the-badge&logo=readthedocs&logoColor=white
[readthedocs]: https://colab-assist.readthedocs.io
[issues-badge]: https://img.shields.io/github/issues/dd-n-kk/colab-assist?style=for-the-badge&logo=github&logoColor=white
[issues]: https://github.com/dd-n-kk/colab-assist/issues
[ci-workflow-badge]: https://img.shields.io/github/actions/workflow/status/dd-n-kk/colab-assist/ci.yaml?style=flat-square&logo=pytest&logoColor=white&label=CI
[ci-workflow]: https://github.com/dd-n-kk/colab-assist/actions/workflows/ci.yaml
[release-workflow-badge]: https://img.shields.io/github/actions/workflow/status/dd-n-kk/colab-assist/release.yaml?style=flat-square&logo=githubactions&logoColor=white&label=Build
[release-workflow]: https://github.com/dd-n-kk/colab-assist/actions/workflows/release.yaml
[codecov-badge]: https://img.shields.io/codecov/c/github/dd-n-kk/colab-assist?style=flat-square&logo=codecov&logoColor=white&label=Coverage
[codecov]: https://app.codecov.io/gh/dd-n-kk/colab-assist
