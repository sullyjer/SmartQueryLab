import sqlglot
from sqlglot import exp


class QueryParser:
    def __init__(self, query: str):
        self.query = query

        # Converte query para AST (árvore)
        self.parsed = sqlglot.parse_one(query)

    # =========================
    # SELECT *
    # =========================
    def has_select_star(self) -> bool:
        for select in self.parsed.find_all(exp.Select):
            for projection in select.expressions:
                if isinstance(projection, exp.Star):
                    return True
                if isinstance(projection, exp.Column) and projection.name == "*":
                    return True
        return False

    # =========================
    # WHERE
    # =========================
    def has_where(self) -> bool:
        return self.parsed.find(exp.Where) is not None

    # =========================
    # JOINS
    # =========================
    def get_joins(self):
        return list(self.parsed.find_all(exp.Join))

    # =========================
    # TABELAS
    # =========================
    def get_tables(self):
        tables = []
        for table in self.parsed.find_all(exp.Table):
            tables.append(table.name)
        return tables

    # =========================
    # DETECTAR CTE (WITH)
    # =========================
    def has_cte(self):
        return self.parsed.find(exp.With) is not None

    # =========================
    # COUNT COLUNAS SELECT
    # =========================
    def count_select_columns(self):
        select = self.parsed.find(exp.Select)
        if not select:
            return 0
        return len(select.expressions)

    # =========================
    # DETECTAR ORDER BY
    # =========================
    def has_order_by(self):
        return self.parsed.find(exp.Order) is not None

    # =========================
    # DETECTAR DISTINCT
    # =========================
    def has_distinct(self):
        select = self.parsed.find(exp.Select)
        return select and select.args.get("distinct") is not None