#!/usr/bin/env python
# picmod.py v0.3  
#    New image files keep same time stamp as originals
#    Listing of image files in HTML file is chronologic
#    and there are date headers included.
# Mon Aug  2 18:25:19 PDT 2010

from picmod_text import copyright_text, intro_text, WebPage, usage, man

import sys, os, getopt, datetime, time
from PIL import Image   
from PIL.ExifTags import TAGS


def handle_fatal_parsing_error(error):
    """ Announces a parsing error, prints <error>, and terminates."""
    print """!!!!! Error parsing options: probably syntax error. !!!!!
Suggest: "picmod -u" for usage or "picmod -m | man" for man page.
Problem may be to do with: %s."""% error
    sys.exit(2)  

def log_message_to(message, logfilepath):
    """Appends message to file called <logfilepath>.
    
    Terminates program if an error is raised."""
    try:
        log=open(logfilepath, 'a')
        log.write(message)
        log.close()
    except:
        print "Error writing to log file:", logfilepath
        sys.exit(2)
        
def new_dir (parent, dir):
    """ Creates a new directory, dir, in the parent file system.
    
    Returns full path name if successful, None if not successful."""
    path = os.path.join(parent,dir)
    cmd = 'mkdir '+path
    try: os.system(cmd)
    except: return None
    if os.path.isdir(path): return path
    else: return None

def dir_is_writeable(dir):
    """ Answers if it is possible to write a file to dir."""
    path=os.path.join(dir, Test_File_Name)
    try: test_fi=open(path, 'w')
    except: return False
    test_fi.close()
    os.system('rm '+path)
    return True
#                        
def interp_rotation(text_input):
    """ Returns one of the following signed integers: 
              0 :  no rotation
            -90 :  rotate clockwise or to the right
             90 :  rotate counter-clockwise or to the left
            360 :  try to rely on EXIF data, else no rotation
        Hence meets the invarient that rotation must be one of the above.
        Inputs (lrLRaA or cl, co): allow for option interpretation.
        Inputs (0168): allow for EXIF data interpretation.
    """
    if text_input:
        if text_input[0] in ('01'): return 0
        elif text_input[0] in ('-lL8'): return 90
        elif text_input[0] in ('+rR6'): return -90
        elif text_input[0] in ('aA'): return 360
        elif len(text_input) > 1:
            if text_input[:2] in ('cl', 'Cl', 'CL'): return -90
            if text_input[:2] in ('co', 'Co', 'CO'): return 90
        else: return 0   # if given invalid string
    else: return 360     # if given empty string

def interp_pre_post_fix(text_input):
    """ Allows user to specify an empty string.
    
    This should never be necessary since the empty string is the default."""
    if text_input in ('""', "''"):
        return ''
    else:
        return text_input
    # the following seems to be 'dead code.' ?should be deleted?
    handle_fatal_parsing_error('designation of pre or post fix')

def is_image_file(filepath):
    """This needs some study as to what exactly I was thinking."""
    if not filepath[-Image_Suffix_Length:] in Image_Suffix_Tuple:
        return False
    l = len(Default_Prefix)
    # I think the above line should use globals.prefix vs Default_Prefix.
    if l == 0:
        return True
    return filepath[:len(Default_Prefix)] != Default_Prefix

def ret_time_stamp():
    """Provides a time stamp for log file entries."""
    return str(datetime.datetime.now())

Timestamp_Truncation_Level=14  # to the level of seconds
def timestamp():      # Trunkated to seconds.
    """ Intended for creation of time stamped file names.
    Not implemented because I found such file names to be cumbersome."""
    t=datetime.datetime.now()
    ret = str.translate(str(t),None,' :.-')[:Timestamp_Truncation_Level]
    return ret
        
# 
def no_dups(fname, t, length=3, place=''):
    """ Returns fname or a modification of it; appends result to the list, t.

    Assumes fname is a name which is to be placed into t, a list.
    This is to be done in such a way that no duplicates can occur in the list.
    If fname does not already exist in t, it is appended.
    If fname already exists in t, it will be modified and then appended.
    Modification consists of inserting a length character long, zero padded
    number (beginning with 1 and incremented as needed) beginning at 
    fname[place]. If place is the empty string it will be converted 
    to the integer len(fname). An attempt will be made to convert any 
    other value given for place into an integer that can be used as a
    slice operand.
    For example: if place = -4, photo.jpg might become photo001.jpg.
    The inserted file name is returned, whether it be the original 
    or a modification.
    This function works even if len(fname) is less than places. It even works
    if fname is an empty string!
    """
    if not place:
        place = len(fname)
    else:
        place = int(place)
    n =0
    name=fname
    s='%0'+str(length)+'d'
    while name in t:
        n=n+1
        insert = s%n
        name=fname[:place]+insert+fname[place:]
    t.append(name)
    return name

TimeStamp = 'ts' # 'ts' is used instead of timestamp()

# Some of the following are used to define the next group of defaults:
Default_Dir_Suffix='_pm.d'
Default_html_Suffix='_pm.html' # web page will display the photos
Path2cssFile='../web.css'  # css file not provided) used by the html page
Test_File_Name='picmod.junk'
Temp_Log_Path='/tmp/picmod.log'
#  Default values used to instantiate globals:
Default_Verbose=True
Default_Interactive=True
Default_Process=False
Default_Max_Dimension=480
Default_Rotation=360
Default_Prefix=''
Default_Postfix=''
Default_Output_Directory=TimeStamp+Default_Dir_Suffix
Default_Create_html_File=False
Default_html_File=TimeStamp+Default_html_Suffix
Default_Log_File_Name=''

Image_Suffix_Tuple = ('.jpg', '.JPG', 'tiff', 'TIFF', '.png', '.PNG')
Image_Suffix_Length = 4

# 
class Specs(object):
    
    """contains the globals to specify how the photos are to be processed"""

    def __init__(self,      verbose=Default_Verbose, \
            interactive=Default_Interactive, process=Default_Process, \
            max_dimension=Default_Max_Dimension, \
            rotation=Default_Rotation, \
            prefix=Default_Prefix, postfix=Default_Postfix,  \
            odir=Default_Output_Directory, \
            create_html_file=Default_Create_html_File, \
            html_file= Default_html_File, \
            logfile=Default_Log_File_Name, \
            file_args=[]        ):

        self.verbose = verbose
        self.interactive=interactive
        self.process=process
        self.max_dimension=max_dimension
        self.rotation=rotation
        self.prefix=prefix
        self.postfix=postfix
        self.odir=odir
        self.create_html_file=create_html_file
        self.html_file=Default_html_File
        self.logfile=logfile
        self.file_args=file_args
        self.temp_logfile=Temp_Log_Path  # no user influence
        self.image_files=[]  # a collector, no user influence
        self.out_files=[]   # used to check for duplicate names


    
    def __str__(self):
        return 'v============== Global Specifications ============v\n\
verbose=%(verbose)s, interactive=%(interactive)s, \
process=%(process)s, maximum_dimension=%(max_dim)d,\n\
rotation=%(rotation)d (90=left,-90=right, 360=auto), \
prefix = %(prefix)s, postfix = %(postfix)s,\n\
output directory = %(odir)s,\n\
create an HTML file = %(create_html)s,\n\
html file = %(html_file)s,\n\
logfile = %(logfile)s,\n\n\
file_args = %(file_args)s,\n\n\
image_files = %(image_files)s\n\
^----------------  end of report -----------------^'\
%  {'verbose':str(self.verbose), 'interactive':str(self.interactive),
    'process':str(self.process), 'max_dim':self.max_dimension,
    'rotation':self.rotation,
    'prefix':self.prefix, 'postfix':self.postfix, 
    'odir':self.odir, 
    'create_html':str(self.create_html_file),
    'html_file':self.html_file, 
    'logfile':self.logfile,
    'file_args':str(self.file_args),
    'image_files':str(self.image_files)}

    def v(self, text, nl=1):  
        """ if verbose, prints text, with or without \n """
        if self.verbose:
            print text,
            if nl:
                print

    def handle_arg(self, file):
        """ Handles each argument; recursively when appropriate. 
        
        Arguments that are image files are appended to 
        self.image_files  (a list of the images to be processed)   """

        self.v("Handling %s"%file, 0)
        if os.path.exists(file):  # EXISTS?
            file=os.path.abspath(file)  # EXPANDED
            self.v('which exists.')
        else:                         # BAD ARGUMENT
            message="\nFile %s doesn't exist.\n" % file
            self.v(message,0)
            log_message_to(message, self.temp_logfile)
            return              # END OF BAD ARG/FILE

        if os.path.isdir(file):      # DIRECTORY
            self.v('Handling directory: %s,'%file)
            if not self.odir:  # In case still need an output dir.
                possible_1st_dir=file
                if dir_is_writeable(possible_1st_dir):
                    self.odir=possible_1st_dir
                    self.v('\twhich is writeable.')
                else:               # No good if can't write to it!
                    message='%s is not writeable!\n'%file
                    self.v(message,0)
                    log_message_to(message, self.temp_logfile)
            # self.v('Recurse through directory %s.'%file)
            for fi in os.listdir(file):  # READ FILES IN DIRECTORY
                fi_path=os.path.join(file, fi)
                self.handle_arg(fi_path)
                
        elif os.path.isfile(file):   # a FILE, finally:-)
            if is_image_file(file):  # ck it's an IMAGE (file access)
                self.v('%s --> list.'%file)
                self.image_files.append(file)  # append to list of image files
            else:                    # report not IMAGE
                message='Ignoring non image file: %s\n' % file
                self.v(message,0)
                log_message_to(message, self.temp_logfile)
        # end of def handle_arg(self, file):
# 
    def complete_calculable_values(self):
        """ 
        1. sets up all the image files into self.image_files,
                                a single list of full path names.
        1.a/ it is here that one could order the image files.
        2. sets up Temp_Log_Path and reports managed problems to it.
        3. sets up the output directory.
        4. (Yet to be implemented: )determines final location for logfile and 
                moves current content of the temporary log file into it.   
        """
        # initialize self.temp_logfile for use by self.handle_arg()
        log_message_to('\n#####'+ret_time_stamp()+': new run of picmod.py.#####\n', \
                                                        self.temp_logfile)
        
        Timestamp_odir = ret_time_stamp()+Default_Dir_Suffix

        if self.odir:  # Is user assigned out put directory valid??
            if (os.path.isdir(self.odir) and dir_is_writeable(self.odir)):
                self.odir=os.path.abspath(self.odir) 
            else:                        # Can't use it as is.
                cwd=os.getcwd()
                possible_odir = new_dir(cwd, self.odir)
                if possible_odir and dir_is_writeable(possible_odir):
                    self.odir = possible_odir
                else:
                    message='Ignoring non valid output directory: %s.\n'\
                                    % self.odir
                    self.v(message,0)
                    log_message_to(message, self.temp_logfile)
                    self.odir=''     # Waste it! We'll look for another.
        if not self.odir:      # try TIME STAMP in CURRENT WORKING DIRECTORY
            cwd=os.getcwd()  # 1st attempt to establish an output directory.
            possible_odir = new_dir(cwd, timestamp_odir)  
            if possible_odir and dir_is_writeable(possible_odir):     
                self.odir=possible_odir

        self.v('Begin traversal of arguments.')
        for file in self.file_args:
            fi=os.path.abspath(file)
            self.handle_arg(fi)  # Will continue attempts to find 
            #                      an output directory (as needed.)
        
        if not self.odir:
            message='FATAL ERROR: unable to establish an output directory!'
            self.v(message, 0)
            log_message_to(message, self.temp_logfile)
            sys.exit(2)
        else:
            message='Out put directory: '+ self.odir +'\n'
            self.v(message,0)
            log_message_to(message, self.temp_logfile)
# 
    def manipulate(self):
        """ Traverse the list of image files and do the work. """

        def scale(two_ints, max_dimension):
            """ scale: a function which takes a tuple of two integers and 
            a single integer (max_dimension,) and returns a tuple of two 
            integers that have the same ratio to one another as did the 
            original tuple, but scaled so that the largest is no greater 
            than max_dimension. (was tested in scale.py which is not in 
            the repository) """
            a, b = two_ints
            longest = a
            if b > a: longest = b
            ratio = (float(max_dimension)/float(longest))
            return (int(a*ratio), int(b*ratio))
        
        def get_orientation(image):
            """ Possible return values:
            None : EXIF data not available.
            1 :  standandard (landscape)
            6 :  portrait, photographer's left hand uppermost, rotate -90*.
            8 :  portrait, right hand uppermost, needs rotation to left (90*)
            """
            exif_info={}
            try:
                info=image._getexif()
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    exif_info[decoded] = value
                return exif_info["Orientation"]
            except: return

        def rotation2text(n):
            if n == 0: return 'none'
            elif n == 90: return 'to left'
            elif n == -90: return 'to right'
            elif n == 360: return 'default or auto'

        """ !!! The BEGINNING of the BODY of def manipulate(self):  !!!"""

        message= \
"""Beginning traversal of image files. If they are to be processed, 
their destination directory will appear below.\n"""
        if self.process:
            message=message+"%s.\n"%self.odir
        self.v(message,0)
        log_message_to(message, self.temp_logfile)
        html_img_data = [] # used to collect data for the html file
        for p in self.image_files:  # TRAVERSE
            save = self.process
            message= \
'\n-----------------------------\nWILL TRY TO OPEN %s\n'  %   p
            self.v(message,0)
            log_message_to(message, self.temp_logfile)
            try: i=Image.open(p)
            except:
                message='\tUnable to open as an image file.\n'
                self.v(message,0)
                log_message_to(message, self.temp_logfile)

                # END OF PROCESSING OF THIS FILE
            else:          # SUCCESSFULLY OPENED AN IMAGE (4 tabs)
                message='\tSuccessfully opened as an image file.\n'
                self.v(message,0)
                log_message_to(message, self.temp_logfile)
                new_size=scale(i.size, self.max_dimension)
                if self.rotation==360:
                    orientation = get_orientation(i)
                    if orientation:
                        message=  \
                            '\tExif data reveals orientation to be %d.\n'\
                                            % orientation
                        self.v(message,0)
                        log_message_to(message, self.temp_logfile)
                        current_rotation=interp_rotation(str(orientation))
                    else:
                        message='\tUnable to gather EXIF data.\n'
                        self.v(message,0)
                        log_message_to(message, self.temp_logfile)
                        current_rotation = 0
                else:
                    current_rotation = self.rotation
                if not current_rotation in (0, 90, -90):  # invarient
                    print \
                    'DEBUG MESSAGE: current_rotation is %d.'%current_rotation
                    handle_fatal_parsing_error   \
                     ('Invarient breach! \n\
                     This is probably NOT a parsing error.\n\
                     It is more likely a bug in the program.\n\
                     Probably in the "interp_rotation" function.\n\
                     Please report this to alex@kleider.ca.\n')
                interactive_text  =  \
"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\
The image is being displayed in a separate window.\n\
!!!You must close that window before proceeding!!!\n\
Data: Orientation = %d and size (width, height) = %s.\n\
Proposed changes are Rotation : %s; and resizing to %s.\n\
To accept simply hit <--' (the Enter or Return key).\n\
To change the rotation, your choices are one of the characters given below:\n\
    0, n(one : no rotation\n\
    l(eft : counter clockwise rotation\n\
    r(ight : clockwise rotation\n\
    a(bort : this choice will abort processing of this image\n\
and then the Enter or Return key.\n"%\
(current_rotation, str(i.size), rotation2text(current_rotation), \
new_size)
                verbose_text  = "n\
Data: Orientation = %d and size (width, height) = %s.\n\
Proposed changes are Rotation : %s; and resizing to %s.\n"%\
(current_rotation, str(i.size), rotation2text(current_rotation), \
new_size)
                if self.interactive:
                    i.show()
                    response = raw_input(interactive_text)
                    if response:
                        if response[0] in '0n': current_rotation=0
                        elif response[0] in 'Ll': current_rotation=90
                        elif response[0] in 'Rr': current_rotation=-90
                        elif response[0] in 'Aa': save = False
                        else:
                            message=  \
'\tUninterpretable response ("%s"); will use defaults.\n'%response
                            print message,
                            log_message_to(message, self.temp_logfile)
                else:
                    self.v(verbose_text)
                    log_message_to(verbose_text, self.temp_logfile)

                if save:  # FINALLY GET TO PROCESS AN IMAGE FILE- p / i

                    file=self.prefix+os.path.basename(p)+self.postfix
                    out_file=no_dups(file, self.out_files, place=-4)
                    out_path=os.path.join(self.odir, out_file)
                    message=  \
                        'Rotation: %d; Size: %s; to be SAVED AS\n%s.\n' \
                        % (current_rotation, str(new_size), out_path)
                    log_message_to(message, self.temp_logfile)
                    self.v(message,0)
                    i=i.resize(new_size, Image.ANTIALIAS)
                    if current_rotation!=0:
                        i = i.rotate(current_rotation)
                        new_size = i.size
                    i.save(out_path); 
                    # Also want to preserve mtime of original photo
                    # Collect mtime and establish time related vars:
                    epoch_mtime = os.path.getmtime(p)
                    struct_mtime = time.localtime(epoch_mtime)
                    date_time_dic = {'y':struct_mtime.tm_year,
                                'm':struct_mtime.tm_mon,
                                'md':struct_mtime.tm_mday,
                                'hour':struct_mtime.tm_hour,
                                'min':struct_mtime.tm_min }
                    date_taken =  "%(y)04d/%(m)02d/%(md)02d"\
                                                      %  date_time_dic
                    date_time_taken4human =  \
                            "%(y)04d/%(m)02d/%(md)02d %(hour)02d:%(min)02d"\
                                                      %  date_time_dic
                    date_time_taken4touch =  \
                            "%(y)04d%(m)02d%(md)02d%(hour)02d%(min)02d"\
                                                      %  date_time_dic

                    cmd = 'touch -t %s %s'  % (date_time_taken4touch, out_path)
                    os.system(cmd)
                    
                    new_html_img_line = \
        '<img src="%s" width="%d" height="%d" alt="%s"/>\n' % \
                        ("./"+out_file, \
                        new_size[0], \
                        new_size[1], \
                        'image taken '+ date_time_taken4human)

                    if self.verbose:
                      print \
                      '#: adding new_html_img_line presented on next line:'
                      print new_html_img_line
                    html_img_data.append(    \
                        (date_time_taken4touch, new_html_img_line, date_taken) )
                else:
                    message= \
                    '\tChanges- Rotation:%d; Size: %s, not made or saved.\n'\
                    % (current_rotation, str(new_size))
                    self.v(message,0)
                    log_message_to(message,self.temp_logfile)
        #
        html_img_data.sort()   # Sorts by time taken.
        date_header=''
        html_txt=''
        for date_time, line, date in html_img_data:
            if not date_header or date_header !=  date:
                date_header = date
                date_header_line = \
                "<h3> Photos taken %s: </h3>\n" % date
                html_txt = html_txt + date_header_line
            html_txt = html_txt + line
        html = WebPage%(Path2cssFile, TimeStamp, self.odir, html_txt)
        htmlFile=os.path.join(self.odir, Default_html_File)
        html_file=open(htmlFile, "w")
        html_file.write(html)
        html_file.close()
        message='-----------------------------------\n\
Look for HTML file here: %s \n'%htmlFile
        self.v(message,0)
        log_message_to(message, self.temp_logfile)


def set_options():
    globals = Specs()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "?uhvqicm:r:p:P:d:l:",  \
        ['conditions', 'usage', 'help', 'man', 'verbose', 'quiet', 
        'interactive', 'change',
        'max=', 'rotation=', 'prefix=', 'Prefix=', 'directory=', 
        'htmlCreate', 'htmlFileName=', 'logfile='])
    except getopt.GetoptError,err:
        # print help info and exit
        print str(err)  # will print something like 'option -a not recognized.'
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == '--conditions':
            print copyright_text
            sys.exit()
        if o in ('-?', '-u', '-h'):
            usage()
            sys.exit()
        if o in ('--man', '--mannual'):
            man()
            sys.exit()
        if o in ('-v', '--verbose'):
            globals.verbose=True
        if o in ('-q', '--quiet'):
            globals.verbose=False
            globals.interactive=False
        if o in ('-i', '--interactive'):
            globals.interactive=True
        if o in ('-c', '--change'):
            globals.process=True
        if o in ('-m', '-max'):
            try:
                globals.max_dimension=int(a)
            except:
                handle_fatal_parsing_error('problem parsing max_dim')
        if o in ('-r', '--rotation'):
            globals.rotation=interp_rotation(a)
        if o in ('-p', '--prefix'):
            globals.prefix=interp_pre_post_fix(a)
        if o in ('-P', '--postfix', '--Postfix'): 
            globals.postfix=interp_pre_post_fix(a)
        if o in ('-d', '--directory'):
            globals.odir=a
        if o == '--htmlCreate':
            globals.create_html_file=True
        if o == '--htmlFileName':
            globals.html_file=a
        if o in ('-l', '--log', '--logfile'):
            globals.logfile=a
    globals.file_args=args
    if not (globals.interactive or globals.process):
        message=  \
         "\nNeither interactive nor change were selected. Nothing to do.\n"
        handle_fatal_parsing_error(message)
    return globals

if __name__=='__main__':  
            # suggested by leif@synthesize.us at NoiseBridge 1/27/2010

    globals=set_options()

    if globals.verbose:
        print intro_text
        print 'Globals as discovered from command line options:'
        print globals.__str__()
        j=raw_input('<---! to continue')

    globals.complete_calculable_values()

    if globals.verbose:
        print 'Globals after processing of cmd ln optioins:'
        print globals.__str__()
        print 'Now for processing; here goes!'
        j=raw_input('<---! to continue')

    globals.manipulate()
"""
+-------------------+------------------+------------------------+
|   Gather photo data and set up to do what 'should' be done.   |
|      Booleans: verbose, interactive, process                  |
|      Values: new_size from max_dimension & original_size      |
|              prefix &/or postfix                              |
+-------------------+------------------+------------------------+
|   No Processing   |          PROCESSING                       |
+-------------------+------------------+------------------------+
|              Interactive             |    Non-Interactive     |
+-------------------+------------------+------------------------+
| Display data and recommended changes.|                        |
|        Allow corrective input.       |                        |
+-------------------+------------------+------------------------+
|   Ignore changes  |         Process and save new image.       |
+-------------------+------------------+------------------------+
"""

