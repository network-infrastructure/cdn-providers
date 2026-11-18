# CDN Bandwidth Cost Calculator: 1 TB vs 10 TB vs 50 TB vs 100 TB vs 500 TB (2026)

> **Last Verified:** `2026-11-15` • [Back to Main CDN Directory](../README.md) • [Interactive Web Calculator](https://network-infrastructure.github.io/cdn-providers/cdn-pricing-calculator.html)

When comparing **CDN providers**, per-GB list prices rarely tell the full story. Minimum monthly fees, free tier allowances, regional multipliers (Asia/LATAM vs North America/Europe), and **per-10,000 HTTP request charges** can swing your monthly bill by **10x to 100x**.

---

## 1. Real-World Monthly Cost Comparison (NA/EU Traffic)

All calculations below use `1 TB = 1,000 GB` and assume **25M HTTP/HTTPS requests at 10 TB** (scaling proportionally) using public self-serve pricing verified on `2026-11-15`.

| CDN Provider | 1 TB/mo | 10 TB/mo | 50 TB/mo | 100 TB/mo | 500 TB/mo | Request Fees? | Official Tariff |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Cloudflare R2 + CDN** | **$0** | **$15** | **$45** | **$90** | **$360** | Class B uncached only | [R2 Pricing →](https://developers.cloudflare.com/r2/pricing/) |
| **Hetzner S3 + Cloudflare** | **$5.39** | **$14.39** | **$54.39** | **$104.39** | **$504.39** | None | [Hetzner →](https://www.hetzner.com/cloud/object-storage/) |
| **Bunny.net (Volume)** | **$5** | **$50** | **$250** | **$450** | **$1,500** | **$0 (None)** | [Bunny.net →](https://bunny.net/pricing/) |
| **BlazingCDN** | **$5** | **$50** | **$225** | **$400** | **$1,500** | **$0 (None)** | [BlazingCDN →](https://blazingcdn.com/pricing/) |
| **Bunny.net (Standard)** | **$10** | **$100** | **$500** | **$1,000** | **$5,000** | **$0 (None)** | [Bunny.net →](https://bunny.net/pricing/) |
| **DigitalOcean Spaces** | **$5** | **$95** | **$495** | **$995** | **$4,995** | **$0 (None)** | [DO Spaces →](https://www.digitalocean.com/pricing/spaces-object-storage) |
| **Oracle Cloud (OCI)** | **$0** | **$0** | **$340** | **$765** | **$4,165** | **$0 (None)** | [Oracle OCI →](https://www.oracle.com/cloud/networking/pricing/) |
| **Gcore CDN** | **$0** | **$180** | **$450** | **$750** | **$2,000** | Free plan 1M cap | [Gcore →](https://gcore.com/pricing/cdn) |
| **CDN77** | **$199** | **$199** | **$650** | **$990** | **$2,250** | **$0 (None)** | [CDN77 →](https://www.cdn77.com/pricing) |
| **KeyCDN** | **$40** | **$400** | **$1,600** | **$2,600** | **$6,600** | **$0 (None)** | [KeyCDN →](https://www.keycdn.com/pricing) |
| **Google Cloud CDN** | **$85** | **$810** | **$2,950** | **$5,450** | **$16,500** | `$0.0075/10k` | [Google Cloud →](https://cloud.google.com/cdn/pricing) |
| **Amazon CloudFront** | **$0** | **$775** | **$4,015** | **$7,515** | **$26,500** | `$0.01/10k` | [CloudFront →](https://aws.amazon.com/cloudfront/pricing/) |
| **Azure Front Door** | **$116** | **$855** | **$3,600** | **$6,800** | **$24,000** | `$0.01/10k` + `$35` | [Azure →](https://azure.microsoft.com/en-us/pricing/details/frontdoor/) |
| **Fastly CDN** | **$75** | **$1,150** | **$4,600** | **$8,200** | **$29,000** | `$0.0075/10k` | [Fastly →](https://www.fastly.com/pricing/) |
| **Vercel Edge** | **$20** | **$1,370** | **$7,370** | **$14,870** | **$74,870** | `$0.02/10k` | [Vercel →](https://vercel.com/pricing) |
| **Netlify Edge** | **$19** | **$4,969** | **$26,969** | **$54,469** | **$274,469** | None | [Netlify →](https://www.netlify.com/pricing/) |

---

## 2. How to Run Custom Calculations in CLI

Use `cdn_calculator.py` to model your exact traffic profile (including **Asia-Pacific** or **Global Blended** routing and high-request API workloads):

```bash
# Compare costs for 35 TB/month and 200M requests in Asia-Pacific
python3 cdn_calculator.py --volume-tb 35 --requests-m 200 --region asia

# Compare only Pay-As-You-Go CDNs at 75 TB/month
python3 cdn_calculator.py --category payg --volume-tb 75
```

---

## 3. FinOps Rule of Thumb by Volume Tier

* **0 to 1 TB/month:** Use **Cloudflare Free**, **AWS CloudFront** (1 TB Always Free), or **Gcore** (1 TB Always Free).
* **1 to 25 TB/month:** **Bunny.net Standard** (`$0.01/GB`), **Bunny.net Volume** (`$0.005/GB`), **DigitalOcean Spaces** (`$5` + `$0.01/GB`), or **Cloudflare R2** (`$0` egress).
* **50 to 500+ TB/month:** **Bunny.net Volume** (`$0.002–$0.005/GB`), **CDN77**, **CacheFly**, or **Cloudflare R2**, or negotiate a custom **AWS CloudFront Security Savings Bundle** if locked into AWS.
