import streamlit as st

from streamlit_option_menu import option_menu

import account
import about
import trending
import your_posts
import home

#from account import load_users

st.set_page_config(page_title="ScholarWings"
)

class MultiApp:

    def __init__(self):
        self.apps = [] 
    def add_app(self, title, function, app):
        self.apps.append({
            "title": title,
            "function": function
        })

   # def run(self):  # Updated indentation
       # with st.sidebar:
            # Rest of the code remains the same


    def run():

        with st.sidebar:    

            app = option_menu(
                menu_title= 'ScholarWings',
                options=['Home','Account','Trending', 'Your posts', 'about'],
                icons=['house-fill','person-circle','trophy-fill', 'chat-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
          "container": {"passing": "5!important","background-color":'black'},
          "icon":{"color":"white", "font-size": "23px"}, 
          "nav-link":{"color":"white","font-size": "20px", "text-align": "left", "margin":"0px"}
          #"nav-link-selected":{"background-color":"#02ab21"}
          })

       
        if app=='Account':
            account.app()
        if app=='Home':
            home.app()
        if app=='Trending':
            trending.app()
        if app=='about':
            about.app()
        if app=='Your posts':
            your_posts.app()
          

    run()