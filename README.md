## Flatpak

There is some way of [doing flatpak declaratively with NixOS](https://github.com/gmodena/nix-flatpak) but that's for another day. For now, to make flatpaks work, after everything is ready, run this:

```
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```

Then reboot. From https://flatpak.org/setup/NixOS
