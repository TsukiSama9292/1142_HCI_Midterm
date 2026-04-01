"""
BigQuery Stack Overflow 數據查詢範例

使用 BigQuery 公共數據集進行社會網路分析
"""

import json
import subprocess
from pathlib import Path
from google.cloud import bigquery
from google.oauth2 import credentials
import pandas as pd

DATASET = "`bigquery-public-data.stackoverflow`"


def create_client():
    """建立 BigQuery 客戶端"""
    adc_path = Path.home() / '.config' / 'gcloud' / 'legacy_credentials' / 'a0985821880@gmail.com' / 'adc.json'
    
    if adc_path.exists():
        try:
            with open(adc_path, 'r') as f:
                adc_data = json.load(f)
            creds = credentials.Credentials.from_authorized_user_info(adc_data)
            return bigquery.Client(project='onlyme-920902', credentials=creds)
        except Exception as e:
            print(f"讀取憑證失敗: {e}")
    
    return bigquery.Client()


def query_users_with_reputation(client: bigquery.Client, limit: int = 100):
    """查詢用戶資料（含聲望等級分類）"""
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
            WHEN reputation BETWEEN 1 AND 100 THEN '1_Low (1-100)'
            WHEN reputation BETWEEN 101 AND 1000 THEN '2_Medium-Low (101-1000)'
            WHEN reputation BETWEEN 1001 AND 10000 THEN '3_Medium-High (1001-10000)'
            WHEN reputation > 10000 THEN '4_High (10001+)'
            ELSE '0_None'
        END AS reputation_level
    FROM {DATASET}.users
    WHERE reputation IS NOT NULL
    LIMIT {limit}
    """
    return client.query(sql).result().to_dataframe()


def query_posts_with_answers(client: bigquery.Client, limit: int = 100):
    """查詢問題與回答關係"""
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
        TIMESTAMP_DIFF(a.creation_date, q.creation_date, HOUR) AS hours_to_accept
    FROM {DATASET}.posts_questions q
    INNER JOIN {DATASET}.posts_answers a
        ON q.accepted_answer_id = a.id
    WHERE q.accepted_answer_id IS NOT NULL
    LIMIT {limit}
    """
    return client.query(sql).result().to_dataframe()


def query_tag_cooccurrence(client: bigquery.Client, limit: int = 100):
    """查詢標籤共現關係"""
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
    )
    WHERE tag1 < tag2 AND tag1 != '' AND tag2 != ''
    GROUP BY tag1, tag2
    ORDER BY co_occurrence_count DESC
    LIMIT {limit}
    """
    return client.query(sql).result().to_dataframe()


def query_user_connectivity(client: bigquery.Client, limit: int = 100):
    """查詢用戶連通性（識別知識孤島）"""
    sql = f"""
    SELECT
        u.id AS user_id,
        u.display_name,
        u.reputation,
        COUNT(DISTINCT p.id) AS post_count,
        COUNT(DISTINCT c.id) AS comment_count,
        (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id)) AS total_interactions,
        CASE
            WHEN (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id)) = 0 THEN '1_Isolated (0)'
            WHEN (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id)) BETWEEN 1 AND 5 THEN '2_Low (1-5)'
            WHEN (COUNT(DISTINCT p.id) + COUNT(DISTINCT c.id)) BETWEEN 6 AND 20 THEN '3_Medium (6-20)'
            ELSE '4_Active (21+)'
        END AS connectivity_level
    FROM {DATASET}.users u
    LEFT JOIN {DATASET}.posts_questions p ON u.id = p.owner_user_id
    LEFT JOIN {DATASET}.comments c ON u.id = c.user_id
    GROUP BY u.id, u.display_name, u.reputation
    ORDER BY total_interactions ASC
    LIMIT {limit}
    """
    return client.query(sql).result().to_dataframe()


def query_posts_with_code(client: bigquery.Client, limit: int = 100):
    """查詢包含程式碼區塊的貼文"""
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
            WHEN score <= -5 THEN '1_Very Negative (<=-5)'
            WHEN score BETWEEN -4 AND -1 THEN '2_Negative (-4 to -1)'
            WHEN score = 0 THEN '3_Neutral (0)'
            WHEN score BETWEEN 1 AND 5 THEN '4_Positive (1-5)'
            WHEN score BETWEEN 6 AND 20 THEN '5_Very Positive (6-20)'
            ELSE '6_Extremely Positive (>20)'
        END AS score_level
    FROM {DATASET}.posts_questions
    WHERE body IS NOT NULL
    LIMIT {limit}
    """
    return client.query(sql).result().to_dataframe()


def query_account_age_analysis(client: bigquery.Client, limit: int = 100):
    """查詢帳號年資與發文類型"""
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
            THEN '2_Questions_Only'
            WHEN COUNT(DISTINCT CASE WHEN p.post_type_id = 1 THEN p.id END) = 0
                AND COUNT(DISTINCT CASE WHEN p.post_type_id = 2 THEN p.id END) > 0
            THEN '3_Answers_Only'
            ELSE '4_Neither'
        END AS post_type,
        CASE
            WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) < 30 THEN '1_New (<30d)'
            WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) BETWEEN 30 AND 180 THEN '2_Young (30d-6m)'
            WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) BETWEEN 181 AND 730 THEN '3_Mature (6m-2y)'
            WHEN DATE_DIFF(CURRENT_DATE(), DATE(u.creation_date), DAY) BETWEEN 731 AND 1825 THEN '4_Established (2-5y)'
            ELSE '5_Senior (5y+)'
        END AS account_age_level
    FROM {DATASET}.users u
    LEFT JOIN (
        SELECT id, owner_user_id, post_type_id FROM {DATASET}.posts_questions
        UNION ALL
        SELECT id, owner_user_id, post_type_id FROM {DATASET}.posts_answers
    ) p ON u.id = p.owner_user_id
    GROUP BY u.id, u.display_name, u.reputation, u.creation_date
    ORDER BY account_age_days DESC
    LIMIT {limit}
    """
    return client.query(sql).result().to_dataframe()


def query_tags_popularity(client: bigquery.Client, limit: int = 100):
    """查詢標籤熱度"""
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
    return client.query(sql).result().to_dataframe()


def main():
    """主函數 - 測試所有查詢"""
    print("測試 BigQuery Stack Overflow 查詢...")
    print("=" * 50)
    
    try:
        client = create_client()
        print(f"✓ BigQuery 客戶端建立成功")
        print(f"  專案: {client.project}")
        
        # 測試用戶查詢
        print("\n1. 測試用戶查詢...")
        users_df = query_users_with_reputation(client, limit=100)
        print(f"   ✓ 取得 {len(users_df)} 筆記錄")
        print(users_df.head(3).to_string(index=False))
        
        # 測試問題-回答查詢
        print("\n2. 測試問題-回答查詢...")
        posts_df = query_posts_with_answers(client, limit=100)
        print(f"   ✓ 取得 {len(posts_df)} 筆記錄")
        print(posts_df.head(3).to_string(index=False))
        
        # 測試標籤熱度
        print("\n3. 測試標籤熱度查詢...")
        tags_df = query_tags_popularity(client, limit=100)
        print(f"   ✓ 取得 {len(tags_df)} 筆記錄")
        print(tags_df.head(5).to_string(index=False))
        
        # 測試用戶連通性
        print("\n4. 測試用戶連通性查詢...")
        connectivity_df = query_user_connectivity(client, limit=100)
        print(f"   ✓ 取得 {len(connectivity_df)} 筆記錄")
        print(connectivity_df.head(3).to_string(index=False))
        
        # 測試程式碼區塊
        print("\n5. 測試程式碼區塊查詢...")
        code_df = query_posts_with_code(client, limit=100)
        print(f"   ✓ 取得 {len(code_df)} 筆記錄")
        print(code_df.head(3).to_string(index=False))
        
        # 測試帳號年資
        print("\n6. 測試帳號年資查詢...")
        age_df = query_account_age_analysis(client, limit=100)
        print(f"   ✓ 取得 {len(age_df)} 筆記錄")
        print(age_df.head(3).to_string(index=False))
        
        print("\n" + "=" * 50)
        print("所有查詢測試成功！")
        print("\n資料已成功從 BigQuery 取得，可以用於社會網路分析！")
        
    except Exception as e:
        print(f"\n✗ 發生錯誤: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
