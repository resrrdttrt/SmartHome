import os
import csv
import psycopg2
from psycopg2 import sql

# Thông tin PostgreSQL
pg_host = "116.103.227.5"
pg_user = "postgres"
pg_password = "newpassword"

try:
    # Kết nối tới PostgreSQL
    pg_connection = psycopg2.connect(host=pg_host, user=pg_user, password=pg_password)

    # Tạo thư mục chính để chứa các thư mục tương ứng với cơ sở dữ liệu
    main_output_dir = "db_postgres"
    os.makedirs(main_output_dir, exist_ok=True)

    # Lấy danh sách các cơ sở dữ liệu
    database_query = sql.SQL(
        "SELECT datname FROM pg_database WHERE datistemplate = false;"
    )
    with pg_connection.cursor() as cursor:
        cursor.execute(database_query)
        database_names = [row[0] for row in cursor.fetchall()]

    for database_name in database_names:
        # Tạo thư mục để lưu các tệp CSV cho cơ sở dữ liệu này
        database_output_dir = os.path.join(main_output_dir, database_name)
        os.makedirs(database_output_dir, exist_ok=True)

        # Kết nối tới cơ sở dữ liệu cụ thể
        database_connection = psycopg2.connect(
            host=pg_host, user=pg_user, password=pg_password, database=database_name
        )

        # Lấy danh sách các bảng trong cơ sở dữ liệu
        table_query = sql.SQL(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        )
        with database_connection.cursor() as cursor:
            cursor.execute(table_query)
            table_names = [row[0] for row in cursor.fetchall()]

        for table_name in table_names:
            # Thực hiện truy vấn SELECT trên mỗi bảng
            select_query = sql.SQL("SELECT * FROM {}").format(
                sql.Identifier(table_name)
            )
            with database_connection.cursor() as cursor:
                cursor.execute(select_query)
                rows = cursor.fetchall()

            # Tạo tệp CSV và lưu dữ liệu vào đó
            csv_file_path = os.path.join(database_output_dir, f"{table_name}.csv")
            with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(
                    [desc[0] for desc in cursor.description]
                )  # Ghi tiêu đề cột
                csv_writer.writerows(rows)  # Ghi dữ liệu

            print(f"Lưu bảng {database_name}.{table_name} vào {csv_file_path}")

except Exception as e:
    print("Lỗi:", e)
finally:
    if pg_connection:
        pg_connection.close()
