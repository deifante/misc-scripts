#!/usr/bin/env python3
import argparse
import sys
import subprocess

from typing import List, Tuple, Dict, Optional, Union

parser = argparse.ArgumentParser(description="Update git branch from Origin. Abandon all local changes.")
# Add positional argument
parser.add_argument("destination_git_branch", help="The git branch to switch to")
args = parser.parse_args()

class SparkCommand:
    def __init__(self,match_string: str, command_string: str, requires_spark_up: bool):
        self.match_string: str = match_string
        self.command_string: str = command_string
        self.requires_spark_up: bool = requires_spark_up
    def run(self):
        print("Running spark command, ", self.command_string)
        try:
            result = subprocess.run(self.command_string, shell=True, capture_output=True, check=True)
            print(result.stdout.decode('utf-8', errors='replace'))
            print(result.stderr.decode('utf-8', errors='replace'))
        except subprocess.CalledProcessError as e:
            print(f"SparkCommand failed: {e}")
            print("Stderr:", e.stderr)
class SparkCommands(list):
    def __init__(self, *args):
        super().__init__(*args)
    
    def has_command(self, command: str) -> bool:
        for item in self:
            if item.match_string in command:
                return True
        return False
    def get_command(self, command: str) -> SparkCommand:
        for item in self:
            if item.match_string in command:
                return item
        raise KeyError(f"Command not found: {command}")


if __name__ == "__main__":
    destination_git_branch = args.destination_git_branch.strip()
    git_commands  = ["git status",
                 "git fetch -p",
                 "git checkout -- .",
                 f"git checkout {destination_git_branch}",
                 "git pull",
                     ]
    hint_tuples = [
        ("./spark artisan migrate", "./spark artisan migrate --uri=spark.benevity.test", True),
        ("./spark build && ./spark up", "./spark build && ./spark up", False),
        ("./spark composer install", "./spark composer install", True),
        ("./spark database migrate", "./spark database migrate", False),
        ("./spark drush benevity-import-translations 0", "./spark drush benevity-import-translations 0", True),
        ("./spark drush updatedb", "./spark drush updatedb", True),
        ("./spark yarn build:drupal", "./spark yarn build:drupal", False),
        ("./spark yarn build:webpack", "./spark yarn build:webpack", False),
        ("./spark yarn install", "./spark yarn install", False),
    ]
    spark_commands: SparkCommands = SparkCommands()
    commands_to_run: SparkCommands = SparkCommands()
    for hint_tuple in hint_tuples:
        spark_commands.append(SparkCommand(hint_tuple[0], hint_tuple[1], hint_tuple[2]))
    try:
        for git_command in git_commands:
            result = subprocess.run(git_command, shell=True, capture_output=True, check=True)
            print(result.stdout.decode('utf-8', errors='replace'))
            print(result.stderr.decode('utf-8', errors='replace'))
            plain_output = result.stderr.decode('utf-8', errors='replace')
            # check for developer hints
            output_lines = result.stderr.decode('utf-8', errors='replace').splitlines()
            for line in output_lines:
                if "Please run" in line:
                    command = line.split("Please run")[1].strip()
                    print(f"#####Found a developer hint in stderr:{command}######")
                    if spark_commands.has_command(command):
                        print("Matched command: run:", spark_commands.get_command(command).command_string )
                        commands_to_run.append(spark_commands.get_command(command))
            # for spark_command in commands_to_run:
            #     if spark_command.requires_spark_up == False:
            #         spark_command.run()
            
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        print("Stderr:", e.stderr)

print ("done")
