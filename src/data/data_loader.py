"""
資料載入器 - 從 BigQuery 載入資料
"""

from typing import Optional

import pandas as pd

from .bigquery_client import BigQueryClient, get_client

DATASET = "`bigquery-public-data.stackoverflow`"


class DataLoader:
    """資料載入器"""

    def __init__(self, client: Optional[BigQueryClient] = None):
        self.client = client or get_client()
        self._cache = {}

    def load_users(self, limit: int = 100, user_ids: list = None) -> pd.DataFrame:
        """載入用戶資料（含聲望等級分類）

        聲望等級（研究方法規格）:
        - 1_Low: 新手 (<1,000)
        - 2_Medium: 中階 (1,000~10,000)
        - 3_Senior: 資深 (10,000~50,000)
        - 4_Expert: 大神 (>50,000)
        """
        if user_ids:
            user_ids_str = ",".join(str(uid) for uid in user_ids)
            cache_key = f"users_by_ids_{hash(user_ids_str)}"
        else:
            cache_key = f"users_{limit}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        if user_ids:
            chunks = [user_ids[i : i + 1000] for i in range(0, len(user_ids), 1000)]
            in_clauses = " OR ".join(
                f"id IN ({','.join(str(uid) for uid in chunk)})" for chunk in chunks
            )
            sql = f"""
            SELECT
                id,
                display_name,
                reputation,
                up_votes,
                down_votes,
                views,
                creation_date,
                location,
                CASE
                    WHEN reputation < 1000 THEN '1_Low'
                    WHEN reputation BETWEEN 1000 AND 10000 THEN '2_Medium'
                    WHEN reputation BETWEEN 10001 AND 50000 THEN '3_Senior'
                    WHEN reputation > 50000 THEN '4_Expert'
                    ELSE '0_None'
                END AS reputation_level
            FROM {DATASET}.users
            WHERE {in_clauses}
            """
        else:
            sql = f"""
            SELECT
                id,
                display_name,
                reputation,
                up_votes,
                down_votes,
                views,
                creation_date,
                location,
                CASE
                    WHEN reputation < 1000 THEN '1_Low'
                    WHEN reputation BETWEEN 1000 AND 10000 THEN '2_Medium'
                    WHEN reputation BETWEEN 10001 AND 50000 THEN '3_Senior'
                    WHEN reputation > 50000 THEN '4_Expert'
                    ELSE '0_None'
                END AS reputation_level
            FROM {DATASET}.users
            WHERE reputation IS NOT NULL
            LIMIT {limit}
            """
        df = self.client.query(sql)
        self._cache[cache_key] = df
        return df

    def load_posts_with_answers(
        self, limit: int = 100, only_accepted: bool = True
    ) -> pd.DataFrame:
        """載入問題與回答關係（含解答時間等級）

        解答時間等級（研究方法規格）:
        - 1_VeryFast: <1小時
        - 2_Fast: 1~12小時
        - 3_Slow: 12~24小時
        - 4_VerySlow: >24小時
        - 0_Unresolved: 未解決
        """
        cache_key = f"posts_{limit}_{only_accepted}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        if only_accepted:
            sql = f"""
            SELECT
                q.id AS question_id,
                q.owner_user_id AS questioner_id,
                q.accepted_answer_id,
                q.score AS question_score,
                q.answer_count,
                q.creation_date AS question_date,
                q.tags,
                a.id AS answer_id,
                a.owner_user_id AS answerer_id,
                a.creation_date AS answer_date,
                TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) AS hours_to_accept,
                CASE
                    WHEN TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) < 1 THEN '1_VeryFast'
                    WHEN TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) BETWEEN 1 AND 12 THEN '2_Fast'
                    WHEN TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) BETWEEN 13 AND 24 THEN '3_Slow'
                    WHEN TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) > 24 THEN '4_VerySlow'
                    ELSE '0_Unresolved'
                END AS answer_time_level
            FROM {DATASET}.posts_questions q
            INNER JOIN {DATASET}.posts_answers a
                ON q.accepted_answer_id = a.id
            WHERE q.accepted_answer_id IS NOT NULL
              AND EXTRACT(YEAR FROM q.creation_date) = 2021
            LIMIT {limit}
            """
        else:
            sql = f"""
            SELECT
                q.id AS question_id,
                q.owner_user_id AS questioner_id,
                q.accepted_answer_id,
                q.score AS question_score,
                q.answer_count,
                q.creation_date AS question_date,
                q.tags,
                a.id AS answer_id,
                a.owner_user_id AS answerer_id,
                a.creation_date AS answer_date,
                TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) AS hours_to_accept,
                CASE
                    WHEN TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) < 1 THEN '1_VeryFast'
                    WHEN TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) BETWEEN 1 AND 12 THEN '2_Fast'
                    WHEN TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) BETWEEN 13 AND 24 THEN '3_Slow'
                    WHEN TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) > 24 THEN '4_VerySlow'
                    ELSE '0_Unresolved'
                END AS answer_time_level
            FROM {DATASET}.posts_questions q
            LEFT JOIN {DATASET}.posts_answers a
                ON q.id = a.parent_id
            WHERE q.post_type_id = 1
              AND EXTRACT(YEAR FROM q.creation_date) = 2021
            LIMIT {limit}
            """
        df = self.client.query(sql)
        self._cache[cache_key] = df
        return df

    def load_tag_cooccurrence(self, limit: int = 100) -> pd.DataFrame:
        """載入標籤共現關係"""
        cache_key = f"tags_{limit}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        sql = f"""
        SELECT
            tag1,
            tag2,
            COUNT(*) AS co_occurrence_count
        FROM (
            SELECT
                q.id,
                t1 AS tag1,
                t2 AS tag2
            FROM {DATASET}.posts_questions q,
                 UNNEST(SPLIT(q.tags, '|')) AS t1,
                 UNNEST(SPLIT(q.tags, '|')) AS t2
            WHERE q.tags IS NOT NULL AND q.tags != ''
              AND EXTRACT(YEAR FROM q.creation_date) = 2021
        )
        WHERE tag1 < tag2 AND tag1 != '' AND tag2 != ''
        GROUP BY tag1, tag2
        ORDER BY co_occurrence_count DESC
        LIMIT {limit}
        """
        df = self.client.query(sql)
        self._cache[cache_key] = df
        return df

    def load_user_connectivity(
        self, limit: int = 100, user_ids: list = None
    ) -> pd.DataFrame:
        """載入用戶連通性（識別知識孤島）"""
        if user_ids:
            user_ids_str = ",".join(str(uid) for uid in user_ids)
            cache_key = f"connectivity_by_ids_{hash(user_ids_str)}"
        else:
            cache_key = f"connectivity_{limit}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        if user_ids:
            chunks = [user_ids[i : i + 1000] for i in range(0, len(user_ids), 1000)]
            in_clauses = " OR ".join(
                f"u.id IN ({','.join(str(uid) for uid in chunk)})" for chunk in chunks
            )
            sql = f"""
            SELECT
                u.id AS user_id,
                u.display_name,
                u.reputation,
                COUNT(DISTINCT p.id) AS post_count,
                COUNT(DISTINCT c.id) AS comment_count,
                (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id)) AS total_interactions,
                CASE
                    WHEN (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id)) = 0 THEN '1_Isolated'
                    WHEN (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id)) BETWEEN 1 AND 5 THEN '2_Low'
                    WHEN (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id)) BETWEEN 6 AND 20 THEN '3_Medium'
                    ELSE '4_Active'
                END AS connectivity_level
            FROM {DATASET}.users u
            LEFT JOIN {DATASET}.posts_questions p ON u.id = p.owner_user_id AND EXTRACT(YEAR FROM p.creation_date) = 2021
            LEFT JOIN {DATASET}.comments c ON u.id = c.user_id AND EXTRACT(YEAR FROM c.creation_date) = 2021
            WHERE {in_clauses}
            GROUP BY u.id, u.display_name, u.reputation
            ORDER BY total_interactions ASC
            LIMIT {limit}
            """
        else:
            sql = f"""
            SELECT
                u.id AS user_id,
                u.display_name,
                u.reputation,
                COUNT(DISTINCT p.id) AS post_count,
                COUNT(DISTINCT c.id) AS comment_count,
                (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id)) AS total_interactions,
                CASE
                    WHEN (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id)) = 0 THEN '1_Isolated'
                    WHEN (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id)) BETWEEN 1 AND 5 THEN '2_Low'
                    WHEN (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id)) BETWEEN 6 AND 20 THEN '3_Medium'
                    ELSE '4_Active'
                END AS connectivity_level
            FROM {DATASET}.users u
            LEFT JOIN {DATASET}.posts_questions p ON u.id = p.owner_user_id AND EXTRACT(YEAR FROM p.creation_date) = 2021
            LEFT JOIN {DATASET}.comments c ON u.id = c.user_id AND EXTRACT(YEAR FROM c.creation_date) = 2021
            GROUP BY u.id, u.display_name, u.reputation
            ORDER BY total_interactions ASC
            LIMIT {limit}
            """
        df = self.client.query(sql)
        self._cache[cache_key] = df
        return df

    def load_posts_with_code(self, limit: int = 100) -> pd.DataFrame:
        """載入包含程式碼區塊的貼文"""
        cache_key = f"code_{limit}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        sql = f"""
        SELECT
            id,
            title,
            score,
            view_count,
            answer_count,
            comment_count,
            creation_date,
            tags,
            CASE
                WHEN REGEXP_CONTAINS(body, r'```') THEN 1
                WHEN REGEXP_CONTAINS(body, r'<code>') THEN 1
                ELSE 0
            END AS has_code_block,
            CASE
                WHEN score <= -5 THEN '1_VeryNegative'
                WHEN score BETWEEN -4 AND -1 THEN '2_Negative'
                WHEN score = 0 THEN '3_Neutral'
                WHEN score BETWEEN 1 AND 5 THEN '4_Positive'
                WHEN score BETWEEN 6 AND 20 THEN '5_VeryPositive'
                ELSE '6_ExtremelyPositive'
            END AS score_level
        FROM {DATASET}.posts_questions
        WHERE body IS NOT NULL
          AND EXTRACT(YEAR FROM creation_date) = 2021
        LIMIT {limit}
        """
        df = self.client.query(sql)
        self._cache[cache_key] = df
        return df

    def load_account_age(self, limit: int = 100, user_ids: list = None) -> pd.DataFrame:
        """載入帳號年資與發文類型"""
        if user_ids:
            user_ids_str = ",".join([str(uid) for uid in user_ids[:1000]])
            cache_key = f"age_by_ids_{user_ids_str}"
        else:
            cache_key = f"age_{limit}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        if user_ids:
            sql = f"""
            SELECT
                u.id AS user_id,
                u.display_name,
                u.reputation,
                u.creation_date AS account_creation_date,
                DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) AS account_age_days,
                COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) AS question_count,
                COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) AS answer_count,
                CASE
                    WHEN COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) > 0
                        AND COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) > 0
                    THEN '1_Both'
                    WHEN COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) > 0
                        AND COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) = 0
                    THEN '2_QuestionsOnly'
                    WHEN COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) = 0
                        AND COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) > 0
                    THEN '3_AnswersOnly'
                    ELSE '4_Neither'
                END AS post_type,
                CASE
                    WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) < 365 THEN '1_New'
                    WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) BETWEEN 365 AND 1095 THEN '2_Young'
                    WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) BETWEEN 1096 AND 2190 THEN '3_Mature'
                    WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) BETWEEN 2191 AND 3650 THEN '4_Established'
                    ELSE '5_Senior'
                END AS account_age_level
            FROM {DATASET}.users u
            LEFT JOIN (
                SELECT id, owner_user_id, post_type_id FROM {DATASET}.posts_questions WHERE EXTRACT(YEAR FROM creation_date) = 2021
                UNION ALL
                SELECT id, owner_user_id, post_type_id FROM {DATASET}.posts_answers WHERE EXTRACT(YEAR FROM creation_date) = 2021
            ) p ON u.id = p.owner_user_id
            WHERE u.id IN ({user_ids_str})
            GROUP BY u.id, u.display_name, u.reputation, u.creation_date
            """
        else:
            sql = f"""
            SELECT
                u.id AS user_id,
                u.display_name,
                u.reputation,
                u.creation_date AS account_creation_date,
                DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) AS account_age_days,
                COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) AS question_count,
                COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) AS answer_count,
                CASE
                    WHEN COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) > 0
                        AND COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) > 0
                    THEN '1_Both'
                    WHEN COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) > 0
                        AND COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) = 0
                    THEN '2_QuestionsOnly'
                    WHEN COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) = 0
                        AND COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) > 0
                    THEN '3_AnswersOnly'
                    ELSE '4_Neither'
                END AS post_type,
                CASE
                    WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) < 365 THEN '1_New'
                    WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) BETWEEN 365 AND 1095 THEN '2_Young'
                    WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) BETWEEN 1096 AND 2190 THEN '3_Mature'
                    WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) BETWEEN 2191 AND 3650 THEN '4_Established'
                    ELSE '5_Senior'
                END AS account_age_level
            FROM {DATASET}.users u
            LEFT JOIN (
                SELECT id, owner_user_id, post_type_id FROM {DATASET}.posts_questions WHERE EXTRACT(YEAR FROM creation_date) = 2021
                UNION ALL
                SELECT id, owner_user_id, post_type_id FROM {DATASET}.posts_answers WHERE EXTRACT(YEAR FROM creation_date) = 2021
            ) p ON u.id = p.owner_user_id
            GROUP BY u.id, u.display_name, u.reputation, u.creation_date
            ORDER BY account_age_days DESC
            LIMIT {limit}
            """
        df = self.client.query(sql)
        self._cache[cache_key] = df
        return df

    def load_tags_popularity(self, limit: int = 100) -> pd.DataFrame:
        """載入標籤熱度"""
        cache_key = f"tags_popularity_{limit}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        sql = f"""
        SELECT
            tag_name,
            count AS usage_count,
            excerpt_post_id,
            wiki_post_id
        FROM {DATASET}.tags
        ORDER BY count DESC
        LIMIT {limit}
        """
        df = self.client.query(sql)
        self._cache[cache_key] = df
        return df

    def clear_cache(self):
        """清除快取"""
        self._cache.clear()
