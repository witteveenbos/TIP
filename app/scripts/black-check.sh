# Run Python style checker
black  --exclude "^.*\b(migrations)\b.*$" "$( dirname "$0"; )/../src/"

