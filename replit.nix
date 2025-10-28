{ pkgs }: {
  deps = [
    pkgs.python310Full
    pkgs.python310Packages.pip
    pkgs.nodejs_20
    pkgs.nodePackages.npm
  ];
}
