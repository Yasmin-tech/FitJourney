import os
from mega import Mega

mega = Mega()
m = mega.login(os.getenv('MEGA_EMAIL'), os.getenv('MEGA_PASSWORD'))
