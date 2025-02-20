# Contributing to AkenoX-Inline

Thank you for your interest in contributing to AkenoX-Inline! We welcome contributions from everyone, whether you're fixing bugs, improving documentation, or proposing new features. This guide will help you get started.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
   - [Reporting Bugs](#reporting-bugs)
   - [Suggesting Enhancements](#suggesting-enhancements)
   - [Your First Code Contribution](#your-first-code-contribution)
3. [Development Setup](#development-setup)
4. [Pull Request Guidelines](#pull-request-guidelines)
5. [Style Guide](#style-guide)
6. [License](#license)

## Code of Conduct
By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## How to Contribute

### Reporting Bugs
- **Check if the bug has already been reported**: Search the [Issues](https://github.com/TeamKillerX/AkenoX-Inline/issues) to avoid duplicates.
- **Provide details**: Include steps to reproduce, expected behavior, actual behavior, and screenshots if applicable.
- **Use the bug report template**: Fill out the template when creating a new issue.

### Suggesting Enhancements
- **Check if the enhancement has already been suggested**: Search the [Issues](https://github.com/TeamKillerX/AkenoX-Inline/issues) to avoid duplicates.
- **Explain the enhancement**: Describe the feature, why it’s useful, and how it should work.
- **Use the enhancement template**: Fill out the template when creating a new issue.

### Your First Code Contribution
If you're new to open source, check out our [Good First Issues](https://github.com/TeamKillerX/AkenoX-Inline/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22) to get started.

## Development Setup
1. **Fork the repository**: Click the "Fork" button on GitHub.
2. **Clone your fork**:
   ```bash
   git clone https://github.com/TeamKillerX/AkenoX-Inline.git
   cd AkenoX-Inline
   ```
3. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```
4. **Create a branch**:
   ```bash
   git checkout -b main
   ```
5. **Make your changes**: Follow the [Style Guide](#style-guide).
6. **Test your changes**: Run the test suite to ensure nothing is broken.
   ```bash
   pytest
   ```
7. **Commit your changes**:
   ```bash
   git commit -m "Your descriptive commit message"
   ```
8. **Push your changes**:
   ```bash
   git push origin main
   ```
9. **Open a Pull Request**: Go to your fork on GitHub and click "New Pull Request."

## Pull Request Guidelines
- **Keep it small**: Focus on one issue or feature per pull request.
- **Describe your changes**: Explain what your PR does and why it’s needed.
- **Reference issues**: Link to any related issues using `#issue-number`.
- **Follow the style guide**: Ensure your code adheres to the project’s style guide.

## Style Guide
- **Code formatting**: Use 4 spaces for indentation, and follow the existing code style.
- **Commit messages**: Write clear, concise commit messages in the present tense (e.g., "Fix bug" not "Fixed bug").
- **Documentation**: Update documentation if your changes affect functionality.

## License
By contributing to this project, you agree that your contributions will be licensed under the [MIT License](https://github.com/TeamKillerX/AkenoX-Inline/blob/main/LICENSE).
