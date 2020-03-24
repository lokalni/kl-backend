#!/bin/bash
set -e


# TODO - add secrets loading?

if [[ $1 =~ ^(/bin/)?(ba)?sh$ ]]; then
  echo "* First CMD argument is a shell: $1"
  echo "* Running: exec ${@@Q}"
  exec "$@"
elif [[ "$*" =~ ([;<>]|\(|\)|\&\&|\|\|) ]]; then
  echo "* Shell metacharacters detected, passing CMD to bash"
  _quoted="$*"
  echo "* Running: exec /bin/bash -c ${_quoted@Q}"
  unset _quoted
  exec /bin/bash -c "$*"
fi

# Use dumb-init to ensure proper handling of signals, zombies, etc.
# See https://github.com/Yelp/dumb-init

echo "* Running command: /usr/local/bin/dumb-init ${@@Q}"
exec dumb-init "$@"