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

  # TODO: Set your username
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
      nix-update-boot = "cd ~/github-projects/nix-shulgi && sudo nixos-rebuild switch --flake .#nyarlathotep";
      nix-clean = "nix-env --delete-generations old && nix-store --gc && sudo nixos-rebuild boot --flake .#nyarlathotep";
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

  # Zoxide config
  programs.zoxide = {
    enable = true;
    enableZshIntegration = true;
    options = ["--cmd cd"];
  };


  # Nicely reload system units when changing configs
  systemd.user.startServices = "sd-switch";

  # https://nixos.wiki/wiki/FAQ/When_do_I_update_stateVersion
  home.stateVersion = "24.05";
}
