# Zedasignal Backend

The backend application for Zedasignal

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


# **Code Contribution Guide**

## **Introduction**

Welcome to the Django Project! This guide outlines the best practices and procedures for contributing code to our project. By following these guidelines, you can help maintain a healthy and efficient development process.

## **Table of Contents**

1. **[Getting Started](#getting-started)**
2. **[Branching Strategy](#branching-strategy)**
3. **[Pull Requests (PRs)](#pull-requests)**
4. **[Coding Standards](#coding-standards)**
5. **[Code Contribution Workfows](#code-contribution-workflow)**
5. **[Testing](#testing)**
6. **[Documentation](#documentation)**
7. **[Review Process](#review-process)**
8. **[Continuous Integration](#continuous-integration)**
9. **[Merging](#merging)**
10. **[Issue Tracking](#issue-tracking)**
11. **[License](#license)**

## **Getting Started**

1. **Fork the Repository**: Start by forking the main project repository on GitHub or the version control system of your choice.
2. **Clone Your Fork**: Clone your forked repository to your local development environment:

    ```
    https://github.com/mannyanebi/zedasignal-backend.git

    ```

3. **Set Up Remote**: Add the main project repository as a remote:

    ```
    git remote add upstream https://github.com/mannyanebi/zedasignal-backend.git

    ```

4. **Install Dependencies**: Install project dependencies and set up your development environment as specified in the project's documentation.

## **Branching Strategy**

1. **Branch Names**:
    - Create feature branches with descriptive names (e.g., **`feature/add-authentication`**).
    - Use hyphens as word separators in branch names.
    - Avoid using special characters or spaces in branch names.
2. **Branch from Main**: Create feature or bug-fix branches from the **`develop`** branch (or the project's default development branch).

## **Pull Requests (PRs)**

1. **Descriptive Titles**:
    - Provide a clear and descriptive title for your PR.
2. **Description**:
    - Write a detailed description that explains the purpose of the PR, the problem it addresses, and the changes made.
    - Include links to relevant issues.
3. **Reviewers**:
    - Assign one or more reviewers to your PR.
    - Reviewers should be knowledgeable about the codebase and the area you're modifying.
4. **Labeling**:
    - Label your PR appropriately (e.g., bug, feature, documentation) to help with categorization.

## **Coding Standards**

1. **PEP 8**: Follow the Python Enhancement Proposal 8 (PEP 8) coding style guide.
2. **Consistency**: Maintain consistency with existing code. Adhere to the project's coding conventions.
3. **Docstrings**: Include clear and informative docstrings for classes, functions, and modules.
4. **Comments**: Add comments where necessary to explain complex logic or provide context.
5. **Imports**: Organize imports according to PEP 8 guidelines. Use absolute imports for intra-project modules.

## **Code Contribution Workflow**

1. **Branch Strategy**:
    - Use a Git branching strategy like Gitflow or GitHub Flow to structure your branches. Gitflow is suitable for more complex projects with regular releases, while GitHub Flow is simpler and suits continuous deployment.
2. **Develop and Main Branches**:
    - Use **`develop`** as the integration branch where feature branches are merged for testing.
    - Use **`main`** as the stable branch for production releases.
3. **Feature Branches**:
    - Developers should create feature branches off **`develop`** for their tasks.
    - Name feature branches descriptively, including the issue or task number, e.g., **`feature/123-add-user-auth`**.
4. **Commits and Pull Requests**:
    - Encourage small, focused commits with clear and concise commit messages.
    - Each feature or bugfix should have its own pull request (PR).
    - Ensure PR titles and descriptions are informative.

### **GitHub Issues and Task Tracking:**

1. **Use GitHub Issues**:
    - Create a GitHub Issue for each task or bug.
    - Include details, acceptance criteria, and labels (e.g., bug, enhancement, feature) to categorize and track issues.
2. **Link Issues to PRs**:
    - Link PRs to the corresponding GitHub Issue. Use keywords like "Closes #123" or "Fixes #456" in PR descriptions to auto-close issues when the PR is merged.
3. **Task Status**:
    - Use labels (e.g., "In Progress," "Review," "Done") to indicate the status of an issue or PR.
    - Regularly update the status of issues and PRs.

### **Definition of Done (DoD):**


1. **DoD Checklist**:
    - Ensure all checklist items are completed before marking a task as "Done."
2. **Acceptance Criteria**:
    - Verify that all acceptance criteria are met before closing an issue or merging a PR.

### **Release Management:**

1. **Semantic Versioning**:
    - Follow Semantic Versioning (SemVer) to version your releases.
2. **Release Notes**:
    - Document release notes for each version, detailing changes, improvements, and bugfixes.
3. **Release Branches**:
    - Create a release branch from **`develop`** for final testing before merging to **`main`**.
4. **Continuous Integration**:
    - Use CI/CD pipelines to automate testing and deployment for each release.
5. **Rollback Plan**:
    - Have a rollback plan in place in case of critical issues with a release.
6. **Tagging Releases**:
    - Tag releases in your version control system to easily reference historical releases.

## **Testing**

1. **Unit Tests**: Write unit tests for new features and ensure that existing tests remain functional.*
2. **Test Coverage**: Aim for high test coverage. Cover edge cases and potential failure scenarios.*
3. **Continuous Integration**: Ensure that your code passes CI/CD checks and tests on all supported platforms.*
(More context on the asterisks below)
## **Documentation**

1. **ReadMe**: Keep the project's ReadMe updated with relevant information, including installation instructions and usage examples.
2. **Inline Documentation**: Document code using inline comments and docstrings.
3. **API Documentation**: If your changes affect APIs, update the API documentation accordingly.

## **Review Process**

1. **Reviewers**:
    - Reviewers should provide constructive feedback and suggestions.
    - Address comments and concerns promptly.
2. **Approval**: PRs should receive at least one approval from a reviewer before merging.
3. **Testing**: Ensure that the changes work as intended and do not introduce new issues.

## **Continuous Integration**

1. **CI/CD Pipelines**: Make sure your PR passes all CI/CD pipelines (e.g., linting, testing).
2. **Fix Failures**: If CI/CD pipelines fail, address the issues and retest.

## **Merging**

1. **Squash Commits**: If your PR has multiple commits, consider squashing them into a single commit with a descriptive message.
2. **Rebase**: Before merging, rebase your branch onto the latest **`main`** branch to ensure a clean history.
3. **Fast Forward**: Use "fast-forward" merges when possible to maintain a linear history.

## **Issue Tracking**

1. **Link to Issues**: Reference relevant issues in PRs and commit messages using keywords (e.g., "Closes #123").
2. **Keep Issues Updated**: Update issue statuses, descriptions

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy zedasignal_backend

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd zedasignal_backend
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd zedasignal_backend
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd zedasignal_backend
celery -A config.celery_app worker -B -l info
```

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [MailHog](https://github.com/mailhog/MailHog) with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`
