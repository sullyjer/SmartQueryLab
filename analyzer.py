from sqlglot import exp


class QueryAnalyzer:
    def __init__(self, parser):
        self.parser = parser
        self.issues = []
        self.suggestions = []

        # Initial score
        self.score = 100

        # Penalty weights
        self.weights = {
            "select_star": 20,
            "missing_where": 15,
            "join_without_on": 25,
            "many_joins": 10,
            "case": 5,
            "fact_without_cte": 15,
            "function_where": 10,
            "or_condition": 8,
            "like_wildcard": 8,
            "order_by": 5,
            "distinct": 5,
            "many_columns": 5,
        }

    def apply_penalty(self, key):
        penalty = self.weights.get(key, 0)
        self.score -= penalty

    def analyze(self):
        # Basic rules
        self.check_select_star()
        self.check_missing_where()
        self.check_joins()

        # Intermediate rules
        self.check_case_usage()
        self.check_many_joins()
        self.check_fact_join()
        self.check_missing_cte_for_fact()

        # Advanced rules
        self.check_functions_in_where()
        self.check_or_conditions()
        self.check_like_wildcard()
        self.check_order_by_without_limit()
        self.check_distinct_usage()
        self.check_many_columns()

        # Ensure score doesn't go below zero
        self.score = max(self.score, 0)

        # Classification
        self.classification = self.get_score_label()

        return self.issues, self.suggestions, self.score, self.classification

    # =========================
    # BASIC RULES
    # =========================

    def check_select_star(self):
        if self.parser.has_select_star():
            self.issues.append("Usage of SELECT * or alias.*")
            self.suggestions.append(
                "Avoid SELECT *. Specify only the required columns."
            )
            self.apply_penalty("select_star")

    def check_missing_where(self):
        if not self.parser.has_where():
            self.issues.append("Query without WHERE clause")
            self.suggestions.append(
                "Add filters to reduce the amount of processed data."
            )
            self.apply_penalty("missing_where")

    def check_joins(self):
        joins = self.parser.get_joins()

        for join in joins:
            if not join.args.get("on"):
                self.issues.append("JOIN without ON condition (possible CROSS JOIN)")
                self.suggestions.append(
                    "Add an ON condition to avoid Cartesian product."
                )
                self.apply_penalty("join_without_on")

    # =========================
    # INTERMEDIATE RULES
    # =========================

    def check_case_usage(self):
        if self.parser.parsed.find(exp.Case):
            self.issues.append("Usage of CASE statement in query")
            self.suggestions.append(
                "CASE expressions may impact performance. Consider moving logic to ETL or precomputed tables."
            )
            self.apply_penalty("case")

    def check_many_joins(self):
        joins = self.parser.get_joins()

        if len(joins) >= 3:
            self.issues.append(f"High number of JOINs detected ({len(joins)})")
            self.suggestions.append(
                "Reduce JOINs or use intermediate aggregations."
            )
            self.apply_penalty("many_joins")

    def check_fact_join(self):
        tables = self.parser.get_tables()

        for table in tables:
            if table.lower().startswith("f"):
                self.issues.append(f"Fact table detected: {table}")
                self.suggestions.append(
                    "JOINs with fact tables can be expensive. Consider reducing data volume."
                )

    def check_missing_cte_for_fact(self):
        tables = self.parser.get_tables()
        joins = self.parser.get_joins()

        has_fact = any(t.lower().startswith("f") for t in tables)
        has_with = self.parser.has_cte()

        if has_fact and joins and not has_with:
            self.issues.append("Fact table used without pre-filtering (missing CTE)")
            self.suggestions.append(
                "Use a CTE (WITH clause) to filter data before applying JOINs."
            )
            self.apply_penalty("fact_without_cte")

    # =========================
    # ADVANCED RULES
    # =========================

    def check_functions_in_where(self):
        where = self.parser.parsed.find(exp.Where)

        if where:
            for node in where.walk():
                if isinstance(node, exp.Anonymous):
                    self.issues.append("Function applied to column in WHERE clause")
                    self.suggestions.append(
                        "Avoid using functions in WHERE clause. This can prevent index usage."
                    )
                    self.apply_penalty("function_where")
                    break

    def check_or_conditions(self):
        where = self.parser.parsed.find(exp.Where)

        if where and where.find(exp.Or):
            self.issues.append("Usage of OR condition in WHERE clause")
            self.suggestions.append(
                "OR conditions may degrade performance. Consider using UNION or IN."
            )
            self.apply_penalty("or_condition")

    def check_like_wildcard(self):
        where = self.parser.parsed.find(exp.Where)

        if where:
            for like in where.find_all(exp.Like):
                pattern = like.args.get("expression")
                if pattern and hasattr(pattern, "this") and str(pattern.this).startswith("%"):
                    self.issues.append("LIKE with leading wildcard detected")
                    self.suggestions.append(
                        "Avoid patterns like '%text'. This prevents index usage."
                    )
                    self.apply_penalty("like_wildcard")
                    break

    def check_order_by_without_limit(self):
        if self.parser.has_order_by() and not self.parser.parsed.find(exp.Limit):
            self.issues.append("ORDER BY used without LIMIT")
            self.suggestions.append(
                "Sorting large datasets can be expensive. Consider limiting results."
            )
            self.apply_penalty("order_by")

    def check_distinct_usage(self):
        if self.parser.has_distinct():
            self.issues.append("Usage of DISTINCT")
            self.suggestions.append(
                "DISTINCT may hide JOIN issues. Review query logic."
            )
            self.apply_penalty("distinct")

    def check_many_columns(self):
        count = self.parser.count_select_columns()

        if count >= 10:
            self.issues.append(f"High number of selected columns ({count})")
            self.suggestions.append(
                "Select only the necessary columns to reduce data processing."
            )
            self.apply_penalty("many_columns")

    # =========================
    # SCORE CLASSIFICATION
    # =========================

    def get_score_label(self):
        if self.score >= 90:
            return "🟢 Excellent"
        elif self.score >= 70:
            return "🟡 Good"
        elif self.score >= 50:
            return "🟠 Fair"
        else:
            return "🔴 Poor"