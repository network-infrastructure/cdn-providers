# Contributing to the CDN Providers Directory & Pricing Calculator

Thank you for helping keep the **CDN Providers Directory & Bandwidth Cost Calculator** accurate, transparent, and up to date!

## How to Submit a Tariff Update or New CDN Provider

1. **Verify Official Public Pricing:**
   - Every CDN provider entry in `providers.json` and `README.md` must link directly to an official pricing or documentation page.
   - If a provider only offers custom enterprise quotes, clearly mark its rate as `Custom / Quote` and provide verified street-price ranges where applicable.

2. **Update `providers.json` and Run the CLI Test Suite:**
   - Add or update the provider's bandwidth rates (`rate_na_eu_gb`, `rate_asia_gb`, `rate_global_blended_gb`, `free_tb_monthly`, `min_monthly_usd`, `request_cost_per_10k`, and `last_verified`).
   - Run the CLI calculator and unit tests locally to verify all calculations:
     ```bash
     python3 cdn_calculator.py --volume-tb 10 --requests-m 50
     python3 -m unittest discover -s tests -v
     ```

3. **Include Verification Date (`YYYY-MM-DD`):**
   - Always update the `last_verified` field to the date you checked the provider's official tariff page.

4. **Open a Pull Request:**
   - Describe the pricing change, new PoP count, or free tier restriction in your PR description with a link to the official announcement or pricing page.
