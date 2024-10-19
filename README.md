The base config is from the awesome repo from Misterio77 [nix-starter-configs](https://github.com/Misterio77/nix-starter-configs)

## Flatpak

There is some way of [doing flatpak declaratively with NixOS](https://github.com/gmodena/nix-flatpak) but that's for another day. For now, to make flatpaks work, after everything is ready, run this:

```
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```

Then reboot. From https://flatpak.org/setup/NixOS

## Build

To build:

```
sudo nixos-rebuild switch --flake .#nyarlathotep
```

To build boot:

```
sudo nixos-rebuild boot --flake .#nyarlathotep 
```

## Gaming
 
To enable proton, remember to run:

```
$ protonup
```
