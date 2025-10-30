{ pkgs }: {
  deps = [
    pkgs.python310Full
    pkgs.python310Packages.pip
    pkgs.nodejs_22
    pkgs.nodePackages.npm
  ];
}
