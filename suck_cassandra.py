import os
import csv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Thông tin Cassandra
cassandra_host = "116.103.226.38"
cassandra_username = "cassandra"
cassandra_password = "cassandra"

try:
    # Kết nối tới Cassandra
    auth_provider = PlainTextAuthProvider(
        username=cassandra_username, password=cassandra_password
    )
    cassandra_cluster = Cluster([cassandra_host], auth_provider=auth_provider)
    cassandra_session = cassandra_cluster.connect()

    # Tạo thư mục chính để chứa các thư mục tương ứng với các keyspace
    main_output_dir = "db_cassandra"
    os.makedirs(main_output_dir, exist_ok=True)

    # Lấy danh sách tất cả các keyspaces trong cơ sở dữ liệu Cassandra
    keyspaces = cassandra_cluster.metadata.keyspaces.keys()

    for keyspace in keyspaces:
        # Tạo thư mục để lưu các tệp CSV cho keyspace này
        keyspace_output_dir = os.path.join(main_output_dir, keyspace)
        os.makedirs(keyspace_output_dir, exist_ok=True)

        # Lấy danh sách tất cả các bảng trong keyspace
        keyspace_metadata = cassandra_cluster.metadata.keyspaces[keyspace]
        table_names = keyspace_metadata.tables.keys()

        for table_name in table_names:
            # Thực hiện truy vấn SELECT trên mỗi bảng
            select_query = f"SELECT * FROM {keyspace}.{table_name}"
            result = cassandra_session.execute(select_query)
            rows = list(result)

            # Tạo tệp CSV và lưu dữ liệu vào đó
            csv_file_path = os.path.join(keyspace_output_dir, f"{table_name}.csv")
            with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
                csv_writer = csv.writer(csv_file)
                if len(rows) > 0:
                    header = rows[0]._fields
                    csv_writer.writerow(header)  # Ghi tiêu đề cột
                    for row in rows:
                        csv_writer.writerow(row)  # Ghi dữ liệu

            print(f"Lưu bảng {keyspace}.{table_name} vào {csv_file_path}")

except Exception as e:
    print("Lỗi:", e)
finally:
    if cassandra_session:
        cassandra_session.shutdown()
        cassandra_cluster.shutdown()
