Compare Requirements
####################
Python utility to compare requirements files. Very useful for comparing your 
installed dependencies (pip freeze) vs dependencies in requirements.txt

.. code-block::
    
    cmpreqs[ <file 1>[ <file 2>]][ --pipdeptree]
    
Available arguments:
    
    * **file1**: First file to compare. By default requirements.txt
    * **file2**: Second file to compare. By default ``pip freeze`` output.
    * **--pipdeptree**: Use pipdeptree instead ``pip freeze`` and show only dependencies that have not been installed by other dependencies.


Output example::
    
    Different dependencies
    ======================
    Name                  requirements.txt  Input 2
    --------------------  ----------------  -------
    py3dns                None              3.1.0  
    django-reversion      2.0.6             1.10.2 
    python-memcached      1.50              1.58   
    
    Equal dependencies
    ==================
    Name                                  Version
    ------------------------------------  -------
    django-hosts                          2.0    
    mailgun2                              0.1.4  
    django-q                              0.7.15 
    
    Only available on requirements.txt
    ==================================
    Name                              Version                                 
    --------------------------------  ----------------------------------------
    django-tables2                    0.15.0 
    requests                          2.11.1                                  
    django_easy_select2-dev           50522d1c71ff19a2124fa735b765ae88f9b859c1
    pytz                              2016.6.1
    
    Only available on Input 2
    =========================
    Name                         Version     
    ---------------------------  ------------
    django-registration-redux    1.1         
    ipython                      2.4.0       
    Markdown                     2.5.2       
    django-phonenumber-field     0.7.1 
