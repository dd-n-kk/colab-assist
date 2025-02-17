
### [0.3.0](https://github.com/dd-n-kk/colab-assist/compare/v0.2.2..v0.3.0) - 2025-02-17

#### Documentation

- Correct version number in CHANGELOG - ([6df1166](https://github.com/dd-n-kk/colab-assist/commit/6df11669c1f0c1b89e965f3cceafcf783ff2e1e3)) - dd-n-kk

#### Chores

- **(cicd)** Fix version bump options of release PR workflow - ([2a5caa5](https://github.com/dd-n-kk/colab-assist/commit/2a5caa593e0daa1e46f6d32b842d7fbd222d525e)) - dd-n-kk

---

### [0.2.2](https://github.com/dd-n-kk/colab-assist/compare/v0.2.1..v0.2.2) - 2025-02-17

#### Features

-  [**breaking**]Drop `reinstall()` alias due to niche use case (#12) - ([f0805d1](https://github.com/dd-n-kk/colab-assist/commit/f0805d19b18ee54ab89fbfecf287d520ab46cad5)) - dd-n-kk

---

### [0.2.1](https://github.com/dd-n-kk/colab-assist/compare/v0.2.0..v0.2.1) - 2025-02-17

#### Bug Fixes

- Fix editable installation for `clone()` (#10) - ([95dac62](https://github.com/dd-n-kk/colab-assist/commit/95dac62b5ecf0d16e95fa983a607a87b9e12b194)) - dd-n-kk

#### Documentation

- Clarify usage - ([092626c](https://github.com/dd-n-kk/colab-assist/commit/092626cd1a5357f087e98ed4a421b10cba127171)) - dd-n-kk

---

### [0.2.0](https://github.com/dd-n-kk/colab-assist/compare/v0.1.2..v0.2.0) - 2025-02-16

#### Features

- Add edit() - ([96300da](https://github.com/dd-n-kk/colab-assist/commit/96300da44d5e55283293241d2adbd8695ad5b0a7)) - dd-n-kk
- Add `__version__` attribute to module (#1) - ([0cf32f5](https://github.com/dd-n-kk/colab-assist/commit/0cf32f52cd7ea5415ad590f565709cee26dbf9cb)) - dd-n-kk
-  [**breaking**]Overhaul `install()` and add `update()` and `reinstall()` - ([4031d3a](https://github.com/dd-n-kk/colab-assist/commit/4031d3a2bf0a9b609da5cb0914db5b5b2e5c2708)) - dd-n-kk
-  [**breaking**]Overhaul and rename `clone_gh()` and `pull_gh()` into `clone()` and `pull()` respectively - ([9ab8279](https://github.com/dd-n-kk/colab-assist/commit/9ab82794c0b63c530a4cf819ffcd37905544a4c6)) - dd-n-kk

#### Bug Fixes

- Correct state bookkeeping of `update_git()` - ([954dda5](https://github.com/dd-n-kk/colab-assist/commit/954dda5b88615099ce278cb5fde1541bcccc3799)) - dd-n-kk

#### Refactoring

- Move import state maintenance & colabtool dependencies into `_colab` module to simplify mocking - ([eb972a0](https://github.com/dd-n-kk/colab-assist/commit/eb972a0c54cb8c2ebe636cb3182be53cbcd60089)) - dd-n-kk
-  [**breaking**]Rename `opt` parameter of `edit()` to `x` - ([9db743e](https://github.com/dd-n-kk/colab-assist/commit/9db743eafd6077dfa5cbf4f726d7c28a963c3395)) - dd-n-kk

#### Documentation

- Edit project description - ([e26df0c](https://github.com/dd-n-kk/colab-assist/commit/e26df0c770974b51a67d863f7290e2be8a5c0687)) - dd-n-kk
- Add shields badges and adjustments - ([2a2524a](https://github.com/dd-n-kk/colab-assist/commit/2a2524aa2c96593ce0282af512dfda8d255233f6)) - dd-n-kk
- Setup CHANGELOG - ([5540d47](https://github.com/dd-n-kk/colab-assist/commit/5540d47d2f824f6f70971e02b5f8e97d8db150df)) - dd-n-kk
- Add badges to README - ([192c25e](https://github.com/dd-n-kk/colab-assist/commit/192c25ea9fb926708d651e45d33a65b7f8d6484c)) - dd-n-kk
- Update README and correct docstring - ([76a9a3d](https://github.com/dd-n-kk/colab-assist/commit/76a9a3d8ecc50296d68759410bd521e1e86aa8b6)) - dd-n-kk

#### Tests

- Add test script stub - ([ed53a11](https://github.com/dd-n-kk/colab-assist/commit/ed53a1106d3326926e2bd21e58aead3c83333c3b)) - dd-n-kk
- Add tests for `restart()`, `mount()`, `unmount()`, `end()`, and helpers - ([2276e69](https://github.com/dd-n-kk/colab-assist/commit/2276e69756cfa366f3cbe6e0193f1ae48888e3f5)) - dd-n-kk

#### Chores

- **(build)** Remove upper cap on Python version - ([a201e7d](https://github.com/dd-n-kk/colab-assist/commit/a201e7da841547c9b1a5b4841ef81c4d86b7048a)) - dd-n-kk
- **(build)** Bumpy Python version to >=3.11 - ([427afd2](https://github.com/dd-n-kk/colab-assist/commit/427afd2677cd4afbd48e2a80c3fb5960fac88152)) - dd-n-kk
- **(cicd)** Add CI workflow - ([8b1e4b4](https://github.com/dd-n-kk/colab-assist/commit/8b1e4b47568cfb9508073f22f4f402d3fc380f0f)) - dd-n-kk
- **(cicd)** Add release PR workflow - ([687c22b](https://github.com/dd-n-kk/colab-assist/commit/687c22b0b3fe349883de2842ab1d821376c93dcd)) - dd-n-kk
- **(cicd)** Remove installation tests from release workflow - ([69c6b8d](https://github.com/dd-n-kk/colab-assist/commit/69c6b8dc41d1082e190cb6e4c441a3a873457059)) - dd-n-kk
- Add pytest & pytest-cov as dev dependencies - ([ab64211](https://github.com/dd-n-kk/colab-assist/commit/ab64211e1584263284dd2276712bb339502a673f)) - dd-n-kk

---

### 0.1.2 - 2025-01-24

#### Features

- Add colab_utils module - ([6610847](https://github.com/dd-n-kk/colab-assist/commit/6610847b197108006159ac2bd0be8710cb8b025e)) - dd-n-kk
- Overhaul colab_util module - ([18caa9b](https://github.com/dd-n-kk/colab-assist/commit/18caa9b4aea00d4baca8644d56d46e2cbbd2d481)) - dd-n-kk
- Add download() - ([1301e8d](https://github.com/dd-n-kk/colab-assist/commit/1301e8d1c11c922459574314e06126e838f57aaf)) - dd-n-kk

#### Bug Fixes

- Replace exit() with IPython.core.getipython.get_ipython().ask_exit() to prevent NameError - ([7882fe2](https://github.com/dd-n-kk/colab-assist/commit/7882fe241c1ee43fa0d3baf9e9205176e17e1542)) - dd-n-kk
- Add option -U to uv pip install command in install() for package update - ([e71fff0](https://github.com/dd-n-kk/colab-assist/commit/e71fff0fbc186a7d302069a0469038f2444bb924)) - dd-n-kk

#### Documentation

- Docs setup - ([3a94527](https://github.com/dd-n-kk/colab-assist/commit/3a945271b7a0b6a533f1ddd3766032844d929e9d)) - dd-n-kk
- Add autorefs plugin - ([9d18a5f](https://github.com/dd-n-kk/colab-assist/commit/9d18a5f04f4cb6ea0543d754c1762dc1e4b82a9e)) - dd-n-kk
- Update README - ([e98e3e8](https://github.com/dd-n-kk/colab-assist/commit/e98e3e8b78c31dc9e4b66651201aca4fd5a89b14)) - dd-n-kk
- Add .readthedocs.yaml - ([721dfde](https://github.com/dd-n-kk/colab-assist/commit/721dfde0a9ee17754e269247d222a962bf5010e4)) - dd-n-kk
- Update docs URL - ([a9e95d4](https://github.com/dd-n-kk/colab-assist/commit/a9e95d4a2b5bf934dcfd4d9ec1844866a4d504fd)) - dd-n-kk

#### Chores

- Edit .gitignore - ([46d6dd2](https://github.com/dd-n-kk/colab-assist/commit/46d6dd2336fc418321b458ee35ddfaefa4c437a4)) - dd-n-kk
- Project setup - ([81622b9](https://github.com/dd-n-kk/colab-assist/commit/81622b95f34c33e53c4340bca6b409a07e1d3714)) - dd-n-kk
- Edit project description - ([89963b1](https://github.com/dd-n-kk/colab-assist/commit/89963b1e3829e060a38dccf8dd6934bf0ca65321)) - dd-n-kk
- Correct README.md path - ([2ac692e](https://github.com/dd-n-kk/colab-assist/commit/2ac692e0b4ed1b3f1673eaeea654a983fa651427)) - dd-n-kk
- Relax dependency requirements - ([87d9d90](https://github.com/dd-n-kk/colab-assist/commit/87d9d90be12ea44591d7d7e28df1964eb3118315)) - dd-n-kk
- Change Python version to 3.11 - ([2189581](https://github.com/dd-n-kk/colab-assist/commit/21895816e3146a86a53db20d6a782349b47f2eee)) - dd-n-kk
- Rename project from colab-utils to colast - ([9f5d189](https://github.com/dd-n-kk/colab-assist/commit/9f5d189a8bbf33ab43b14e6b9d6f3129b0c9d604)) - dd-n-kk
- Version bump - ([f6f3750](https://github.com/dd-n-kk/colab-assist/commit/f6f3750dde1ac7d327c914e78060687f6ba0d9f6)) - dd-n-kk
- Version bump - ([6ee1ee9](https://github.com/dd-n-kk/colab-assist/commit/6ee1ee92ed0c251b1049f5c750a9e01fbc1a3693)) - dd-n-kk
- Rename project from colast to colab-assist - ([a083448](https://github.com/dd-n-kk/colab-assist/commit/a0834480d55d5b7354efac36f46beccf143ff9d6)) - dd-n-kk

---
<!-- generated by git-cliff -->
