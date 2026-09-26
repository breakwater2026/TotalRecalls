# Paddle + Courier setup — SUPERSEDED

**Read `PADDLE_COURIER_FULFILLMENT_STATUS.md` instead.** It is the verified, current state
(re-checked live against Paddle, Cloudflare and Courier on 2026-09-26).

The previous version of this file was wrong in ways that cost real time:

| It said | Reality |
|---|---|
| Webhook URL `https://paddle-fulfillment-worker.sparkling-paradox.workers.dev/webhook` | That subdomain is **dead** (DNS `100::`). The live destination is `https://totalrecalls.app/webhook/paddle` |
| Worker name `paddle-fulfillment-worker` | The deployed script is named **`paddle-webhook`** |
| "Status: LIVE (configured)" | It was live but wrote nothing to D1 and could not fulfill a single order |
| Secrets were "placeholders to replace" | Now actually set: `PADDLE_WEBHOOK_SECRET`, `COURIER_API_KEY`, `COURIER_TEMPLATE_ID`, `PADDLE_API_KEY` — verified through the worker's `/health` |

Facts from here that are still true:

- **Notification destination**: `ntfset_01m39f0thgb00rgdfpwdw9hs9k`, events `transaction.created`,
  `transaction.completed`, `transaction.updated`, API version 1
- **Product**: `pro_01m37qgm5hgzv7tfrg519884ds` (TotalRecalls)
- **Price**: `pri_01m37qpx77bst2w1gnf3zkf4zd` — one-time, 3 installations, $48.00 USD
- **Launch discount**: `dsc_01m39879ga7pv9zg0gsvzqsmjw` — 50% off → $24
- **Courier template**: `nt_01m3f2b6rxeh1vrqmmy25zfxaq` ("TotalRecalls License Key")

**Do not chase a "Couriers URL."** It does not exist. Courier is an external email API
(`https://api.courier.com/send`) — not a Cloudflare resource, so nothing in the Cloudflare
account can find it. The `couriers.gadget.app/api/licenses` URL an earlier session recorded was
invented, and the worker no longer references it.
