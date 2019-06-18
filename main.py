#!/usr/bin/python3

from database.scheme import Song 
from database.database import get_session,save_recommendations
from api.app import main



if __name__=="__main__":
    # fill_streams()    
    main()