# Import the argparse module
# argparse is used to create command-line applications
import argparse

# Step 1: Create an ArgumentParser object
# The description appears when users run --help
parser = argparse.ArgumentParser(
    description="Backup files"
)

# Step 2: Create a command-line argument called --source
# Users must provide the folder they want to back up
parser.add_argument(
    "--source",
    required=True,
    help="Folder to back up"
)

# Step 3: Create a command-line argument called --destination
# Users must provide where the backup should be saved
parser.add_argument(
    "--destination",
    required=True,
    help="Backup location"
)

# Step 4: Read and process the user's command-line arguments
args = parser.parse_args()

# Step 5: Access the values entered by the user
# args.source stores the value passed to --source
# args.destination stores the value passed to --destination

print(f"Backing up {args.source}")
print(f"Saving backup to {args.destination}")