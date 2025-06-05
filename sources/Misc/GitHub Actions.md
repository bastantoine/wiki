Random bash tips and tricks to (_try to_) use GitHub Actions properly and efficiently...

## Using temporary dir

When you need to use temporary files within a GitHub Action, you can use the `${{ runner.temp }}` context variable or the `RUNNER_TEMP` environment variable.

Things to note:
- The temporary directory is job-specific and not shared between jobs
- The directory is cleared at the start and end of each job, only if the runner's user account have permission to delete them.

[\[src\]](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/accessing-contextual-information-about-workflow-runs#runner-context)

## Using outputs to pass data between jobs

```yaml
name: Test

on:
  push:

jobs:
  job_1:
    outputs:
      version: ${{ steps.step_1.outputs.version }}
    steps:
      - name: Format version
        id: step_1
        run: |
          VERSION=${{ github.ref_name }}
          echo "version=${VERSION}" >> $GITHUB_OUTPUT

  job_2:
    needs: [job_1]
    steps:
      - run: |
          echo "version=${{ needs.job_1.outputs.version }}"
```

## Ternary conditions

Github Actions doesn't have a proper ternary operator. Tricks can be used to achieve that:

```yaml
${{ github.ref != 'refs/heads/master' && 'true' || 'false' }}
```

Things to note:
- The second part of the `AND` must be truthy, otherwise the second part of the `OR` will always be returned.

[\[src`]](https://github.com/orgs/community/discussions/26738)
