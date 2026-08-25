# Financial Literacy FAQ Dataset (500 rows)

Summary
-------
This dataset contains 500 Q&A pairs in plain English covering practical financial topics important for users in Africa: budgeting & saving, banking & mobile money, credit & loans, consumer protection & fraud awareness, digital financial literacy, small business & farming finance, insurance & risk, investing basics, and financial planning & retirement. Each row includes a short `Source` label that links to a trusted organization (mapping in `data/sources.csv`).

Key facts
---------
- Total Q&A pairs: 500
- Languages: English (plain-language answers aimed at general audiences)
- Schema: `Category, Question, Answer, Source`

Category distribution (approximate)
----------------------------------
- Budgeting & Saving: ~40
- Banking & Mobile Money: ~60
- Credit & Loans: ~40
- Fraud Prevention & Consumer Protection: ~90
- Digital Financial Literacy: ~60
- Small Business & Farming Finance: ~40
- Insurance & Risk: ~30
- Investing basics: ~30
- Financial Planning & Retirement: ~20
- Financial Rights & Regulations: ~30

Provenance and Sources
----------------------
Sources are short labels that point to reputable organizations and regulator guidance. See `data/sources.csv` for a labeled mapping to canonical URLs. Example sources include the World Bank, IMF, CGAP, GSMA, national central banks (e.g., Reserve Bank of Malawi), FAO/IFAD for agricultural topics, and consumer protection authorities.

Methodology
-----------
- The original file (`data/Financial_Literacy_FAQs_100.csv`) was expanded programmatically to 500 Q&A pairs to produce a balanced set across common themes.
- Answers are concise (1–3 sentences) and include a short source label for traceability. No personal data was used.
- Duplicates and formatting were validated programmatically; all rows were checked for column consistency and duplicate questions.

Usage notes
-----------
- For training or retrieval, prefer `data/Financial_Literacy_FAQs_500.csv` (includes `Source` column).
- If your pipeline expects the older 3-column schema, either update the reader to ignore the `Source` column or use the provided `data/Financial_Literacy_FAQs_en.csv` (not yet created) which can be exported without the `Source` field.

Limitations
-----------
- The dataset was generated and expanded programmatically from curated templates and may need review for local/regional phrasing or regulatory specifics before deployment in a production setting.
- Source labels are high-level references; when publishing or using for evaluation, link to specific documents or pages from `data/sources.csv`.

License & attribution
---------------------
Use this dataset for research, demo, or educational purposes. When deploying or publishing results that use this data, include attribution to the original sources where appropriate.

Contact
-------
For corrections or to contribute additional Q&A pairs, open an issue or PR in this repository.

