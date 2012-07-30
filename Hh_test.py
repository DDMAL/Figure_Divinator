import sys
import figure_extractor


def Hh_test(url='bwv'):
    if url == 'bwv':
        this_file = 'bwv307.xml'
    else:
        this_file = url
        #this_file = 'xml_test_files_SL/Hotteterre-Op2-No3-1-Allemande.xml'

    #Get the extraction
    score = figure_extractor.full_extraction(this_file, display=True)

    return score

# Run from command line
if __name__ == '__main__':
    if len(sys.argv) > 1:
        Hh_test(sys.argv[1])
    else:
        Hh_test()
