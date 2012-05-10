import figure_extractor


solutions = {	'1a': 'BB2_6 C2', 
				'1b':'AA2  BB-2_6',
				'2':'BB-2_6  AA2',
				'3':'E2_#6 F2_6',
				'4':'D2  BB2',
				'5':'D2 BB-2'}

#for x in ['1a', '1b', '2', '3', '4', '5']:
for x in ['1a']:
	this_rule = 'SLRule' + x
	this_file = 'xml_test_files_SL/Lambert ' + x + '.xml'
	this_solution = solutions[x]

	figure_extractor.full_extraction(this_file, this_rule, this_solution)