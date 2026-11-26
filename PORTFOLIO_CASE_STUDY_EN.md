# Accounting export to a Persian management dashboard — conceptual demonstration

**Problem:** Show what a Persian, RTL management report could look like if a hypothetical accounting export from Shayan were available. No authentic Shayan file, API, license, specification, or database was used; no commercial affiliation is implied. The column mapping is an unverified analytical proposal, not an actual integration contract.

**Approach:** Fixed-seed synthetic sales, receipts, bills and balanced journal lines feed a local five-page Streamlit prototype. A proposed dimension-to-fact star schema, illustrative DAX, a Power BI build guide, a theme and automated quality controls are included. As of 2025-03-20, amounts are integer IRR and aging is based on outstanding amount and due date. The ledger and sales data are independently generated and are not reconciled to each other.

**Evidence:** 1,500 balanced journal documents comprise 3,000 lines, with 649,279,581,770 IRR on each side; 2,500 synthetic invoices; local tests and five-page AppTest. See `VALIDATION.md` for exactly what was and was not tested.

**Limitations:** This is not a production integration, financial advice, proof of vendor compatibility, a PBIX deliverable, or a claim of ROI. For real deployment, obtain authorized exports under suitable confidentiality, validate field mapping and controls with the relevant experts, implement ETL, and test the resulting model in Power BI Desktop.
