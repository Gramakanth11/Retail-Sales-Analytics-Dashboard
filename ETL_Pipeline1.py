import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ============== CONFIG ==============
CSV_FILE = "train.csv"

MYSQL_USER = "root"
RAW_PASSWORD = "Chinna@11"   # keep your real password
MYSQL_PASSWORD = quote_plus(RAW_PASSWORD)  # fixes @ or special chars
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DB = "retail_sales"
TABLE_NAME = "sales_cleaned"

# ====================================

def extract_data():
    print("📥 Extracting data...")
    df = pd.read_csv(CSV_FILE)
    print("Columns:", list(df.columns))
    return df

def transform_data(df):
    print("🔧 Transforming data...")

    # 1. Remove duplicates
    df = df.drop_duplicates()

    # 2. Convert dates
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

    # 3. Create new time features
    df["Order_Year"] = df["Order Date"].dt.year
    df["Order_Month"] = df["Order Date"].dt.month
    df["Order_Month_Name"] = df["Order Date"].dt.strftime("%B")
    df["Order_Week"] = df["Order Date"].dt.isocalendar().week
    df["Order_Day"] = df["Order Date"].dt.day
    df["Order_Weekday"] = df["Order Date"].dt.day_name()

    # 4. Create sales KPIs (since no quantity column)
    df["Avg_Daily_Sales"] = df["Sales"] / df.groupby("Order Date")["Sales"].transform("count")

    # 5. Rename columns for SQL friendliness
    df = df.rename(columns=lambda x: x.strip().replace(" ", "_"))

    print("🔧 Transformation complete.")
    return df

def load_data(df):
    print("📦 Loading to MySQL...")

    conn_str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    safe_print = conn_str.replace(MYSQL_PASSWORD, "****")
    print("Using:", safe_print)

    engine = create_engine(conn_str)
    df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)

    print("✅ Load complete!")

def main():
    df = extract_data()
    cleaned = transform_data(df)
    cleaned.to_csv("cleaned_train.csv", index=False)
    load_data(cleaned)

if __name__ == "__main__":
    main()
