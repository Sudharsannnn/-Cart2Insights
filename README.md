# -Cart2Insights
End-to-end e-commerce analytics project exploring sales performance, customer behavior, product trends, delivery efficiency, and customer satisfaction using Python, SQL, data visualization, and an interactive Streamlit dashboard.


**Transforming raw e-commerce data into actionable business insights through data analytics, statistical exploration, and interactive visualization.**

1. Project Overview

Cart2Insights is an end-to-end e-commerce analytics project built to investigate the business performance of an online retail marketplace using real-world transactional data. The project focuses on understanding how sales evolve over time, how customers interact with the platform, which products and categories generate the most revenue, how sellers contribute to marketplace performance, and how delivery experiences relate to customer satisfaction.

The project follows a structured analytical workflow, starting with raw data exploration and quality assessment, followed by data cleaning, feature engineering, exploratory data analysis, statistical analysis, and interactive dashboard development.

Rather than treating data analysis as a collection of isolated charts, Cart2Insights connects multiple aspects of e-commerce operations to answer practical business questions and communicate findings in a form that business stakeholders can understand.

The final goal is to demonstrate how a data analyst can convert complex transactional records into a coherent view of business performance and identify opportunities for further investigation and operational improvement.

2. Business Problem

E-commerce platforms generate large amounts of data across orders, customers, products, sellers, payments, reviews, and deliveries. Although these records contain valuable information, they are distributed across multiple tables and may contain missing values, duplicates, inconsistent records, and other data-quality issues.

Without a structured analytical process, it can be difficult to answer questions such as:

- Is revenue growing or declining over time?
- Which product categories contribute most to sales?
- Which customer regions generate the greatest business activity?
- Do customers tend to purchase only once or return for additional orders?
- How do delivery timelines vary across orders and regions?
- Is there an observable relationship between delivery duration and customer review scores?
- Which sellers and product categories stand out across selected performance metrics?

Cart2Insights addresses these questions by organizing the data, applying consistent analytical methods, and presenting relevant metrics through an interactive dashboard.

3. Project Objectives

    Sales and Revenue Analysis
- Examine monthly revenue trends and order volumes.
- Calculate key business indicators such as total revenue and average order value.
- Compare revenue across product categories and customer regions.
- Identify products and categories with high sales contributions.

    Customer Behavior Analysis
- Explore customer distribution across geographical regions.
- Investigate customer spending patterns.
- Distinguish between one-time and repeat customers using order history.
- Identify purchasing patterns that may support customer retention analysis.

    Product and Seller Performance
- Compare product categories based on revenue and sales volume.
- Examine seller contributions to marketplace activity.
- Identify high-performing sellers using clearly defined metrics.
- Explore differences between product popularity and revenue contribution.

    Delivery and Operational Performance
- Analyze delivery durations and delivery status.
- Investigate delivery performance across geographical regions.
- Examine changes in delivery duration over time.
- Explore potential relationships between delivery experience and review scores.

   Customer Satisfaction
- Analyze the distribution of customer review scores.
- Compare review scores across product categories.
- Investigate whether delivery duration is associated with differences in customer feedback.
- Highlight potential areas for further customer-experience analysis.

4. Dataset Description

This project uses the **Brazilian E-Commerce Public Dataset by Olist**, available on Kaggle.

**Dataset source:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

The dataset contains anonymized marketplace records covering orders, customers, products, sellers, payments, reviews, and geographical information.

The original dataset includes multiple related tables, including:

| Dataset | Analytical purpose |
|---|---|
| Customers | Customer identification and geographical distribution |
| Orders | Order status, purchase timestamps, and delivery milestones |
| Order Items | Products purchased, seller information, prices, and freight charges |
| Products | Product attributes and category information |
| Sellers | Seller identification and geographical information |
| Order Payments | Payment types and payment values |
| Order Reviews | Customer feedback and review scores |
| Product Category Translation | Product category labels and translations |
| Geolocation | Geographical information associated with postal-code prefixes |

The tables are connected through their respective identifiers to support analysis across different parts of the marketplace.

**Data handling:** The raw and cleaned CSV files are not included in this GitHub repository because of their size. Users who wish to reproduce the analysis should obtain the original dataset from the source and follow the cleaning workflow documented in the notebooks.

5. Technology Stack

Technology & Purpose 

Python | Core analytical programming 
Pandas | Data manipulation, cleaning, grouping, and aggregation 
NumPy | Numerical operations and analytical calculations 
SQL | Structured querying and business analysis 
Jupyter Notebook | Step-by-step analysis and documentation 
Plotly | Interactive charts and data visualization 
Streamlit | Interactive dashboard development 
Matplotlib / Seaborn | Statistical and exploratory visualizations, where used 

The final dependency list should be maintained in `requirements.txt` based on the libraries actually imported by the project.

6. Analytical Workflow

Phase 1 — Data Understanding

**Notebook:** `01_data_understanding.ipynb`

The initial phase examines the dataset structure and establishes an understanding of the available information.

Activities include:
- Loading the source datasets.
- Reviewing dataset dimensions, column names, and data types.
- Inspecting sample records.
- Understanding table relationships and identifiers.
- Identifying the fields required for downstream analysis.

**Outcome:** A documented understanding of the available datasets and their analytical relevance.

Phase 2 — Data Quality Assessment

**Notebook:** `02_data_quality_analysis.ipynb`

Before drawing business conclusions, the data must be assessed for quality issues.

Activities include:
- Checking missing values by column.
- Identifying duplicate records.
- Reviewing inconsistent or unexpected values.
- Examining data types and timestamp fields.
- Investigating potential data-quality problems that could affect analytical accuracy.

**Outcome:** A clearer understanding of the data-quality limitations and the cleaning decisions required.

Phase 3 — Data Cleaning and Preparation

**Notebook:** `03_data_cleaning.ipynb`

This phase prepares the datasets for reliable analysis while preserving important information.

Activities include:
- Applying documented missing-value handling rules.
- Removing or managing duplicate records where appropriate.
- Correcting data types and preparing date-time columns.
- Standardizing selected fields.
- Saving processed datasets for subsequent analytical stages.

Cleaning decisions should be evaluated according to each column's meaning rather than applying one rule to every missing value.

**Outcome:** Cleaned datasets suitable for analysis, with important data limitations documented.

Phase 4 — SQL Business Analysis

**Notebook:** `04_sql_analysis.ipynb`

SQL is used to express business questions through structured queries and aggregations.

The analytical focus includes:
- Revenue and order-related metrics.
- Grouped analysis by product category and other business dimensions.
- Customer and seller performance comparisons.
- Aggregations that support business reporting.

The exact queries and metrics are documented in the notebook.

**Outcome:** Structured query-based analysis that supports repeatable business reporting.

Phase 5 — Feature Engineering

**Notebook:** `05_feature_engineering.ipynb`

Feature engineering derives analytical variables from existing fields.

Depending on the analysis requirements, this may include:
- Extracting month and year from timestamps.
- Calculating order-level revenue measures.
- Deriving delivery duration from relevant order timestamps.
- Classifying customers using order history.
- Creating analytical groupings for comparative analysis.

Derived variables must be based on valid source fields and clearly defined calculation rules.

**Outcome:** Additional variables that make business patterns easier to investigate.

Phase 6 — Exploratory Data Analysis

**Notebook:** `06_eda.ipynb`

Exploratory data analysis investigates the distribution and behavior of key business metrics.

Areas of investigation include:
- Revenue trends over time.
- Order and customer activity.
- Product and category performance.
- Regional sales patterns.
- Seller contributions.
- Delivery performance.
- Customer review patterns.

Charts and grouped summaries help reveal patterns, differences, and potential anomalies that may require further investigation.

**Outcome:** A visual and descriptive understanding of the dataset and the business questions it can address.

Phase 7 — Statistical Analysis

**Notebook:** `07_statistical_analysis.ipynb`

Statistical analysis extends descriptive exploration by examining numerical distributions and relationships between relevant variables.

Depending on the implemented analyses, this can include:
- Descriptive statistics.
- Distribution analysis.
- Comparison of selected groups.
- Examination of associations between delivery duration and review scores.
- Statistical interpretation of observed patterns.

An observed association does not, by itself, establish causation. Statistical conclusions should reflect the methods, assumptions, and limitations documented in the notebook.

**Outcome:** A more structured interpretation of selected patterns and relationships.

Phase 8 — Interactive Dashboard

**Application:** `streamlit/app.py`

The Streamlit dashboard brings important analytical metrics and visualizations into one interactive interface. It is intended to make the analysis easier to explore without requiring users to read every notebook.

7. Dashboard Modules

The dashboard is organized around six analytical areas.

 7.1 Business Overview
Provides a high-level view of marketplace performance using metrics such as:
- Total revenue, based on the implemented revenue definition.
- Total orders, customers, and sellers.
- Average order value.
- Average review score.
- Monthly revenue trends.

7.2 Sales Analysis
Explores sales performance through:
- Monthly revenue trends.
- Revenue by product category.
- Top products by units sold.
- Revenue distribution across customer states.
  
7.3 Customer Analysis
Focuses on customer activity and spending:
- Customer distribution by state.
- Highest-spending customers.
- One-time versus repeat purchasing behavior.
- Comparisons of customer activity across available dimensions.

7.4 Seller and Product Analysis
Investigates marketplace supply-side performance:
- Sellers ranked by revenue.
- Product category performance.
- Product sales comparisons.
- Seller review metrics, subject to the minimum-review threshold implemented in the dashboard.

7.5 Delivery Analysis
Examines operational delivery indicators:
- On-time and delayed delivery classifications.
- Average delivery duration over time.
- Delivery duration by state.
- Differences in delivery performance across available groups.

7.6 Customer Experience
Connects customer feedback with other marketplace indicators:
- Review-score distribution.
- Average ratings across selected product categories.
- Delivery duration compared with review scores.
- A summary of analytical observations and potential business implications.

Dashboard metrics should be interpreted according to their definitions, filtering rules, and treatment of incomplete records.

8. Key Business Questions

The project is structured to investigate the following questions:

1. How does revenue change over time?
2. Which product categories contribute most to marketplace revenue?
3. Which products lead in sales volume, and how does that compare with revenue contribution?
4. How does customer activity vary by region?
5. What proportion of customers place repeat orders?
6. Which sellers contribute most to the selected sales metrics?
7. How do delivery durations vary over time and across regions?
8. How are customer review scores distributed?
9. Is delivery duration associated with customer review scores?
10. What data-quality limitations should be considered before using the results for business decisions?

These questions connect the technical work to practical business analysis.

9. Key Findings and Business Insights

The final findings should be populated from the validated outputs of the notebooks and dashboard. Each finding should include a measured result, its interpretation, and any relevant limitations.

Recommended format:

| Area | Finding to document | Business relevance |
|---|---|---|
| Revenue | Validated monthly revenue trend and period of highest activity | Supports sales monitoring and planning |
| Product categories | Leading categories by revenue and/or sales volume | Helps distinguish high-value categories from high-volume categories |
| Customer behavior | Measured share of one-time and repeat customers | Provides context for retention analysis |
| Regional performance | States or regions with the highest measured activity | Supports geographical performance comparisons |
| Delivery | Measured delivery-duration patterns and delay rates | Highlights potential operational improvement areas |
| Customer satisfaction | Review-score patterns and validated relationships with delivery duration | Helps prioritize further customer-experience investigation |

**Important:** These are reporting areas, not pre-established conclusions. Actual values and findings should be added only after checking the analytical outputs. Revenue is not the same as profit, and a relationship between delivery duration and review scores should not be presented as proof of causation.

 10. Repository Structure


Cart2Insights_project1/
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_quality_analysis.ipynb
│   ├── 03_data_cleaning.ipynb
│   ├── 04_sql_analysis.ipynb
│   ├── 05_feature_engineering.ipynb
│   ├── 06_eda.ipynb
│   └── 07_statistical_analysis.ipynb
│
├── streamlit/
│   └── app.py
│
├── .gitignore
├── requirements.txt
└── README.md


The raw and cleaned data directories are maintained locally and excluded from the repository. The structure above describes the main tracked project files; optional local configuration files are not shown.

11. Setup and Reproducibility

### Prerequisites

Install:
- Python 3.10 or another Python version supported by the project's dependencies.
- Git.
- Jupyter Notebook or VS Code with Jupyter support.

The exact Python version and package versions should be documented after verifying the environment used to run the project.

### Step 1 — Clone the Repository


git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Cart2Insights


Replace the placeholder URL with the repository's actual GitHub URL.

Step 2 — Create a Virtual Environment

On Windows:

powershell
python -m venv .venv
.venv\Scripts\Activate.ps1


If PowerShell blocks activation, use the Python executable inside venv directly or follow the appropriate environment-activation instructions for your system.

Step 3 — Install Dependencies

Once requirements.txt has been verified and committed:

bash
python -m pip install -r requirements.txt


Step 4 — Obtain the Dataset

Download the Brazilian E-Commerce Public Dataset from the Kaggle source linked above.

Place the required source CSV files in the expected local data directory. Confirm the exact filenames and paths by reviewing the data-loading cells in the notebooks before running them.

Step 5 — Run the Notebooks

Open the project in VS Code or Jupyter and execute the notebooks in the documented analytical order, beginning with data understanding and data-quality assessment.

Some later notebooks may depend on cleaned datasets or features created by earlier notebooks. Run prerequisite stages first and confirm that expected output files are generated.

Step 6 — Launch the Dashboard

From the project root:

bash
python -m streamlit run streamlit/app.py


Open the local URL displayed in the terminal.

**Note:** Dashboard setup may require additional local data configuration depending on how the application loads its data. Review `streamlit/app.py` before assuming the dashboard works immediately after cloning.

12. Data Governance and Security

The repository is intended to contain project code and documentation, not private configuration or large source datasets.

- Raw and cleaned datasets are excluded from version control.
- Credentials, passwords, API keys, and local secrets must not be committed.
- Local configuration files should be excluded using `.gitignore`.
- Notebook outputs and code cells should be checked for sensitive information before publishing.
- Dataset limitations and cleaning assumptions should be documented to make the analysis more transparent.

Before making the repository public, verify that no sensitive credentials or private information appear in tracked files or notebook outputs.

13. Limitations and Future Improvements

Potential next steps include:
- Adding automated data-quality checks.
- Improving reproducibility with verified dependency versions.
- Adding more robust validation for derived metrics.
- Extending customer segmentation and repeat-purchase analysis.
- Exploring more detailed delivery-performance factors.
- Improving dashboard filters and explanatory annotations.
- Adding automated tests for key analytical calculations.
- Documenting measured business findings with charts and supporting values.
- Evaluating deployment options after confirming the dashboard's data dependencies.

These improvements would strengthen the reliability, maintainability, and practical value of the project.

14. Conclusion

Cart2Insights demonstrates a structured approach to e-commerce data analysis, connecting data preparation, SQL-based querying, feature engineering, exploratory analysis, statistical investigation, and dashboard development.

The project emphasizes the importance of data quality, clearly defined metrics, and responsible interpretation of analytical results. By combining a documented analytical workflow with an interactive dashboard, it provides a foundation for exploring marketplace performance and communicating evidence-based insights.

---

**Project:** Cart2Insights — Decoding E-Commerce Performance  
**Domain:** E-Commerce Analytics and Business Intelligence  
**Dataset:** Brazilian E-Commerce Public Dataset by Olist  
**Focus:** Sales
