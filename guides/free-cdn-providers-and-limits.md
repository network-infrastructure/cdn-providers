# Free CDN Providers & Hidden Restrictions Compared (2026)

> **Last Verified:** `2026-11-15` • [Back to Main CDN Directory](../README.md) • [Interactive Web Calculator](https://ktif77.github.io/cdn-providers/free-cdn-providers.html)

Many developers assume a **"Free CDN"** means unlimited free file hosting. In reality, every major free CDN enforces strict **Terms of Service (ToS)**, **monthly TB caps**, **HTTP request limits**, or **non-commercial clauses**. Exceeding them can result in either **account suspension** or a **surprise $500–$5,000+ overage invoice**.

---

## 1. Best 100% Free CDN Providers by Use Case (Verified 2026-11-15)

| Free CDN Provider | Free Bandwidth / Quota | Request / File Limits | Commercial OK? | Official Free Tier Docs |
| :--- | :--- | :--- | :---: | :--- |
| **Cloudflare Free** | Unlimited HTML/CSS/JS | 100 MB max upload/file | ✅ Yes | [cloudflare.com/plans](https://www.cloudflare.com/plans/) |
| **Cloudflare R2** | **10 GB storage + ∞ Egress** | 1M Class A + 10M Class B/mo | ✅ Yes | [developers.cloudflare.com/r2](https://developers.cloudflare.com/r2/pricing/) |
| **Cloudflare Pages** | Unlimited static sites | 25 MB/file • 20k files | ✅ Yes | [pages.cloudflare.com](https://pages.cloudflare.com/) |
| **Oracle Cloud (OCI)** | **10 TB/mo Always Free** | 4 ARM cores + 200 GB SSD | ✅ Yes | [oracle.com/cloud/networking](https://www.oracle.com/cloud/networking/pricing/) |
| **Amazon CloudFront** | **1 TB/mo Always Free** | 10,000,000 HTTP/S reqs/mo | ✅ Yes | [aws.amazon.com/cloudfront](https://aws.amazon.com/cloudfront/pricing/) |
| **Gcore CDN** | **1 TB/mo Always Free** | 1,000,000 requests/mo | ✅ Yes | [gcore.com/pricing/cdn](https://gcore.com/pricing/cdn) |
| **Fastly Developer** | **$50/mo Always Free** | ~400 GB NA/EU or ~4M reqs | ✅ Yes | [fastly.com/pricing](https://www.fastly.com/pricing/) |
| **Netlify Starter** | 100 GB/mo | 300 build mins/mo | ✅ Yes | [netlify.com/pricing](https://www.netlify.com/pricing/) |
| **Vercel Hobby** | 100 GB/mo | 1M Edge Requests/mo | ❌ **Non-Commercial** | [vercel.com/pricing](https://vercel.com/pricing) |
| **ImageKit.io** | 20 GB/mo | Unlimited image transforms | ✅ Yes | [imagekit.io/plans](https://imagekit.io/plans/) |
| **Cloudinary** | 25 Credits/mo (~25 GB) | Shared with transforms/storage | ✅ Yes | [cloudinary.com/pricing](https://cloudinary.com/pricing) |
| **QUIC.cloud** | 10–20 GB/mo | LiteSpeed origin required | ✅ Yes | [quic.cloud/cost](https://quic.cloud/cost/) |
| **jsDelivr / cdnjs** | Unlimited (Fair Use) | Public OSS npm/GitHub only | ✅ Yes | [jsdelivr.com](https://www.jsdelivr.com/) |

---

## 2. The 4 Biggest Free CDN Traps to Avoid

### Trap #1: Serving Video or Large Downloads on Cloudflare's Free Proxy
Cloudflare's *Service-Specific Terms* prohibit serving disproportionate volumes of video, audio, or non-HTML binary archives through its standard CDN proxy on Free/Pro/Business plans.
* **The Fix:** Store large files, MP4s, game assets, or backups on **Cloudflare R2** (`$0.00/GB` egress, 10 GB free) or **Backblaze B2** (`$6/TB/mo` + `$0.00/GB` egress to Cloudflare/Bunny via the Bandwidth Alliance).

### Trap #2: Netlify's `$55 per 100 GB` ($0.55/GB) Overage Billing
Netlify Starter includes 100 GB/month, and Netlify Pro ($19/mo) includes 1 TB/month. Once you cross that threshold, Netlify automatically bills **$55 per 100 GB ($0.55/GB)** — which is **55x more expensive** than Bunny.net ($0.01/GB) or DigitalOcean Spaces ($0.01/GB).
* **The Fix:** Use **Cloudflare Pages** (unlimited static bandwidth) or offload heavy images/PDFs/videos to **Bunny.net** or **Cloudflare R2**.

### Trap #3: AWS CloudFront & Fastly Request Fees on Small Assets
Even if your bandwidth stays small, serving millions of tiny 5 KB JSON API responses or thumbnails triggers per-request billing:
* **AWS CloudFront:** `$0.01` per 10,000 HTTPS requests after 10M free/mo (`100M reqs = $90` in request fees alone).
* **Fastly:** `$0.0075–$0.016` per 10,000 requests once you exceed the `$50/mo` free developer credit.
* **The Fix:** **Bunny.net**, **Gcore**, **CDN77**, and **KeyCDN** charge **$0.00 per HTTP request**.

### Trap #4: Vercel Hobby Commercial Ban
Vercel's Free Hobby tier explicitly forbids commercial websites, SaaS landing pages, or monetized blogs.
* **The Fix:** Upgrade to Vercel Pro ($20/mo), or deploy commercial static/Jamstack sites to **Cloudflare Pages** or **DigitalOcean App Platform** (3 free static sites).

---

## 3. Recommended Zero-Cost Production Stacks

1. **Static Site / SaaS Frontend:** `Cloudflare Pages` (Unlimited bandwidth) + `jsDelivr` (public npm libs).
2. **WordPress / WooCommerce:** `Cloudflare Free` (DNS + WAF) + `QUIC.cloud` (if on LiteSpeed) or `Bunny.net` (`$1/mo` min) for media offload.
3. **Downloads / Game Patches / Media (<10 TB/mo):** `Oracle Cloud OCI` (`10 TB/mo` free egress) or `Cloudflare R2` (`$0/GB` egress) + `Backblaze B2`.
