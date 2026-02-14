## Getting the URL of a remote

Few options available when you need to get the URL of a remote

1. `git remote show origin`

   Requires a network access to the remote

2. `git remote get-url origin`

   Requires Git >= 2.7

3. `git config --get remote.origin.url`
