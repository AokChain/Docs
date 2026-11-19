#!/bin/sh
# Copy build/ to the web server. The target lives in .deploy.env, which is
# not in git (this repository is public):
#   AOK_DEPLOY_HOST=user@host
#   AOK_DEPLOY_DIR=/path/on/the/server/
#   AOK_DEPLOY_KEY=/path/to/ssh/key      (optional)
#   AOK_DEPLOY_BASE=/doc/                (optional, default /doc/)
# Run tools/build.py first. The build must have been made for the base the
# server serves it under.
set -eu
cd "$(dirname "$0")/.."
[ -f .deploy.env ] && . ./.deploy.env
: "${AOK_DEPLOY_HOST:?set AOK_DEPLOY_HOST in .deploy.env}"
: "${AOK_DEPLOY_DIR:?set AOK_DEPLOY_DIR in .deploy.env}"
: "${AOK_DEPLOY_BASE:=/doc/}"
SSH="ssh -o BatchMode=yes"
[ -n "${AOK_DEPLOY_KEY:-}" ] && SSH="$SSH -i $AOK_DEPLOY_KEY"

if [ ! -f build/.wiki-build.json ] || [ ! -f build/index.html ]; then
  echo "build/ is empty: run tools/build.py first" >&2
  exit 1
fi
if ! grep -q "\"base\": \"$AOK_DEPLOY_BASE\"" build/.wiki-build.json; then
  echo "build/ was not made for base $AOK_DEPLOY_BASE: run tools/build.py --base $AOK_DEPLOY_BASE" >&2
  exit 1
fi

# A folder that holds the wiki of the launch names the website's address in
# .site; a build for another address (the test values of wiki.yml) is refused.
BUILT=$(grep -o 'rel="canonical" href="[^"]*"' build/index.html | sed 's#.*href="\(https*://[^/"]*\).*#\1#')
THERE=$($SSH "$AOK_DEPLOY_HOST" "cat '${AOK_DEPLOY_DIR%/}/.site' 2>/dev/null" || true)
if [ -n "$THERE" ] && [ "$THERE" != "$BUILT" ]; then
  echo "the server holds the wiki for $THERE and build/ is for $BUILT: not deployed" >&2
  echo "(build with --launch, or make the launch values the values of wiki.yml)" >&2
  exit 1
fi

rsync -rlt --delete --delay-updates --chmod=D755,F644 --exclude='.*' -e "$SSH" build/ "$AOK_DEPLOY_HOST:${AOK_DEPLOY_DIR%/}/"
echo "deployed build/ ($(grep -o '"pages": [0-9]*' build/.wiki-build.json)) to the server"
