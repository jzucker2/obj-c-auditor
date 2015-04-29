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

def properties_and_methods_for_header_file(header_file_path):
	header_file_string = get_string_from_header_file(header_file_path)
	header_file_dict = {}
	methods = get_methods(header_file_string)
	properties = get_properties(header_file_string)
	if (0 < len(properties)):
		header_file_dict['properties'] = properties
	if (0 < len(methods)):
		header_file_dict['methods'] = methods
	return header_file_dict

def main():
	project_folder = "/Users/jordanz/Coding/objective-c/PubNub/PubNub/PubNub"
	print project_folder
	all_header_files = collect_header_files(project_folder)
	print 'total header files found: ' + str(len(all_header_files))
	# file_string = get_string_from_header_file('/Users/jordanz/Coding/objective-c/PubNub/PubNub/PubNub/Core/PubNub.h')
	# get_properties(file_string)
	audit_dict = {}
	for header_file_path in all_header_files:
		header_file_overview = properties_and_methods_for_header_file(header_file_path)
		if (0 < len(header_file_overview.keys())):
			header_file_name = os.path.basename(header_file_path)
			header_file_overview['path'] = header_file_path
			print header_file_name
			audit_dict[header_file_name] = header_file_overview
	for thingy in audit_dict:
		print '------------------'
		print thingy
		print audit_dict[thingy]
		print '------------------'




if __name__ == "__main__":
	main()