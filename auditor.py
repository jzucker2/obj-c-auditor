#!/usr/bin/env python

# import argparse
import fnmatch
import os
import re

def collect_header_files(project_folder):
	matches = []
	for root, dirnames, filenames in os.walk(project_folder):
		for filename in fnmatch.filter(filenames, '*.h'):
			matches.append(os.path.join(root, filename))
	return matches

def get_string_from_header_file(header_file_path):
	header_file_descriptor = open(header_file_path, 'r')
	file_text = header_file_descriptor.read()
	header_file_descriptor.close()
	return file_text

def get_methods(header_file_as_string):
	method_pattern = re.compile('[-\+](?=\s*\().*?;', flags=re.MULTILINE|re.DOTALL)
	matches = method_pattern.findall(header_file_as_string)
	return matches

def get_properties(header_file_as_string):
	properties_pattern = re.compile('^@property.*?;', flags=re.MULTILINE)
	matches = properties_pattern.findall(header_file_as_string)
	return matches

def main():
	project_folder = "/Users/jordanz/Coding/objective-c/PubNub/PubNub/PubNub"
	print project_folder
	matches = collect_header_files(project_folder)
	print len(matches)
	file_string = get_string_from_header_file('/Users/jordanz/Coding/objective-c/PubNub/PubNub/PubNub/Core/PubNub.h')
	get_properties(file_string)


if __name__ == "__main__":
	main()