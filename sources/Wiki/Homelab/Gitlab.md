## To reset the root password
https://docs.gitlab.com/ee/security/reset_user_password.html#reset-the-root-password

https://stackoverflow.com/questions/60062065/gitlab-initial-root-password

```bash
sudo gitlab-rake "gitlab:password:reset[root]"
```

