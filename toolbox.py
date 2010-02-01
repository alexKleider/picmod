#!/usr/bin/env python
# toolbox.py

def no_dups(fname, t, len=3, place=-4):
    """ Assumes fname is a (?file?) name which is to be placed into t, a list.
    This is to be done in such a way that no duplicates can occur in the list.
    If fname does not already exist in t, it is appended.
    If fname already exists in t, it will be modified and then appended.
    Modification consists of inserting a len character long, zero padded
    number (beginning with 1 and incremented as needed) beginning at 
    fname[place].
    For example: photo.jpg might become photo001.jpg.
    The inserted file name is returned, whether it be the original 
    or a modification.
    This function works even if len(fname) is less than places. It even works
    if fname is an empty string!
    """
    n =0
    name=fname
    s='%0'+str(len)+'d'
    while name in t:
        n=n+1
        insert = s%n
        name=fname[:place]+insert+fname[place:]
    t.append(name)
    return name

if __name__ == '__main__':
    my_list=['f', 'f.jpg', 'f001.jpg', 'f002.jpg']
    name = 'f'
    stored_name=no_dups(name, my_list)
    print stored_name
    print my_list


