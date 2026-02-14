## VM template

From [pycvala.de/blog/proxmox/create-your-own-debian-12-cloud-init-template](https://pycvala.de/blog/proxmox/create-your-own-debian-12-cloud-init-template/)

```bash
wget https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-generic-amd64.qcow2

# Creating base VM
qm create 9000 \
    --name debian12-cloudinit \
    --net0 virtio,bridge=vmbr0 \
    --scsihw virtio-scsi-pci \
    --machine q35

# Configuring disk
qm set 9000 \
    --scsi0 local-lvm:0,discard=on,ssd=1,format=qcow2,import-from=/root/debian-12-generic-amd64.qcow2
qm disk resize 9000 scsi0 8G

# Setting the Boot order
qm set 9000 --boot order=scsi0

# Configuring CPU and memory Resources
qm set 9000 --cpu host --cores 2 --memory 1024

# Configuring BIOS and EFI
qm set 9000 \
    --bios ovmf \
    --efidisk0 local-lvm:1,format=qcow2,efitype=4m,pre-enrolled-keys=1

# Setting up Cloud-Init
qm set 9000 --ide2 local-lvm:cloudinit

# Enabling QEMU Guest Agent
qm set 9000 --agent enabled=1

# Customizing Cloud-Init Settings => this is done in the Proxmox UI

# Creating the VM template
qm template 9000
```

