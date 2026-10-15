#!/usr/bin/env bash
set -euo pipefail
repo=pfxamd/KINETONE
root="$(cd "$(dirname "$0")" && pwd)"
command -v gh >/dev/null;command -v git >/dev/null
gh auth status >/dev/null
[[ "$(find "$root/docs/assets/img" -maxdepth 1 -name '*.webp' | wc -l)" -eq 28 ]] || { echo "Expected 28 images";exit 1; }
tmp="$(mktemp -d)";trap 'rm -rf "$tmp"' EXIT
git clone "https://github.com/$repo.git" "$tmp/KINETONE"
cd "$tmp/KINETONE"
git checkout -B main
if ! git rev-parse --verify HEAD >/dev/null 2>&1;then
 printf '# KINETONE\n' >README.md
 git add README.md
 git -c user.name=pfxamd -c user.email=pfxamd@users.noreply.github.com commit -m 'Initialize KINETONE repository'
 git push -u origin main
fi
if ! gh api "repos/$repo/pages" >/dev/null 2>&1; then gh api -X POST "repos/$repo/pages" -f build_type=workflow >/dev/null || true;fi
for f in docs assets tools .github README.md .gitignore publish-pages.ps1 publish-pages.bat publish-pages.sh; do if [[ -e "$root/$f" ]];then rm -rf "$f";cp -r "$root/$f" "$f";fi;done
git add -A
if ! git diff --cached --quiet;then git -c user.name=pfxamd -c user.email=pfxamd@users.noreply.github.com commit -m 'Launch complete KINETONE interactive website';fi
git push -u origin main
echo 'Website: https://pfxamd.github.io/KINETONE/'
