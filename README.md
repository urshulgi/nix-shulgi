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

## Cleaning the system

`/nix` folder can get pretty big. Make sure to cleam your system sometimes.

(Read this reddit thread)[https://www.reddit.com/r/NixOS/comments/10107km/how_to_delete_old_generations_on_nixos/]
TL;DR


```
  nix-env --list-generations

  nix-collect-garbage  --delete-old

  nix-collect-garbage  --delete-generations 1 2 3

  # recommeneded to sometimes run as sudo to collect additional garbage
  sudo nix-collect-garbage -d

  # As a separation of concerns - you will need to run this command to clean out boot
  sudo /run/current-system/bin/switch-to-configuration boot
```
