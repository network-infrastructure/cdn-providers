import unittest
from cdn_calculator import estimate_monthly_cost, filter_providers, load_data


class TestCDNCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.data = load_data()
        self.providers = self.data["providers"]

    def test_providers_loaded_and_verified(self) -> None:
        self.assertGreaterEqual(len(self.providers), 28)
        for p in self.providers:
            self.assertIn("name", p)
            self.assertIn("pricing_url", p)
            self.assertEqual(p.get("last_verified"), "2026-11-15")

    def test_cost_calculation_free_tiers(self) -> None:
        by_id = {p["id"]: p for p in self.providers}
        # AWS CloudFront 1 TB + 10M requests should be $0.00 under Always Free tier
        self.assertEqual(estimate_monthly_cost(by_id["aws-cloudfront"], 1.0, 10.0, "na-eu"), 0.0)
        # Gcore 1 TB + 1M requests should be $0.00 under Always Free tier
        self.assertEqual(estimate_monthly_cost(by_id["gcore"], 1.0, 1.0, "na-eu"), 0.0)
        # jsDelivr open-source CDN is $0.00 at any volume
        self.assertEqual(estimate_monthly_cost(by_id["jsdelivr"], 100.0, 500.0, "global"), 0.0)

    def test_cost_calculation_bunny(self) -> None:
        by_id = {p["id"]: p for p in self.providers}
        # Bunny Standard 10 TB in NA/EU at $0.01/GB = $100.00
        self.assertEqual(estimate_monthly_cost(by_id["bunny-standard"], 10.0, 25.0, "na-eu"), 100.0)
        # Bunny Volume 10 TB at $0.005/GB = $50.00
        self.assertEqual(estimate_monthly_cost(by_id["bunny-volume"], 10.0, 25.0, "global"), 50.0)

    def test_filter_by_category_and_free(self) -> None:
        opensource = filter_providers(self.providers, category="opensource")
        self.assertGreaterEqual(len(opensource), 5)
        free_list = filter_providers(self.providers, free_only=True)
        self.assertGreaterEqual(len(free_list), 10)


if __name__ == "__main__":
    unittest.main()
