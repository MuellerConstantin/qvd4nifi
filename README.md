# qvd4nifi

> NiFi processors for reading and writing QVD files.

---

- [Introduction](#introduction)
- [Usage](#usage)
- [License](#license)
  - [Forbidden](#forbidden)

---

## Introduction

The _qvd4nifi_ library provides a set of Apache NiFi processors for reading and writing QVD files, which are a proprietary file format used by QlikView and Qlik Sense to store data. The library allows users to easily integrate QVD file processing into their NiFi data flows, enabling seamless data integration and transformation. With _qvd4nifi_, users can read data from QVD files, perform transformations, and write the results back to QVD files, all within the NiFi ecosystem. Internally, the library utilizes the [PyQvd](https://github.com/MuellerConstantin/PyQvd) library for QVD file operations.

## Usage

With every release, a new artifact, a NAR (NiFi Archive) file, is published to the [GitHub Releases](https://github.com/MuellerConstantin/qvd4nifi/releases) page of this repository. To use the library, simply download the latest NAR file and place it in the `lib` directory of your NiFi installation. After restarting NiFi, the new processors will be available for use in your data flows. Detailed documentation on how to use the processors can be found in the [NiFi User Guide](https://nifi.apache.org/docs/nifi-docs/html/user-guide.html) and the processor-specific documentation provided in the GitHub repository.

The NAR artifact is delivered as a standalone package, which means that all dependencies are included within the NAR file. This allows for easy deployment and ensures that there are no conflicts with other NiFi processors or libraries.

## License

Copyright (c) 2026 Constantin Müller and contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[MIT License](https://opensource.org/licenses/MIT) or [LICENSE](LICENSE) for
more details.

### Forbidden

**Hold Liable**: Software is provided without warranty and the software
author/license owner cannot be held liable for damages.
