#!/usr/bin/env python

import argparse
import fnmatch
import os
import re

def collect_header_files(project_folder):
	matches = []
	for root, dirnames, filenames in os.walk(project_folder):
		for filename in fnmatch.filter(filenames, '*.h'):
			matches.append(os.path.join(root, filename))
	return matches

def get_file_as_string(header_file_path):
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
	header_file_string = get_file_as_string(header_file_path)
	header_file_dict = {}
	methods = get_methods(header_file_string)
	properties = get_properties(header_file_string)
	if (0 < len(properties)):
		header_file_dict['properties'] = properties
	if (0 < len(methods)):
		header_file_dict['methods'] = methods
	return header_file_dict

class HeaderFileParser(object):
	"""docstring for HeaderFileParser"""
	def __init__(self, header_file_path):
		super(HeaderFileParser, self).__init__()
		self.header_file_path = header_file_path
		self.header_file_string = None
		self.properties = None
		self.methods = None
		self.name = os.path.basename(self.header_file_path)
	def __set_header_file_as_string(self):
		self.header_file_string = get_file_as_string(self.header_file_path)
	def __get_methods(self):
		method_pattern = re.compile('(?<!=\s)^[-\+](?=\s*\()[^{}]*?;', flags=re.MULTILINE|re.DOTALL)
		# method_pattern = re.compile('^[-\+](?=\s*\().*?;', flags=re.MULTILINE|re.DOTALL)
		if not self.header_file_string:
			self.__set_header_file_as_string()
		matches = method_pattern.findall(self.header_file_string)
		return matches
	def __get_properties(self):
		properties_pattern = re.compile('^@property.*?;', flags=re.MULTILINE)
		if not self.header_file_string:
			self.__set_header_file_as_string()
		matches = properties_pattern.findall(self.header_file_string)
		return matches
	def process(self):
		self.properties = self.__get_properties()
		self.methods = self.__get_methods()
		self.header_file_string = None
		return ((0 < len(self.methods)) or (0 < len(self.properties)))
	def has_properties(self):
		if self.properties:
			return (0 < len(self.properties))
		return False
	def has_methods(self):
		if self.methods:
			return (0 < len(self.methods))
		return False
		# header_file_dict = {}
		# methods = self.get_methods
		# properties = self.get_properties
		# if (0 < len(properties)):
		# 	header_file_dict['properties'] = properties
		# if (0 < len(methods)):
		# 	header_file_dict['methods'] = methods
		# if (0 < len(header_file_dict)):
		# 	self.info = header_file_dict

class AuditFileWriter(object):
	"""docstring for AuditFileWriter"""
	def __init__(self, audit_list, output):
		super(AuditFileWriter, self).__init__()
		self.audit_list = audit_list
		self.output = output
	def output_to_file(self):
		with open(self.output, 'a+') as output_file:
			for header_file in self.audit_list:
				output_file.write('==================================\n')
				output_file.write(header_file.name)
				output_file.write('\n')
				if header_file.has_properties():
					output_file.write('Properties:\n')
					for property_item in header_file.properties:
						output_file.write("%s\n" % property_item)
				if header_file.has_methods():
					output_file.write('----------------------------------\n')
					output_file.write('Methods:\n')
					for method_item in header_file.methods:
						output_file.write("%s\n" % method_item)
				output_file.write('==================================\n')
				output_file.write('\n')


def main():
	# project_folder = "/Users/jordanz/Coding/objective-c/PubNub/PubNub/PubNub"
	parser = argparse.ArgumentParser(description="Process all methods and properties in an Xcode Project.")
	parser.add_argument('--input', '-i', action='store', required=True, help="Path to directory of project to audit")
	parser.add_argument('--output', '-o', action='store', required=True, help="Path for output file")
	args = parser.parse_args()
	if not os.path.isdir(args.input):
		print args.input + ' is not a valid directory'
		return
	if os.path.exists(args.output):
		print args.output + ' already exists. Must supply a path to create a NEW file'
		return
	all_header_files = collect_header_files(args.input)
	print 'total header files found: ' + str(len(all_header_files))
	audit_list = []
	for header_file_path in all_header_files:
		header_file_overview = HeaderFileParser(header_file_path)
		# only add files that have methods or properties
		if (header_file_overview.process()):
			audit_list.append(header_file_overview)
	print 'header files with public methods and/or properties ' + str(len(audit_list))
	# for thingy in audit_list:
	# 	print "==========="
	# 	print thingy.name
	# 	print thingy.properties
	# 	print thingy.methods
	# 	print "==========="
	audit_file_writer = AuditFileWriter(audit_list, args.output)
	audit_file_writer.output_to_file()




if __name__ == "__main__":
	main()