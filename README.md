# PlatFormerGame

this is a python project where I will try to make a platform (scroller) game.  this will be done following a tutorial here:  https://www.youtube.com/watch?v=6gLeplbqtqg



I set up a virtual env, and intalled pygame.  see below on how to do a venv.

set up a venv to handle this.
        1)  Clone code into a local directory
        2)  set up virtual enviroment with this command  
                  python3 -m venv your_dir_name
        3)  activate enviroment.
                a) windows:  source ./dirname/Scripts/activate
                b) linux:  source dirname/bin/activate
        3)  install the requests library with this command
                a) pip3 install requests
        4)  generate your requirements.txt file for other machines
            a)  pip freeze > requirements.txt
            
    2)  when setting your enviroment, and you've got this off of github you run a install using the requirements file
            a)  pip3 install -r requirements.txt   -- this will install  into your virtual directory.  
    3)  when all done,  to deactivate the venv  use deactivate 
