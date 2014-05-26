#!/usr/bin/env python
# file :  picmod_text.py, part of picmod package
# textual data imported by picmod.py
# Tue Aug  3 20:28:34 PDT 2010

what_am_i = \
"""
This is in a file called "picmod_text.py"
It is a module used by "picmod.py"
This module is for the sole purpose of moving the long bits of text out
of the main picmod module to make it more managable for analysis and 
development.
There is no actual functioning code in this file/module.
It contains only the text constants used by picmod.
"""

copyright_text = \
"""
    "picmod" stands for "picture modifier": 
        it provides for shrinkage and rotation of jpeg image files.
        It also can create an html page showing the processed images,
        thus allowing for rapid deployment to a web server.

    Copyright (C) 2009, 2010  Alexander Kleider 

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
"""

intro_text = \
"""
    picmod  Copyright (C) 2009, 2010 Alexander Kleider
    This program comes with ABSOLUTELY NO WARRANTY; 
    This is free software, and you are welcome to redistribute it
    under certain conditions;
    for details rerun the program as follows: picmod.py --conditions

If you are not sure what to do, use CTL-C to quit this program, and then
try picmod --usage or picmod --man (picmod --man | pager will be better:-)

Contact: Alex Kleider, P.O. Box 277, Bolinas, CA 94924 USA    alex@kleider.ca
Copyright 2010 Alexander Kleider (alex@kleider.ca)
"""

WebPage = \
""" <!-- a web page created by picmod 
Copyright 2010 Alexander Kleider (alex@kleider.ca)
    This file is part of picmod.  (...or has been generated by it.)

    Picmod is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.  

    Picmod is distributed in the hope that it will be useful, but WITHOUT 
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public 
    License for more details. If you did not receive a copy of the license 
    along with picmod, see <http://www.gnu.org/licenses/>.

# This file consists of text that can be used as a format string.
# The picmod program uses it with the format operator and a 4-tuple.
# Items of the tuple specify:
# 0. the path name of a .css file, 
# 1. a time stamp, 
# 2. the directory housing the photos, and 
# 3. a multi line  string containing the HTML "<img src=..." references, 
# one per line, for each of the photos.

-->
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html>
<head>
<title> picmod Web page </title>
<link rel="stylesheet" type="text/css" href="%s">
</head>

<div id="container">
<body>
<h1> picmod Photos </h1>
<p> These photos were generated by the picmod program by its %s time stamped
run. Look in %s for the photos themselves. This is provided for you to serve
as a template for a web page you may want to make out of the photos.</p>
<p> Clearly you will want to edit it to suit your own purposes. The frame work
is here to make it easier.</p>
%s
<!--
<h3> OTHER LINKS </h3>
<ul>
<li> <a href="./next_page.html">Next page</a></li>
<li> <a href="./previous_page.html">Previous page</a></li>
<li> Link back to: <a href="../sub_index.html">contents</a></li>
<li> Link back to: <a href="../index.html">main page</a></li>
</ul>
-->
</body>
</div>
</html>
"""


def usage():
    print """ picmod usage statement
    picmod.py options arguments:
"?uhvqicm:r:p:P:d:l:", 
['conditions', 'usage', 'help', 'man', 'verbose', 'quiet', 
'interactive', 'change', 'htmlCreate', 'htmlFileName', 
'max=', 'rotation=', 'prefix=', 'Prefix=', 'directory=', 'logfile='] 
file_name_arguments
If you do not use the -c(hange option, no processing will be done.
Typical usage: picmod.py -cq --htmlCreate <imagefile(s) &/or directory(ies)>
"""

def man():
    print """ picmod man page
    NAME  picmod.py  -  Photo processing utility.

    SYNOPSIS
        picmod.py [-?uhvqic] [-m max_dimension] [-r rotation] [-p prefix ] \
        [-P postfix] [-d directory] [-l logfile] files.. directories..

    SUGGESTED USAGE
        if you have a high end camera that provides EXIF Orientation data:
            picmod.py -qc[m 500] --htmlCreate <image files>
        if not and if you have some portrait shots in your collection:
            picmod.py -qic[m 500] --htmlCreate <image files>
        The optional -m 500 (the [] should NOT be included either way) 
        parameter can be set to what ever number you want or left out if
        you like my default which is a little under 500 pixels in the 
        picture's maximum dimension.
        Replace <image files> with a space separated sequence of the image 
        files or directories containing such files. 

    OPTIONS
        -?, -h, -u :  print a usage statement.
        -v : verbose- provides extra output during program execution.
            default is True
        -i : interactive- provides data, shows images, and accepts user input.
            default is True
        -q : quiet- sets both verbose and interactive to false;
            If you want verbose or interactive but not the other,
            use -q followed by -v or -i, which ever you want
        -c : change- with out this option, nothing is processed.
        -m max : processed image will be shrunk to fit into a max pixels
            square without distortion. I've set a default that best fits 
            my web page. -m 500 will reset it to 500 pixels (a tiny bit too 
            big for my purposes.)
        -r rotation : 0, n, a, -, l, co, +, r, cl
            0, n(o rotation
            a(uto is the default: this assumes EXIF data is available.
                defaults to no rotation if data is not available.
            -, l(eft, co(nter clockwise.
            +, r(ight, cl(lockwise
            If your camera does not provide EXIF "Orientation" data you'd be
            well advised to use interactive mode: -i
        -p prefix :  designates a prefix for output file, default is ''
            There's really no need to use this or the next option unless
            you want to go out of your way to put the new files in the same
            directory as the originals.
        -P postfix : designates a postfix, default is ''
        -d directory :  an out put directory name may be specified.
            The plan is to use a time stamped default but current 
            implementation is to use 'ts' as a default output directory name.
        -l logfile :  a log file may be specified.
               This has not yet been implemented and I've no immediate plan
               to do so since there is a default file you can consult in 
               /tmp/picmod.log

        Long options are also available. 
        Those that have corresponding short options will be obvious:  
        --usage, --help, --man, --verbose, --quiet, --interactive, --change,
        --max, --rotation, --prefix, --Prefix, --directory, --logfile

        Other long options:
        --htmlCreate :  if set, an html file will be created with refs to the 
            output files so the images can be examined with a browser and 
            the text of the html used in web design.
        --htmlFileName :  the user may specify a name for this file but
            need not since a default is provided.
        --conditions : this one simply prints copyright information and exits.

    ARGUMENTS
        Arguments can be image files or directories containing image files.

    NOTES:
        The basic functionality of this program is to downsize image files,
        rotate them if need be and to create an html page which shows 
        the images.
    
    Image files are assumed to end in one of the strings defined in the
    'Image_Suffix_Tuple' constant currently set as: 
    ('.jpg', '.JPG', 'tiff', 'TIFF', '.png', '.PNG')
    Other files are simply ignored after they are reported in the log.
    A none image file with such a sufix will probably be ignored (although
    this has yet to be tested.)

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
    arguments. A 0 padded three digit number is inserted before the four
    character suffix (i.e. ".jpg")
        Without the -c or --change option, no image processing will be done
    but the -i or --interactive option, provides an opportunity for a 'dry 
    run.' If neither of these is in effect, the program will abort. 
        The -v or -verbose option is what you'd expect (but it can get 
    somewhat tedious.)
        The -p or --prefix and -P or --postfix options are probably best 
    left set to their null string defaults. If you want to explicitly set 
    one (or both) DO NOT use quotes. Quotation marks will be part of the 
    string. You would only need to use quotes to specify the null string
    and since that is already the default, there's no need. ..so I repeat,
    do not use quotation marks.
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

if __name__ == "__main__":
    print what_am_i

