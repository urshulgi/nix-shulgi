# This is your home-manager configuration file
# Use this to configure your home environment (it replaces ~/.config/nixpkgs/home.nix)
{
  inputs,
  outputs,
  lib,
  config,
  pkgs,
  ...
}: {
  # You can import other home-manager modules here
  imports = [
    # If you want to use modules your own flake exports (from modules/home-manager):
    # outputs.homeManagerModules.example

    # Or modules exported from other flakes (such as nix-colors):
    # inputs.nix-colors.homeManagerModules.default

    # You can also split up your configuration and import pieces of it here:
    # ./nvim.nix
  ];

  nixpkgs = {
    # You can add overlays here
    overlays = [
      # Add overlays your own flake exports (from overlays and pkgs dir):
      outputs.overlays.additions
      outputs.overlays.modifications
      outputs.overlays.unstable-packages

      # You can also add overlays exported from other flakes:
      # neovim-nightly-overlay.overlays.default

      # Or define it inline, for example:
      # (final: prev: {
      #   hi = final.hello.overrideAttrs (oldAttrs: {
      #     patches = [ ./change-hello-to-hi.patch ];
      #   });
      # })
    ];
    # Configure your nixpkgs instance
    config = {
      # Disable if you don't want unfree packages
      allowUnfree = true;
    };
  };

  home = {
    username = "urshulgi";
    homeDirectory = "/home/urshulgi";
    packages = with pkgs; [
      neovim
      cargo
      flameshot
      obsidian
      quickemu
      quickgui
      spice
      steam
      steam-run
      protonup-ng
      openssl
      nerdfonts
      vesktop
      flatpak
      telegram-desktop
      rofi
      i3lock
      dunst
      goxlr-utility
      plex-media-player
      plexamp
      spotify
      (lutris.override {
        extraPkgs = pkgs: [
          wineWowPackages.stable
          winetricks		
        ];
      })
    ];
  };

  # Add stuff for your user as you see fit:
  # programs.neovim.enable = true;
  # home.packages = with pkgs; [ steam ];

  # Enable home-manager and git
  programs.home-manager.enable = true;
  programs.git = {
    enable = true;
    userName = "Nick Baldallo";
    userEmail = "nick@mich.is";
    extraConfig = {
      core = {
        editor = "nvim";
      };
    };
  };
  
  # Config zsh
  programs.zsh = {
    enable = true;
    enableCompletion = true;
    autosuggestion.enable = true;
    syntaxHighlighting.enable = true;
    shellAliases = {
      ll = "ls -l";
      nix-update = "cd ~/github-projects/nix-shulgi && sudo nixos-rebuild switch --flake .#nyarlathotep";
      nix-clean = "nix-env --delete-generations old && sudo nix-collect-garbage --delete-older-than 1d && nix-store --gc && sudo nixos-rebuild boot --flake .#nyarlathotep";
    };
    history = {
      size = 10000;
      path = "${config.xdg.dataHome}/zsh/history";
    };
    oh-my-zsh = {
      enable = true;
      plugins = ["git"];
      theme = "robbyrussell";
    };
  };
  
  # Config files
  xdg.configFile = {
    "qtile/config.py".source = ./qtile/config.py;
    "dunst/dunstrc".source = ./dunst/dunstrc;
    "picom/picom.conf".source = ./picom/picom.conf;
  };

  # Config picom
  services.picom = {
    enable = true;
    package = pkgs.unstable.picom;
  };

  # Zoxide config
  programs.zoxide = {
    enable = true;
    enableZshIntegration = true;
    options = ["--cmd cd"];
  };
  
  # Grobi config
  services.grobi = {
    enable = true;
    rules = [
      {
        name = "Default";
        outputs_connected = [ "DP-4" "DP-1" "HDMI-0" ];
        configure_row = [ "HDMI-0" "DP-4" "DP-1" ];
        primary = "DP-4";
        atomic = true;
        execute_after = [
          "${pkgs.xorg.xrandr}/bin/xrandr --dpi 96"
          "${pkgs.xorg.xrandr}/bin/xrandr --output 'DP-4' --mode 1920x1080 --primary --rate 144.00"
          "${pkgs.xorg.xrandr}/bin/xrandr --output 'DP-1' --mode 1920x1080 --rate 119.98"
          "${pkgs.xorg.xrandr}/bin/xrandr --output 'HDMI-0' --mode 1920x1080 --rate 74.97"
        ];
      }
      {
        name = "Dual-screen";
        outputs_connected = [ "DP-4" "HDMI-0" ];
        configure_row = [ "HDMI-0" "DP-4" ];
        primary = "DP-4";
        atomic = true;
        execute_after = [
          "${pkgs.xorg.xrandr}/bin/xrandr --dpi 96"
          "${pkgs.xorg.xrandr}/bin/xrandr --output 'DP-4' --mode 1920x1080 --primary --rate 144.00"
          "${pkgs.xorg.xrandr}/bin/xrandr --output 'HDMI-0' --mode 1920x1080 --rate 74.97"
        ];
      }
      {
        name = "Dual-screen 2";
        outputs_connected = [ "DP-4" "DP-1" ];
        configure_row = [ "DP-4" "DP-1" ];
        primary = "DP-4";
        atomic = true;
        execute_after = [
          "${pkgs.xorg.xrandr}/bin/xrandr --dpi 96"
          "${pkgs.xorg.xrandr}/bin/xrandr --output 'DP-4' --mode 1920x1080 --primary --rate 144.00"
          "${pkgs.xorg.xrandr}/bin/xrandr --output 'DP-1' --mode 1920x1080 --rate 119.98"
        ];
      }
      {
        name = "Single screen";
        outputs_connected = [ "DP-4" ];
        configure_row = [ "DP-4" ];
        primary = true;
        atomic = true;
        execute_after = [
          "${pkgs.xorg.xrandr}/bin/xrandr --dpi 96"
          "${pkgs.xorg.xrandr}/bin/xrandr --output 'DP-4' --mode 1920x1080 --primary --rate 144.00"
        ];
      }

    ];
  };

  # Nicely reload system units when changing configs
  systemd.user.startServices = "sd-switch";

  # https://nixos.wiki/wiki/FAQ/When_do_I_update_stateVersion
  home.stateVersion = "24.05";
}
