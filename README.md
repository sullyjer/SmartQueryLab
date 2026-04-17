# 🚀 SmartQueryLab

## SQL Performance Risk Analyzer (Local-first Tool)

---

## 📌 Overview

**SmartQueryLab** is a Python-based tool designed to analyze SQL queries and identify potential performance issues **without executing them**.

Instead of calculating real execution cost, the tool focuses on:

👉 **Performance risk detection using static analysis**

It evaluates the structure of SQL queries and provides:

* Identified issues
* Optimization suggestions
* A performance score (0–100)
* A qualitative classification

---

## 🎯 Purpose

The goal of SmartQueryLab is to help:

* Data analysts
* BI developers
* SQL users

quickly identify **anti-patterns and inefficiencies** in queries before running them against large datasets.

---

## ⚠️ Important Concept

SmartQueryLab does NOT:

* Execute queries
* Access databases
* Measure real execution cost

Instead, it estimates:

```text
Performance Risk (heuristic-based)
```

---

## 🧠 How It Works

```text
SQL Query
   ↓
Parser (AST via sqlglot)
   ↓
Analyzer (rule-based engine)
   ↓
Output:
  - Issues
  - Suggestions
  - Score
  - Classification
```

---

## 🧩 Architecture

### 1. Parser (`parser.py`)

Responsible for transforming SQL into a structured format (AST).

Uses:

* `sqlglot`

Provides methods such as:

* `has_select_star()`
* `has_where()`
* `get_joins()`
* `get_tables()`
* `has_cte()`
* `count_select_columns()`
* `has_order_by()`
* `has_distinct()`

---

### 2. Analyzer (`analyzer.py`)

Core engine of the application.

Applies heuristic rules to detect performance risks.

---

#### 🔹 Basic Rules

* Usage of `SELECT *`
* Missing `WHERE`
* JOIN without `ON`

---

#### 🔹 Intermediate Rules

* CASE expressions
* Multiple JOINs
* Fact table detection (prefix `f`)
* Missing CTE for fact tables

---

#### 🔹 Advanced Rules

* Functions inside WHERE clause
* OR conditions
* LIKE with leading wildcard (`%value`)
* ORDER BY without LIMIT
* DISTINCT usage
* Excessive number of columns

---

## 📊 Scoring System

Each detected issue reduces the score from an initial value of 100.

Example:

```text
Score: 60/100
```

---

### Penalty Model

Each rule has a weight:

```text
select_star: 20
missing_where: 15
join_without_on: 25
many_joins: 10
case: 5
fact_without_cte: 15
function_where: 10
or_condition: 8
like_wildcard: 8
order_by: 5
distinct: 5
many_columns: 5
```

---

## 🏷️ Score Classification

```text
90–100 → 🟢 Excellent
70–89  → 🟡 Good
50–69  → 🟠 Fair
<50    → 🔴 Poor
```

---

## 🖥️ User Interface

The tool provides a local web interface built with:

* Streamlit

Features:

* SQL input box
* Analyze button
* Clear button
* Real-time feedback

---

## 🎨 UI Design

Custom styling includes:

* Color palette:

  * Dark blue: `#1a4683`
  * Light blue: `#a0d1ff`
  * Blue: `#2581c4`
  * Green: `#2ccf63`
  * Red: `#de6a73`

* Font:

  * Baloo Chettan 2

---

## ▶️ Running Locally

### Requirements

* Python 3.10+
* pip

---

### Install dependencies

```bash
pip install -r requirements.txt
```

---

### Run the app

```bash
python -m streamlit run app.py
```

---

### Access in browser

```text
http://localhost:8501
```

---

## 🧑‍💻 Running Without Python (Windows)

A `.bat` launcher is included:

```text
run_app.bat
```

Double-click to start the application.

---

## 📁 Project Structure

```text
SmartQueryLab/
│
├── app.py              # Streamlit UI
├── parser.py           # SQL parsing logic
├── analyzer.py         # Rule engine + scoring
├── requirements.txt
├── run_app.bat
```

---

## ⚠️ Known Limitations

* No database awareness
* No index detection
* No execution plan analysis
* No real cost estimation
* Heuristic-based approach

---

## 🚀 Future Improvements

Planned features:

* Severity classification (Critical / Medium / Low)
* Natural language explanations
* Query highlighting
* Export results (PDF / JSON)
* API (FastAPI)
* Multi-user support
* Integration with real databases (EXPLAIN)

---

## 💡 Project Positioning

SmartQueryLab is best described as:

```text
SQL Performance Risk Analyzer
```

Not:

* Query optimizer
* Database tuning engine
* Execution planner

---

## 🤝 Contribution

Contributions are welcome.

Ideas:

* New rules
* Better heuristics
* UI improvements
* Integration features


