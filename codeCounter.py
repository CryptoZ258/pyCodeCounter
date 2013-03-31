# !/usr/bin/python
# -*- coding:utf-8 -*-

import os
import re

class code_counter_app(object):
	#folder_name ='/'	# the dir that want to walk
	log_file =''		# wirte output to the log file
	folder_tree = []	# the root tree
	folder_info = {		# the root folder info, also the templete of subtree
		'name': '',
		'counter': 0
	}
	my_pattern = re.compile(r'[a-zA-Z1-9]+.(py|c|java|php|cpp|css|html|xml|htm|js|cs|h|asm|sh|ruby|perl)$')

	def __init__(self, folder_name, log_file_name):
		#self.folder_name = folder_name
		self.folder_info['name'] = folder_name
		# open the log file to write
		self.log_file = open(log_file_name, 'w')
		#print self.folder_info['name']
		
    # initial the folder and tree    
	def init_app(self):
		self.folder_tree = []
		self.folder_tree.append(self.folder_info)
		self.folder_tree.append([])
		#print self.folder_tree
		
	# count the line number of a file
	def count_code_of_file(self,file_name):
		return len(open(file_name).readlines())
		
		
	# 核心遍历函数
	def walk_dir(self,folder_tree, topdown=True):
		for root, dirs, files in os.walk(folder_tree[0]['name'], topdown):
			for name in files:
				if name[0] == '.':
					continue
				
				if self.my_pattern.match(name):
				
					path_name = os.path.join(root,name)
					if os.path.islink(path_name):
						continue
					# calculate the summry of the file
					count_result = self.count_code_of_file(path_name)
					# insert into the tree
					# print path_name , " 6"
					#fileinfo.write(os.path.join(root,name) + '\n')
					sub_folder_tree = [{'name':path_name,'counter': count_result},[]]
					folder_tree[1].append(sub_folder_tree)
					# sum
					folder_tree[0]['counter'] = folder_tree[0]['counter'] + count_result
				
			for name in dirs:
				if name[0] == '.':
					continue
				path_name = os.path.join(root,name)
				# print(path_name)
				#fileinfo.write('  ' + os.path.join(root,name) + '\n')
				sub_folder_tree = [{'name':path_name,'counter': 0},[]]
				folder_tree[1].append(sub_folder_tree)
				self.walk_dir(sub_folder_tree, topdown)
				# sum
				folder_tree[0]['counter'] = folder_tree[0]['counter'] + sub_folder_tree[0]['counter']
			return

	def print_tree(self,folder_tree, tabs = 0,topdown=True):
		if os.path.isdir(folder_tree[0]['name']):
			print ' '
			print '   '*tabs,'+',folder_tree[0]['name'] , ' : ' ,folder_tree[0]['counter']
			
		else:
			file_name = os.path.split(folder_tree[0]['name'])
			print '   '*tabs,'+',file_name[1], ' : ' ,folder_tree[0]['counter']
			return
		if folder_tree[1]:
			
			for sub_tree in folder_tree[1]:
				self.print_tree(sub_tree,tabs +1)
		else:
			return
	
	# print the output to the file
	def print_tree_to_file(self, folder_tree, tabs = 0, topdown= True):
		if os.path.isdir(folder_tree[0]['name']):
			print >>self.log_file,' '
			print >>self.log_file,'   '*tabs,'+',folder_tree[0]['name'] , ' : ' ,folder_tree[0]['counter']
			
		else:
			file_name = os.path.split(folder_tree[0]['name'])
			print >>self.log_file,'   '*tabs,'+',file_name[1], ' : ' ,folder_tree[0]['counter']
			return
		if folder_tree[1]:
			
			for sub_tree in folder_tree[1]:
				self.print_tree_to_file(sub_tree,tabs +1)
		else:
			return

# '/home/bibodeng/programming/python/djcode'
input_path = raw_input("please input the PATH of your source code: ")
log_file_name = raw_input("please input the filename of the output: ")
input_path = str(input_path)
print "PATH and logfile are: ",input_path, log_file_name
a=code_counter_app(input_path,log_file_name)
a.init_app()
a.walk_dir(a.folder_tree)
a.print_tree(a.folder_tree)
a.print_tree_to_file(a.folder_tree)

