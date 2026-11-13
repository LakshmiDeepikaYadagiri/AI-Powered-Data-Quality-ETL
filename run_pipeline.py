
import subprocess
import sys
import logging
from pathlib import Path
from datetime import datetime

project_folder = Path(__file__).parent

# Create logs folder
logs_folder = project_folder / "logs"
logs_folder.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=logs_folder / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

pipeline_steps = [
    "main.py",
    "load_to_database.py",
    "analyze_orders.py",
    "anomaly_detection.py"
]

start_time = datetime.now()

print("\nAUTOMATED ETL PIPELINE")
print("=" * 40)

logging.info("Pipeline started")

for step in pipeline_steps:
    print(f"\nRunning: {step}")
    logging.info("Starting %s", step)

    try:
        subprocess.run(
            [sys.executable, str(project_folder / step)],
            cwd=project_folder,
            check=True
        )

        print(f"SUCCESS: {step}")
        logging.info("SUCCESS: %s", step)

    except subprocess.CalledProcessError:
        print(f"FAILED: {step}")
        logging.exception("FAILED: %s", step)
        logging.error("Pipeline stopped")
        sys.exit(1)

    except OSError:
        print(f"Could not start: {step}")
        logging.exception("Could not start: %s", step)
        sys.exit(1)

end_time = datetime.now()
duration = end_time - start_time

print("\n" + "=" * 40)
print("PIPELINE COMPLETED SUCCESSFULLY")
print("Duration:", duration)

logging.info("Pipeline completed successfully")
logging.info("Duration: %s", duration)
