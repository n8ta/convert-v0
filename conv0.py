import argparse
import os
import sys
import queue
from conv0lib import *

parser = argparse.ArgumentParser(description='ConvertV0 -- flac to mp3')
parser.add_argument('path', type=str)
parser.add_argument("--delete-flac", help="Remove flac files after converting", action="store_true")
parser.add_argument("--verbose", help="Verbose output for debugging", action="store_true")

args = parser.parse_args()

if not os.path.exists(args.path):
    sys.exit("That path doesn't appear to exists. Try providing a full path, for example: '/Users/you/Music/'")

q = queue.SimpleQueue()

for file_or_folder in os.listdir(args.path):
    q.put(os.path.join(args.path, file_or_folder))


def print_verbose(text):
    if args.verbose:
        print(text)


def handle(path):
    # file/folder path --> Result enum
    print_verbose("Considering {}".format(path))
    if os.path.isfile(path) and path.endswith(".flac"):
        print_verbose("  Path is .flac, converting...")
        try:
            convert_to_v0(path)
        except ConversionFailure:
            return Result.ConversionFailed
        print_verbose("  Conversion completed")
        return Result.ConversionSuccessful
    elif os.path.isdir(path):
        print_verbose("  Path is a directory putting contents into queue")
        for item in os.listdir(path):
            q.put(os.path.join(path, item))
        return Result.Directory
    else:
        return Result.NotFlac
        print_verbose("  Not .flac or a directory, skipping")


converted_count = 0  # successful conversions
failed = []  # list of failed files
flac_size = 0  # total file size of flac files
v0_size = 0  # total file size of new mp3 v3 files.

while not q.empty():
    path = q.get()
    result = handle(path)
    if result is Result.ConversionSuccessful:
        converted_count += 1
        flac_size += os.stat(path).st_size  # flac file size
        v0_size += os.stat(output_path(path)).st_size  # v0 file size
    elif result is Result.ConversionFailed:
        failed.append(path)

print_verbose("Queue empty")
print("Completed, converted {} files".format(converted_count))
print("{} of flac converted to {} of mp3v0".format(sizeof_fmt(flac_size), sizeof_fmt(v0_size)))
print(" ")
print("Saved {}".format(sizeof_fmt(flac_size - v0_size)))
if failed:
    print("{} failure(s):".format(len(failed)))
    for failure in failed:
        print(failure)
