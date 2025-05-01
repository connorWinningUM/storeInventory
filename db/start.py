import subprocess
import time
import psycopg2
import os

# Write docker-compose.yml if needed
with open("docker-compose.yml", "w") as f:
    f.write("""

services:
  db:
    image: postgres:16
    container_name: store_inventory_db
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: store
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - pgdata:/var/lib/postgresql/data4 

volumes:
  pgdata:
            
""")

# Start the service
subprocess.run(["docker", "compose", "up", "-d"], check=True)

#function that will poll the db until its up
def wait_for_postgres(
    dbname="store",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432",
    timeout=30
):
    start = time.time()
    while True:
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            conn.close()
            print("Database is UP!")
            break
        except psycopg2.OperationalError as e:
            if time.time() - start > timeout:
                print("Timed out while waiting for database to start.")
                raise e
            print("* ", end="")
            time.sleep(0.1)

wait_for_postgres()

conn = psycopg2.connect(
    dbname="store",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Read and execute the setup.sql file
setup_path = os.path.join(os.path.dirname(__file__), "setup.sql")
with open(setup_path, "r") as f:
    cursor.execute(f.read())

conn.commit()
cursor.close()
conn.close()

print("Database schema initialized from setup.sql.")
