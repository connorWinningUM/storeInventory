import subprocess

# Stop and remove containers defined in docker-compose.yml
subprocess.run(["docker", "compose", "down"], check=True)

print("Database container stopped and removed.")