import os
import argparse


trim_usage = '''
=========================== trim example commands ===========================

BioSAK trim -1 Cliona_R1.fastq.gz -2 Cliona_R2.fastq.gz -a TruSeq3-PE-2.fa

=============================================================================
'''

def sep_path_basename_ext(file_in):

    f_path, f_name = os.path.split(file_in)
    if f_path == '':
        f_path = '.'
    f_base, f_ext = os.path.splitext(f_name)

    return f_name, f_path, f_base, f_ext[1:]


def trim(args):

    fastq_r1        = args['1']
    fastq_r2        = args['2']
    adapter_file    = args['a']
    leading         = args['leading']
    trailing        = args['trailing']
    crop            = args['crop']
    headcrop        = args['headcrop']
    swl             = args['swl']
    swq             = args['swq']
    minlen          = args['minlen']

    _, _, r1_base, r1_ext = sep_path_basename_ext(fastq_r1)
    _, _, r2_base, r2_ext = sep_path_basename_ext(fastq_r2)

    r1_p  = '%s_P.%s'   % (r1_base, r1_ext)
    r1_up = '%s_UP.%s'  % (r1_base, r1_ext)
    r2_p  = '%s_P.%s'   % (r2_base, r2_ext)
    r2_up = '%s_UP.%s'  % (r2_base, r2_ext)

    trimmomatic_cmd = 'trimmomatic PE %s %s %s %s %s %s ILLUMINACLIP:%s:2:30:10 LEADING:%s TRAILING:%s CROP:%s HEADCROP:%s SLIDINGWINDOW:%s:%s MINLEN:%s' % (fastq_r1, fastq_r2, r1_p, r1_up, r2_p, r2_up, adapter_file, leading, trailing, crop, headcrop, swl, swq, minlen)
    print(trimmomatic_cmd)
    os.system(trimmomatic_cmd)


if __name__ == '__main__':
    trim_parser = argparse.ArgumentParser(usage=trim_usage)
    trim_parser.add_argument('-1',              required=True,                          help='fastq R1')
    trim_parser.add_argument('-2',              required=True,                          help='fastq R2')
    trim_parser.add_argument('-a',              required=True,                          help='adapter file, e.g., TruSeq3-PE-2.fa')
    trim_parser.add_argument('-leading',        required=False, type=int, default=25,   help='leading, default is 25')
    trim_parser.add_argument('-trailing',       required=False, type=int, default=25,   help='trailing, default is 25')
    trim_parser.add_argument('-crop',           required=False, type=int, default=140,  help='crop, default is 140')
    trim_parser.add_argument('-headcrop',       required=False, type=int, default=10,   help='headcrop, default is 10')
    trim_parser.add_argument('-swl',            required=False, type=int, default=5,    help='slidingwindow length, default is 5')
    trim_parser.add_argument('-swq',            required=False, type=int, default=30,   help='slidingwindow q-value, default is 30')
    trim_parser.add_argument('-minlen',         required=False, type=int, default=36,   help='minlen, default is 36')
    args = vars(trim_parser.parse_args())
    trim(args)
