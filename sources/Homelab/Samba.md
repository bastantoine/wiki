# Installing and configuring Samba

## Installing

```bash
sudo apt install samba samba-common-bin
```

## Configuring

```bash
sudo vim /etc/samba/smb.conf
```

Ensure that user based authentication is configured:

```ini
[global]
security = user
```
[\[src\]](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html#SECURITY)

Configure the shares:

```ini
[<share name>]
  comment= <Share comment>
  path = </share/path/>
  valid users = @users
  force group = users
  create mask = 0660
  directory mask = 0771
  read only = no
```

### Ensuring maximal compatibility with macOS

Additional configuration is required to ensure maximal compatiblity with macOS clients:

```ini
min protocol = SMB3
ea support = yes
vfs objects = fruit streams_xattr
fruit:metadata = stream
fruit:model = MacSamba
fruit:veto_appledouble = no
fruit:nfs_aces = no
fruit:wipe_intentionally_left_blank_rfork = yes
fruit:delete_empty_adfiles = yes
fruit:posix_rename = yes
fruit:zero_file_id = yes
```
[\[src\]](https://gist.github.com/fschiettecatte/02d61e3d36c5f8d36bd45586fc5d0dc7)

## Authentication

Unless configured otherwise, authentication is managed by Samba itself, based on users on the system.

You need to configure the password of a user first:

```bash
sudo smbpasswd -a <username>
```

Make sure `<username>` match to an already existing user on the current machine. If not, create it first:

```bash
sudo adduser <username>
```

## Restart daemon

```bash
sudo /etc/init.d/smbd restart
```
