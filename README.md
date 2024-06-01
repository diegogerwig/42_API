# 42evaluators

Welcome to the **42evaluators** GitHub repository!

## Running

We use [devenv](https://devenv.sh) for development. It provides an easy way to
install and setup PostgreSQL (it's probably also possible to setup PostgreSQL
separately. You might have to modify `internal/database/db.go` adequately).

Once you've downloaded it, run `devenv up -d`. This runs PostgreSQL in the background
(you can also remove the `-d` if you want to inspect the logs). Afterwards, you
can enter the development shell with `devenv shell`.

You need to fill `.env`. It contains credentials to connect to your account,
which you can find in the "Storage" tab of the Devtools while you're on the 42 intra,
to create API keys (to prevent rate limiting, because 42evaluators requires
doing a LOT of API requests). See `.env.example`.

Finally, you can use the Makefile to launch 42evaluators: `make`

This will generate API keys, and start fetching a bunch of stuff (such as
projects, which takes a lot of time...). You can open up `localhost:8080`.
