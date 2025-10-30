{ pkgs }: {
  deps = [
    pkgs.python310Full
    pkgs.python310Packages.pip
    pkgs.nodejs-22_x
    pkgs.nodePackages.npm
  ];
}
