**DK public-holiday data source.** Provenance of the calendar used to construct the holiday features.

| Field                      | Value                                                 |
|:---------------------------|:------------------------------------------------------|
| Source                     | Nager.Date v3                                         |
| Endpoint                   | https://date.nager.at/api/v3/PublicHolidays/{year}/DK |
| Country code               | DK                                                    |
| Retrieved (UTC)            | 2026-09-06T15:06:15+00:00                             |
| Years covered              | 2018-2027                                             |
| Holiday-days retrieved (n) | 146                                                   |
| Access                     | Public tier, no API key                               |

*Note.* Retrieved from the free public tier. The commercial nagerholidays.com/api/pro/ paths require a key and return HTTP 401 without one.

---

<!-- INTERNAL REVIEW -- NOT FOR SUBMISSION -->

Cache: `Z:\_dev-ssd\thesis-manifold\01_SRQ1_Model_Training\01_thesis_data\_00_raw\holidays\nager_dk`
Manifest: `Z:\_dev-ssd\thesis-manifold\01_SRQ1_Model_Training\01_thesis_data\_00_raw\holidays\nager_dk_manifest.json`

Per-year sha256 digests in the manifest detect an upstream revision on re-pull. Regenerate with `fetch_holidays.py --force`.
