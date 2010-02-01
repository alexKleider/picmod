#!/usr/bin/env python
# picmod.py
# Thu Jan 28 21:58:14 PST 2010

copyright_text = \
"""
    "picmod" stands for "picture modifier": 
        it provides for shrinkage and rotation of jpeg image files.

    Copyright (C) 2010  Alexander Kleider 

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  (Look for a file called COPYING.)
    If not, see <http://www.gnu.org/licenses/>.

Contact: Alex Kleider, P.O. Box 277, Bolinas, CA 94924 USA    alex@kleider.ca
"""

intro_text = \
"""
    picmod  Copyright (C) 2010 Alexander Kleider
    This program comes with ABSOLUTELY NO WARRANTY; 
    This is free software, and you are welcome to redistribute it
    under certain conditions;
    for details rerun the program as follows: picmod.py --conditions
"""

import sys, os, getopt, datetime
import toolbox
from PIL import Image   
from PIL.ExifTags import TAGS


print intro_text

def usage():
    print """ picmod usage statement
    picmod.py options arguments:
"?uhvqicm:r:p:P:d:l:", 
['conditions', 'usage', 'help', 'man', 'verbose', 'quiet', 
'interactive', 'change', 'htmlCreate', 'htmlFileName', 
'max=', 'rotation=', 'prefix=', 'Prefix=', 'directory=', 'logfile='] 
file_name_arguments
"""

def man():
    print """ picmod man page
    NAME  picmod.py  -  Photo processing utility.

    SYNOPSIS
        picmod.py [-?uhvqic] [-m max_dimension] [-r rotation] [-p prefix ] \
        [-P postfix] [-d directory] [-l logfile] files.. directories..

    OPTIONS
        -?, -h, -u :  print a usage statement.
        -v : verbose- provides extra output during program execution.
        -q : quiet- sets verbose to true (which is the current default.)
        -i : interactive- provides data, shows images, and accepts user input.
        -c : change- with out this option, noting is processed.
        -m max : processed image will be shrunk to fit into a max pixels
            square without distortion.
        -r rotation : 0, n, a, -, l, co, +, r, cl
            0, n(o rotation
            a(uto is the default: this assumes EXIF data is available.
                defaults to no rotation if data is not available.
            -, l(eft, co(nter clockwise.
            +, r(ight, cl(lockwise
        -p prefix :  designates a prefix for output file, default is 'new_'
        -P postfix : designates a postfix, default is ''
        -d directory :  an out put directory name may be specified.
        -l logfile :  a log file may be specified.
        
        Long options are also available. 
        Those that have corresponding short options will be obvious:  
        --usage, --help, --man, --verbose, --quiet, --interactive, --change,
        --max, --rotation, --prefix, --Prefix, --directory, --logfile
        Other long options:
        --htmlCreate :  if set, an html file will be created with refs to the 
            output files so the images can be examined with a browser and 
            the text of the html used in web design.
        --htmlFileName :  the user may specify a name for this file but is
            advised not to do so since the default name will be time stamped
            and hence guaranteed to remain unique.
        --conditions : this one simply prints copyright information and exits.

    ARGUMENTS
        Arguments can be image files or directories containing image files.

    NOTES:
        The basic functionality of this program is to downsize image files.
    It is also possible to rotate images. (See below.)
    
    Image files are assumed to 1.) be jpeg format and 2.) end in '.jpg' or 
    '.JPG'. Other files are simply ignored after they are reported in the log.
    A none jpeg file with such a sufix will be treated the same way.
    (This may be not quite true: a non-jpeg image file sith a jpg suffix could
    (in theory) exist but how it would be handled has not been investigated.)

        An output directory will be created and any user specified name will
    be respected to the extent possible. The default behavior is to create a 
    directory name by appending '_pm.d' to a time stamp and place this 
    directory under the current working directory. If this proves impossible
    (?permissions?), arguments will be traversed and the first suitable 
    directory will be chosen. If the argument is a directory itself, it will
    be picked as a parent for the output directory; if it is a file, an 
    attempt will be made to use its directory as a parent. If all fails, 
    possibly due to restrictive permissions preventing directory creation, 
    the program will abort.
         There exists protection against the very real possibility
    that there may be files having the same name but in different directory 
    arguments. A 0 padded three digit number is inserted before the .jpg 
    or .JPG) suffix to make each name unique.
        Without the -c or --change option, no image processing will be done
    but the -i or --interactive option, provides an opportunity for a 'dry 
    run.' If neither of these is in effect, the program will abort. 
        The -v or -verbose option is what you'd expect.
    The -p or --prefix and -P or --postfix options are probably best left set 
    to their null string defaults. If you want to explicitly set one (or both)
    DO NOT use quotes unless it's to specify the null string; if you do, the 
    quotes will be part of the string! Since the null string is the default
    anyway, it should never be necessary to use quotes.
        It is possible to specify that images be rotated. L(eft (counter 
    clock wise) or r(ight (clock wise) are self explanatory. The a(uto option
    causes the program to make a decision based on EXIF data if available; 
    if EXIF data is not available, there will be no rotation. Interactive 
    mode gives the user the option to over ride rotation before processing 
    begins. It also allows the user to abort processing of the image currently 
    under displayed. 
        EXIF data is only available with images taken by high end cameras. 
    When it is available, most display programs will read this data and 
    display the photo in the correct orientation even though it is really not 
    that way in the file, so keep this in mind. When in doubt, use interactive 
    mode: the photo will be presented without any such correction.
        A log file may be specified using the -l or --logfile option. 
    Regardless of any such specification, log entries are appended to a file 
    Default_Temp_Log_Path which is created if it doesn't already exist. The 
    plan is to copy the relevant data for a particular run to the file 
    specified for that run (not yet implemented.) After the program is run a 
    few times, Default_Temp_Log_Path may get large and the data you might be 
    looking for will be at the end of it. Data from each run of the program 
    appears beneath a timestamp header line. Default_Temp_Log_Path is currently
    set to and will probably remain as '/tmp/picmod.log'. If this file gets
    very large, you can always edit it or simply delete it. Be aware that your
    system may intermittently delete files in /tmp so don't rely on this data
    being permanent.

    """

def handle_fatal_parsing_error(error):
    print """!!!!! Error parsing options: probably syntax error. !!!!!
Suggest: picmod -u for usage or picmod -m for man page.
Problem may be to do with: %s."""% error
    sys.exit(2)  

def log_message_to(message, logfilepath):
    try:
        log=open(logfilepath, 'a')
        log.write(message)
        log.close()
    except:
        print "Error writing to log file:", logfilepath
        sys.exit(2)
        
def new_dir (parent, dir):
    path = os.path.join(parent,dir)
    cmd = 'mkdir '+path
    try:
        os.system(cmd)
    except:
        return None
    if os.path.isdir(path):
        return path

def dir_is_writeable(dir):
    path=os.path.join(dir, Test_File_Name)
    try:
        test_fi=open(path, 'w')
    except:
        return False
    else:
        test_fi.close()
        os.system('rm '+path)
        return True
                       
def interp_rotation(text_input):
    """ inputs lrLRaA or cl, co allow for option interpretation
        inputs 0168 allow for EXIF data interpretation
        returns one of the following signed integers: 
        0 :  no rotation
        -90 :  rotate clockwise or to the right
        90 :  rotate counter-clockwise or to the left
        360 :  try to rely on EXIF data, else no rotation
        -hence meets the invarient that rotation must be one of these.
    """
    if text_input:
        if text_input[0] in ('01'):
            return 0
        elif text_input[0] in ('-lL8'):
            return 90
        elif text_input[0] in ('+rR6'):
            return -90
        elif text_input[0] in ('aA'):
            return 360
        elif len(text_input) > 1:
            if text_input[:2] in ('cl', 'Cl', 'CL'):
                return -90
            if text_input[:2] in ('co', 'Co', 'CO'):
                return 90
        else:
            return 0
    else:
        return 360

def interp_pre_post_fix(text_input):
    if text_input in ('""', "''"):
        return ''
    else:
        return text_input
    handle_fatal_parsing_error('designation of pre or post fix')

def is_image_file(filepath):
    return ((filepath[-3:] in ('jpg', 'JPG')) \
          and (filepath[:4]!=Default_Prefix))

def time():
    return str(datetime.datetime.now())

Timestamp_Truncation_Level=14  # to the level of seconds
def timestamp():      # Trunkated to seconds.
    t=datetime.datetime.now()
    ret = str.translate(str(t),None,' :.-')[:Timestamp_Truncation_Level]
    return ret
        
TimeStamp = timestamp()

#  Default values:
Default_Dir_Suffix='_pm.d'
Default_html_Suffix='_pm.html' #plan to eventually have an html page
Default_Verbose=False
Default_Interactive=True
Default_Process=False
Default_Max_Dimension=400
Default_Rotation=360
Default_Prefix='new_'
Default_Postfix=''
Default_Output_Directory=TimeStamp+Default_Dir_Suffix
Default_Create_html_File=False
Default_html_File=TimeStamp+Default_html_Suffix
Default_Temp_Log_Path='/tmp/picmod.log'
Default_Log_File_Name=''
Default_File_Args=[]
Test_File_Name='picmod.junk'
 

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
            file_args=Default_File_Args        ):

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
        self.temp_logfile=Default_Temp_Log_Path  # no user influence
        # the above attribute is only used by 'handle_arg'
        self.image_files=[]          # empty list, no user influence
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
        """ Handles each argument; recursively when appropriate. """
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
            if is_image_file(file):  # ck it's an IMAGE
                self.v('%s --> list.'%file)
                self.image_files.append(file)
            else:                    # report not IMAGE
                message='Ignoring non image file: %s\n' % file
                self.v(message,0)
                log_message_to(message, self.temp_logfile)

    def complete_calculable_values(self):
        """ 
        1. sets up all the image files into self.image_files,
                                a single list of full path names.
        2. sets up Default_Temp_Log_Path and reports managed problems to it.
        3. sets up the output directory.
        4. (Yet to be implemented: )determines final location for logfile and 
                moves current content of the temporary log file into it.   
        """
        # initialize self.temp_logfile for use by self.handle_arg()
        log_message_to('\n'+time()+': new run of picmod.py.\n', \
                                                        self.temp_logfile)
        
        timestamp_odir = timestamp()+Default_Dir_Suffix

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
            cwd=os.getcwd()
            possible_odir = new_dir(cwd, timestamp_odir)  
            if possible_odir and dir_is_writeable(possible_odir):     
                self.odir=possible_odir

        self.v('Begin traversal of arguments.')
        for file in self.file_args:
            fi=os.path.abspath(file)
            self.handle_arg(fi)

        if not self.odir:
            self.v('Begin search for an out_put_directory.')
            for path in self.image_files: 
                if self.odir:
                    break
                dir, file = os.path.split(path)
                possible_odir = new_dir(dir, timestamp_odir)
                if possible_odir and dir_is_writeable(possible_odir):
                    self.odir=possible_odir
                    self.v('Found $s to be out_put_directory.'%dir) 
        if not self.odir:
            message='FATAL ERROR: unable to establish an output directory!'
            self.v(message, 0)
            log_message_to(message, self.temp_logfile)
            sys.exit(2)
        else:
            message='Out put directory: '+ self.odir +'\n'
            self.v(message,0)
            log_message_to(message, self.temp_logfile)

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
            if b > a:
                longest = b
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
            except:
                return

        def rotation2text(n):
            if n == 0:
                return 'none'
            elif n == 90:
                return 'to left'
            elif n == -90:
                return 'to right'
            elif n == 360:
                return 'default or auto'

        """ The beginning of the body of def process(self):"""

        message= \
"""Beginning traversal of image files. If they are to be processed, 
their destination directory will appear below.\n"""
        if self.process:
            message=message+"%s.\n"%self.odir
        self.v(message,0)
        log_message_to(message, self.temp_logfile)
        for p in self.image_files:  # TRAVERSE
            save = self.process
            message= \
'#####################\n\
WILL TRY TO OPEN %s\n'%p
            self.v(message,0)
            log_message_to(message, self.temp_logfile)
            try:
                i=Image.open(p)
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
                verbose_text  = "\n\
##################################################\n\
Data: Orientation = %d and size (width, height) = %s.\n\
Proposed changes are Rotation : %s; and resizing to %s.\n"%\
(current_rotation, str(i.size), rotation2text(current_rotation), \
new_size)
                if self.interactive:
                    i.show()
                    response = raw_input(interactive_text)
                    if response:
                        if response[0] in '0n':
                            current_rotation=0
                        elif response[0] in 'Ll':
                            current_rotation=90
                        elif response[0] in 'Rr':
                            current_rotation=-90
                        elif response[0] in 'Aa':
                            save = False
                        else:
                            message=  \
'\tUninterpretable response ("%s"); will use defaults.\n'%response
                            print message,
                            log_message_to(message, self.temp_logfile)
                else:
                    self.v(verbose_text)
                    log_message_to(verbose_text, self.temp_logfile)

                if save:
                    file=self.prefix+os.path.basename(p)+self.postfix
                    out_file=toolbox.no_dups(file, self.out_files)
                    out_path=os.path.join(self.odir, out_file)
                    message=  \
                        'Rotation: %d; Size: %s; to be saved as %s.\n' \
                        % (current_rotation, str(new_size), out_file)
                    log_message_to(message, self.temp_logfile)
                    self.v(message,0)
                    i=i.resize(new_size, Image.ANTIALIAS)
                    if current_rotation!=0:
                        i.rotate(current_rotation)
                    i.save(out_path)
                else:
                    message= \
                    '\tChanges- Rotation:%d; Size: %s, not made or saved.\n'\
                    % current_rotation, str(new_size)
                    self.v(message,0)
                    log_message_to(message,self.temp_logfile)



def set_options():
    globals = Specs()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "?uhvqicm:r:p:P:d:l:",  \
        ['usage', 'help', 'man', 'verbose', 'quiet', 'interactive', 'change',
        'max=', 'rotation=', 'prefix=', 'Prefix=', 'directory=', 
        'htmlCreate', 'htmlFileName=', 'logfile='])
    except getopt.GetoptError,err:
        # print help info and exit
        print str(err)  # will print something like 'option -a not recognized.'
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == '--conditions':
            conditions()
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
        if 0 == '--htmlCreate':
            globals.create_html_file=True
        if 0 == '--htmlFileName':
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

    print 'Globals as discovered from cmd ln options:'
    if globals.verbose:
        print 'verbose is set:'
        print globals.__str__()

    if not globals.verbose:
        print 'verbose not set but printing anyway:'
        print globals.__str__()

    j=raw_input('<---! to continue')

    globals.complete_calculable_values()

    print 'Globals after processing of cmd ln optioins:'
    if globals.verbose:
        print 'verbose is set:'
        print globals.__str__()

    if not globals.verbose:
        print 'verbose not set but printing anyway:'
        print globals.__str__()

    print 'Now for processing; here goes!'
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
"""
                
            """
