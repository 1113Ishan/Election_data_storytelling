# Nepal Elections Analytics Dashboard (2082)

## Overview
This project is an end-to-end **data analytics system** built using Nepal’s 2082 election data. It transforms raw constituency-level results into a structured dashboard that explains **who won, how they won, where they dominate, and how competitive the election was**.

The focus is not just reporting results, but delivering **insight-driven political analysis**.

---

## Objectives
- Build a structured SQL-based analytics pipeline  
- Analyze party performance, competitiveness, and geography  
- Design an interactive Power BI dashboard  
- Turn raw data into meaningful insights and storytelling  

---

## Data Model
### Base Table: `elections`
Each row represents a candidate in a constituency.

**Columns:**
- province, district, constituency  
- candidate, party  
- votes, winner (boolean)  
- election_year  

---

## SQL Pipeline

The project follows a layered transformation approach:

1. **Candidate Ranking (`candidate_rank`)**  
   Ranks candidates within each constituency using window functions.

2. **Winner & Runner-Up (`winner_and_runnerup`)**  
   Extracts winner, runner-up, and vote counts.

3. **Win Margin Analysis (`win_margin_analysis`)**  
   Calculates vote difference and win percentage.

4. **Win Classification (`win_classification`)**  
   Categorizes constituencies:
   - Close (<5%)  
   - Competitive (5–25%)  
   - Safe (>25%)  

5. **Party Distribution (`win_status_count`)**  
   Aggregates how parties win (close vs safe vs competitive).

6. **Geographic Distribution (`win_distribution_province`)**  
   Calculates seats per party per province.

Ensures accurate seat counting (1 constituency = 1 seat).

Power BI Model
-----------------

### Fact Tables

*   fact\_winners → winners only
    
*   fact\_constituency\_results → full dataset
    

### Derived Table

*   province\_party
    
    *   province, party
        
    *   seats won, total seats
        
    *   seat share %
        
Dashboard
------------

### Page 1 — National Overview

*   Seats won by party
    
*   Province × Party matrix
    
*   KPI cards (total seats, leading party)
    

### Page 2 — Competitiveness

*   Close vs competitive vs safe wins
    
*   Close constituency analysis
    

### Page 3 — Geography

*   Province-level dominance
    
*   Regional seat distribution
  

### Page 4 — Executive Summary

*   Consolidated insights across all analyses
    

Key Insights
---------------

*   RSP won **125/165 seats (~76%)**, showing strong dominance
    
*   Most seats were **safe wins**, indicating low competition
    
*   **15 constituencies (<5% margin)** reveal tight contests
    
*   Traditional parties retain localized influence
    
*   Geographic patterns show both dominance and regional resistance
    

Tools & Technologies
------------------------

*   PostgreSQL
    
*   SQL (Window functions, aggregations, views)
    
*   Power BI
    
*   DAX
    

Challenges
-------------

*   Fixing incorrect seat aggregation due to duplicates
    
*   Managing DAX context (row vs filter context)
    
*   Handling multi-level grouping (province, district, constituency)
    

🚀 Conclusion
-------------

This project demonstrates how raw election data can be transformed into a **decision-ready analytics system**. It highlights not just results, but the **structure, competitiveness, and geographic dynamics** behind the election.

<img width="1429" height="805" alt="image" src="https://github.com/user-attachments/assets/9c5466ef-3528-435c-bf76-d7528a434536" />
<img width="1431" height="803" alt="image" src="https://github.com/user-attachments/assets/493b673c-e7b8-4bf9-957b-123d9ea0286f" />
<img width="1427" height="800" alt="image" src="https://github.com/user-attachments/assets/10323501-162c-4fb1-bca7-5799eec96a3c" />
<img width="1426" height="807" alt="image" src="https://github.com/user-attachments/assets/59000df0-0fa5-4e25-85e4-b33b8c3b2cbe" />



