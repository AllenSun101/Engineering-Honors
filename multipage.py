# Import necessary libraries 
import streamlit as st

# Define the multipage class to manage the multiple apps in our program 
class MultiPage: 
    """Framework for combining multiple streamlit applications."""

    def __init__(self) -> None:
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.pages = []
    
    def add_page(self, title, func, *args, **kwargs) -> None: 
        """Class Method to Add pages to the project
        Args:
            title ([str]): The title of page which we are adding to the list of apps 
            
            func: Python function to render this page in Streamlit
        """

        self.pages.append(
            {
                "title": title, 
                "function": func,
                "args": args,
                "kwargs": kwargs
            }
        )

    def run(self):
        # Dropdown to select the page to run  
        st.sidebar.image('Logo.png', width=200)
        st.sidebar.title("Engineering Honors Activities")
        st.sidebar.write("### Select your dashboard")
        page = st.sidebar.selectbox(
            'Dashboard:', 
            self.pages, 
            format_func=lambda page: page['title']
        )

        # Disappear when the sidebar changes
        appears = True
        if appears:
            st.sidebar.write("Semester: Get Value")
            st.sidebar.write("Event: Get Value")
            st.sidebar.write("Major: Get Value")
            st.sidebar.write("Class: Get Value")


        # run the app function 
        page['function'](*page["args"], **page["kwargs"])