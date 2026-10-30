# Deployment record and procedure

Stage A is Cloudflare Pages Free, Render Free and Neon Free. No paid services or synthetic keep-alive are authorized. The existing Neon free organization contains project `sanjivani-pilot` in Singapore, with separate pilot and development branches. Credentials stay in private environment files and provider secret storage.

No frontend or backend URL has yet been verified. Render authorization and signed-in Cloudflare/Google Cloud setup remain required. This document will be updated with actual URLs and test evidence after deployment.

`render.yaml` configures Python/Gunicorn, static collection, migrations and a public health check. Secrets include DATABASE_URL, DJANGO_SECRET_KEY, PROXY_SECRET, MAINTENANCE_SECRET and TOKEN_ENCRYPTION_KEY. Set APP_ORIGIN to the exact Pages origin, ALLOWED_HOSTS to the Render host, and DEBUG=0. Never expose these as Vite variables.

Pages builds `frontend` using `npm ci && npm run build`; output `dist`, Functions directory `functions`. Configure BACKEND_ORIGIN and PROXY_SECRET as server-side bindings. Use fail-closed behavior when Functions allowance is exhausted. SPA navigation uses Pages' default fallback; do not put a top-level 404.html in the build.

Verification must run through the actual Pages URL: HTTPS, routing, login, Set-Cookie persistence, logout, CSRF rejection/success, all roles, booking conflict, financial correction, authorization failures, protected backend boundary and cold-start retries. Record only synthetic data. Repeat secure-cookie verification on the deployed origin; localhost tests are insufficient.

Stage B requires explicit approval to change the existing Render service to Starter. Verify current price (the amendment estimates USD 7/month), preserve service URL/secrets/database, deploy the reviewed revision and measure memory/latency. Then configure a legitimate one-minute business-maintenance scheduler with `POST /api/maintenance/` and a secret Authorization header. Never put the token in the URL. Reconciliation remains a fallback. No paid upgrade or production scheduler has been executed.

References checked on 2026-10-28: [Render free behavior](https://render.com/docs/free), [Render pricing](https://render.com/pricing), [Pages Functions routing](https://developers.cloudflare.com/pages/functions/routing/), [Neon free tier announcement](https://neon.com/blog/neon-free-plan-1-gb-per-project).
