import re

from langchain_ollama import ChatOllama


class QueryRouter:

    """
    Hybrid intent router for the Enterprise BI application.

    Routing responsibilities:

        RAG
            Company policies, rules, eligibility, agreements,
            refunds, discounts and other document-based questions.

        ANALYTICS
            Statistical, mathematical, time-series and forecasting
            calculations performed by the Python analytics engine.

        SQL
            Structured business-data questions that require querying
            the SQL Server database.

    High-confidence intents are handled deterministically.
    Ambiguous questions are classified by the local LLM.
    """

    def __init__(self):

        self.llm = ChatOllama(
            model="qwen2.5:3b",
            temperature=0
        )

    # =========================================================
    # NORMALIZATION
    # =========================================================

    @staticmethod
    def _normalize(question: str) -> str:

        question = question.lower().strip()

        question = re.sub(
            r"[^\w\s$%'-]",
            " ",
            question
        )

        question = re.sub(
            r"\s+",
            " ",
            question
        )

        return question

    # =========================================================
    # RAG / POLICY DETECTION
    # =========================================================

    def _is_policy_question(self, q: str) -> bool:

        # -----------------------------------------------------
        # Explicit policy/document language
        # -----------------------------------------------------

        explicit_policy_patterns = [
            r"\bpolicy\b",
            r"\bpolicies\b",
            r"\brule\b",
            r"\brules\b",
            r"\bagreement\b",
            r"\bagreements\b",
            r"\bterms\b",
            r"\bconditions\b",
            r"\beligib\w*\b",
            r"\bapproved\b",
            r"\bapproval\b",
            r"\ballowed\b",
            r"\bpermitted\b",
            r"\brequirements\b",
        ]

        if any(
            re.search(pattern, q)
            for pattern in explicit_policy_patterns
        ):
            return True

        # -----------------------------------------------------
        # Refund / return policy questions
        #
        # These are deliberately semantic patterns rather than
        # simply checking for the word "refund".
        # -----------------------------------------------------

        refund_policy_patterns = [

            # "Can customers get a refund?"
            r"\bcan\b.*\brefund\b",
            r"\bcan\b.*\bget\b.*\brefund\b",
            r"\bcan\b.*\breceive\b.*\brefund\b",

            # "Can I get my money back?"
            r"\bcan\b.*\bget\b.*\bmy\b.*\bmoney\b.*\bback\b",
            r"\bcan\b.*\bget\b.*\bmoney\b.*\bback\b",

            # "Are purchases refundable?"
            r"\bare\b.*\brefund\w*\b",
            r"\bis\b.*\brefund\w*\b",

            # "Is a refund allowed?"
            r"\brefund\b.*\ballowed\b",
            r"\brefund\b.*\bpermitted\b",

            # "What is the refund policy?"
            r"\brefund\b.*\bpolicy\b",

            # "What are the refund rules?"
            r"\brefund\b.*\brules?\b",

            # "Can I return a purchase?"
            r"\bcan\b.*\breturn\b.*\b(purchase|product|item)\b",

            # "What is the return policy?"
            r"\breturn\b.*\bpolicy\b",

            # "Are returns allowed?"
            r"\breturn\w*\b.*\ballowed\b",

            # "Can customers return products?"
            r"\bcan\b.*\bcustomer\w*\b.*\breturn\b",
        ]

        if any(
            re.search(pattern, q)
            for pattern in refund_policy_patterns
        ):
            return True

        # -----------------------------------------------------
        # Discount policy questions
        # -----------------------------------------------------

        discount_policy_patterns = [
            r"\bdiscount\b.*\bpolicy\b",
            r"\bdiscount\b.*\brules?\b",
            r"\bdiscount\b.*\ballowed\b",
            r"\bdiscount\b.*\beligible\b",
            r"\bcan\b.*\bdiscount\b",
            r"\bdo\b.*\boffer\b.*\bdiscount\b",
        ]

        if any(
            re.search(pattern, q)
            for pattern in discount_policy_patterns
        ):
            return True

        # -----------------------------------------------------
        # Generic business-policy questions
        # -----------------------------------------------------

        generic_policy_patterns = [
            r"\bwhat\b.*\b(company|customer|business)\b.*\bpolicy\b",
            r"\bwhat\b.*\brules?\b.*\bcustomer",
            r"\bwhat\b.*\bterms\b",
            r"\bwhat\b.*\brequirements\b",
            r"\bwhat\b.*\beligib\w*\b",
            r"\bwho\b.*\beligib\w*\b",
        ]

        if any(
            re.search(pattern, q)
            for pattern in generic_policy_patterns
        ):
            return True

        return False

    # =========================================================
    # ANALYTICS DETECTION
    # =========================================================

    def _is_analytics_question(self, q: str) -> bool:

        analytics_patterns = [

            # Average
            r"\baverage\b.*\border\b",
            r"\baverage\b.*\bsales\b",
            r"\baverage\b.*\brevenue\b",

            # Standard deviation / variability
            r"\bstandard deviation\b",
            r"\bstd\b",
            r"\bvariab\w*\b",
            r"\bvariability\b",
            r"\bvariation\b",
            r"\bvariance\b",
            r"\bspread\b.*\bsales\b",
            r"\bspread\b.*\brevenue\b",
            r"\bhow much\b.*\b(vary|differ|fluctuate)\b",
            r"\bhow\b.*\bspread out\b",
            r"\bhow\b.*\bvolatile\b",

            # Trends
            r"\btrend\b",
            r"\btrending\b",
            r"\bgrowth\b",
            r"\bgrowing\b",
            r"\bdeclin\w*\b",
            r"\bchange\b.*\bover time\b",

            # Forecasting / prediction
            r"\bforecast\b",
            r"\bforecasting\b",
            r"\bpredict\b",
            r"\bprediction\b",
            r"\bexpected\b.*\brevenue\b",
            r"\bexpect\b.*\brevenue\b",
            r"\bnext month\b",
            r"\bfuture\b.*\brevenue\b",

            # Revenue by month
            r"\bwhich month\b.*\bhighest\b.*\brevenue\b",
            r"\bwhich month\b.*\blowest\b.*\brevenue\b",
            r"\bhighest\b.*\brevenue\b.*\bmonth\b",
            r"\blowest\b.*\brevenue\b.*\bmonth\b",
            r"\bbest\b.*\bsales month\b",
            r"\bworst\b.*\bsales month\b",
        ]

        return any(
            re.search(pattern, q)
            for pattern in analytics_patterns
        )

    # =========================================================
    # SQL DETECTION
    # =========================================================

    def _is_sql_question(self, q: str) -> bool:

        sql_patterns = [

            # Customers
            r"\bcustomer\b",
            r"\bcustomers\b",
            r"\bbiggest customers?\b",
            r"\btop customers?\b",

            # Products
            r"\bproduct\b",
            r"\bproducts\b",
            r"\bbest[- ]selling\b",

            # Orders
            r"\border\b",
            r"\borders\b",

            # Regions / geography
            r"\bregion\b",
            r"\bregions\b",
            r"\bgeographical\b",
            r"\bgeographic\b",
            r"\barea\b",
            r"\blocation\b",
            r"\blocations\b",

            # Structured sales questions
            r"\btotal sales\b",
            r"\btotal revenue\b",
            r"\bsales revenue\b",
            r"\brevenue by\b",
            r"\bsales by\b",

            # Quantity
            r"\bquantity\b",
            r"\bunits\b",

            # Rankings
            r"\bwhich\b.*\b(customer|product|region|area|location)\b",
            r"\bwho\b.*\b(customer|customers)\b",

            # Counts
            r"\bhow many\b.*\borders?\b",
            r"\bhow many\b.*\bcustomers?\b",
            r"\bhow many\b.*\bproducts?\b",

            # Structured comparisons
            r"\bcompare\b.*\b(customer|customers|products?|regions?)\b",
        ]

        return any(
            re.search(pattern, q)
            for pattern in sql_patterns
        )

    # =========================================================
    # LLM FALLBACK
    # =========================================================

    def _llm_route(self, question: str) -> str:

        prompt = f"""
You are an intent classifier for an Enterprise Business
Intelligence application.

Classify the user's question into EXACTLY ONE route:

SQL
RAG
ANALYTICS

==================================================
RAG
==================================================

Choose RAG when the user is asking about:

- company policies
- business rules
- customer rules
- refund rules
- return rules
- discount rules
- eligibility
- agreements
- terms and conditions
- what the company allows or permits
- information contained in business documents

Examples:

Can customers get a refund?
RAG

Can I get my money back?
RAG

Are purchases refundable?
RAG

What is the refund policy?
RAG

Are customers eligible for a discount?
RAG

What are the customer eligibility rules?
RAG

==================================================
SQL
==================================================

Choose SQL when the user wants information from structured
business records/database data.

Examples:

Which customers generated the most revenue?
SQL

Who were our biggest customers?
SQL

Which product sold the most?
SQL

Which region generated the highest revenue?
SQL

Which geographical area brought in the most money?
SQL

How many orders did we receive?
SQL

What are our total sales?
SQL

Important:

Questions asking WHICH CUSTOMER, WHICH PRODUCT, WHICH REGION,
WHICH AREA, WHICH LOCATION or WHO generated a business result
are SQL when they refer to actual business data.

==================================================
ANALYTICS
==================================================

Choose ANALYTICS when the user asks for:

- averages
- standard deviation
- variability
- variance
- spread
- trends
- growth
- forecasting
- prediction
- time-series analysis
- highest/lowest revenue by MONTH

Examples:

What is the average order value?
ANALYTICS

How much do our sales vary?
ANALYTICS

What is the standard deviation of sales?
ANALYTICS

How is revenue trending?
ANALYTICS

What is next month's revenue forecast?
ANALYTICS

Which month had the highest revenue?
ANALYTICS

==================================================
IMPORTANT
==================================================

Classify according to the user's INTENT, not individual words.

"refund" does not automatically mean SQL.

"customer" does not automatically mean RAG.

"revenue" does not automatically mean ANALYTICS.

A policy question about a refund is RAG.

A database question about customers who received refunds is SQL.

A statistical question about revenue is ANALYTICS.

Return ONLY:

SQL

RAG

or

ANALYTICS

User question:
{question}

Route:
"""

        try:

            response = self.llm.invoke(prompt)

            route = response.content.strip().upper()

            # Protect against responses such as:
            # "The correct route is SQL"
            if "RAG" in route:
                return "RAG"

            if "ANALYTICS" in route:
                return "ANALYTICS"

            if "SQL" in route:
                return "SQL"

        except Exception:
            pass

        # Safe default for structured BI questions
        return "SQL"

    # =========================================================
    # PUBLIC ROUTING METHOD
    # =========================================================

    def route(self, question: str) -> str:

        q = self._normalize(question)

        if not q:
            return "SQL"

        # -----------------------------------------------------
        # Priority 1: Policy / document intent
        #
        # This is deliberately evaluated first so that:
        #
        # "Can customers get a refund?"
        #
        # cannot accidentally become SQL simply because the
        # question contains "customers".
        # -----------------------------------------------------

        if self._is_policy_question(q):
            return "RAG"

        # -----------------------------------------------------
        # Priority 2: Mathematical / statistical / predictive
        # -----------------------------------------------------

        if self._is_analytics_question(q):
            return "ANALYTICS"

        # -----------------------------------------------------
        # Priority 3: Structured business data
        # -----------------------------------------------------

        if self._is_sql_question(q):
            return "SQL"

        # -----------------------------------------------------
        # Priority 4: LLM semantic fallback
        #
        # Handles natural-language questions that do not match
        # the high-confidence patterns above.
        # -----------------------------------------------------

        return self._llm_route(question)