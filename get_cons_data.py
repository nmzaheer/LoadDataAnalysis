"""
Consumer Data Extraction
_ _ _ _ _ _ _ _ _ _ _ _ _
- - - - - - - - - - - - -

This script will extract consumer data like Consumer ID, Type of Consumer
and Consumption details from the URL given
"""

import base64
import re
import urllib
import urllib2



def get_cons_data(cons_no):
    """ Gets data of the given Consumer Number and writes it to a database

    Args:
        cons_no: A string containing the Consumer Number

    Returns:
        None

        
        A dict containing Consumer Number, Type of Consumer. Assessment Date
        and Reading details is written to a database. For example

        cons_data = {'cons_no':'0842411563', 'type':'LA1A',
        'ass_date':'22/07/2013', 'units_cons':[500,645,458,485,586]}
    """
    
