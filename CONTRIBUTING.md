# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change.

## Code of Conduct

Please note we have a [Code of Conduct](https://www.mozilla.org/en-US/about/governance/policies/participation/), please follow it in all your interactions with the project.

## Filing an Issue

1. Look for a similar issue that may already exist.

2. If none exists, create a new issue and provide as much description and context as possible.

3. Apply any relevant labels to the issue.

## Pull Request Process

1. Find the issue you want to work on. If no relevant issue exists, see above and file an
   issue, then continue to the next step.

1. Assign the issue to yourself.

1. Create a branch in your local fork with the issue number in the name.

1. Implement the code changes described by the issue. All Python code changes should
   be accompanied by any relevant tests, either by modifying existing ones or adding new
   ones.

1. When all your changes are complete to your satisfaction:

- Run `make check` to run the full test, linting, formatting, and coverage suites.
- Fix any linting issues by running `make code_format` or by hand if the auto formatter is unable to fix it.
- Fix any broken tests
- Ensure coverage is not reduced.

1. When all tests and checks are passing, commit all your changes into a single commit and follow the [Git Commit Guidelines](#git-commit-guidelines)

1. Push your branch up to your fork and submit a pull request on to main. Add any additional
   information you'd like to the pull request body, including descriptions of changes, special instructions for testing, etc.

1. Request a review if one is not automatically selected for you.

1. If you receive feedback that requires changes to your pull request, make the changes locally,
   run `make check` again to ensure all tests and linting are passing, and then create a new commit
   that describes what feedback was addressed. This commit can be formatted however you like, it will
   be squashed before it is merged into main.

1. When your pull request is approved, it can be closed by using the 'Squash and Merge' button to
   squash all of the commits into a single one that refers to both the issue and the pull request and
   contains any additional descriptive information.

1. Thank you for submitting changes to Foxpuppet!

## Git Commit Guidelines

### Subject

The subject should follow the this pattern:

`type(scope): Description`

#### Type

One of the following

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing
  semi-colons, etc)
- **refactor**: A code change that neither fixes a bug or adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests
- **chore**: Changes to the build process or auxiliary tools and libraries such as documentation
  generation

#### Scope

One of the following:

- **project**: Anything that affects the entire project
- **foxpuppet**: Anything scoped only to Nimbus experiment frontend

#### Description

- use the imperative, present tense: "change" not "changed" nor "changes"
- don't capitalize first letter
- no dot (.) at the end

### Body

The body should describe the purpose of the commit, so that it's clear why this change is being
made. To assist in writing this along with the footer, a git commit template (saved as `~/.gitmessage`)
can be used:

```
Because

* Reason

This commit

* Change

Fixes #github_issue_number
```

Just as in the **subject**, use the imperative, present tense: "change" not "changed" nor "changes". Commits are expected to follow this format.


### Failed Dependabot PRs

If a Dependabot PR fails the CI checks you can either investigate the failure and see if it can be resolved quickly/easily, or close it altogether.


## Updating an existing fork

1.  Go to your cloned directory and add the main repository as your upstream

        git remote add upstream  https://github.com/mozilla/foxpuppet

2.  Fetch the latest changes from the main repository

        git fetch upstream

3.  Merge the changes from the main repository into your forked branch

        git merge upstream/main
