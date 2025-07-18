docker compose  --env-file ../build/.env.dev -f ../build/compose.yml -f ../build/compose.dev.yml down --remove-orphans
docker compose  --env-file ../build/.env.dev -f ../build/compose.yml -f ../build/compose.dev.yml up --build --watch

