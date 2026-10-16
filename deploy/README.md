# Deploying Model Compass

How the public instance runs: one Docker container on a Linux host,
reached through the host's existing Cloudflare Tunnel at a hostname such
as `modelcompass.lcaitech.com`. No port is opened on the host, Cloudflare
terminates HTTPS, and the container is capped at 256 MB of RAM and half
a CPU so it doesn't crowd other projects on the same machine.

The app has no database and no background jobs: it loads `dataset/` at
startup and answers each request in memory. One worker is enough.

## Prerequisites on the host

- Docker Engine with the Compose plugin (`docker compose version`).
- A clone of this repository (for example `~/model-compass`).
- A running `cloudflared` container for the tunnel, managed from the
  Cloudflare Zero Trust dashboard.

## First deploy

1. **Find the tunnel's Docker network.**

   ```bash
   docker ps --format '{{.Names}}\t{{.Image}}' | grep -i cloudflared
   docker inspect <cloudflared-container> --format '{{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}'
   ```

2. **Point the compose file at it.**

   ```bash
   cp deploy/.env.example deploy/.env
   # edit deploy/.env: TUNNEL_NETWORK=<network from step 1>
   ```

3. **Build and start.**

   ```bash
   docker compose -f deploy/compose.yaml up -d --build
   docker compose -f deploy/compose.yaml ps      # wait for "healthy"
   docker stats --no-stream model-compass        # memory and CPU use
   ```

4. **Publish the hostname.** In Cloudflare Zero Trust → Networks →
   Tunnels → your tunnel → Public Hostname → Add:
   subdomain `modelcompass`, domain `lcaitech.com`, service type `HTTP`,
   URL `model-compass:8000`. Cloudflare creates the DNS record itself.

   If the tunnel is configured locally (a `config.yml` with `ingress:`
   rules) instead of from the dashboard, add the equivalent rule above the
   final catch-all and restart `cloudflared`:

   ```yaml
   - hostname: modelcompass.lcaitech.com
     service: http://model-compass:8000
   ```

## Updating

```bash
git pull
docker compose -f deploy/compose.yaml up -d --build
```

Dataset edits (prices, new models, retirements) ship the same way: the
dataset is read at startup, so a rebuild picks them up. When
`tests/test_catalog_dates.py` starts failing because a dated fact has
passed, fix the dataset, merge, and redeploy; until then the public site
keeps showing the old value.

To roll back, check out the previous commit and run the same `up -d
--build`. To stop it: `docker compose -f deploy/compose.yaml down`.
