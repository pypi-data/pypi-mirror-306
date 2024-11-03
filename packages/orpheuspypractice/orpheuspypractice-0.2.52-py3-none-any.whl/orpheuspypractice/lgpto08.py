#%%
import os
from click import prompt
import dotenv
from langchain import hub

#%%

dotenv.load_dotenv()

#%%
#from dotenv in ./.env , load key

try:
        
    api_key_variable = "OPENAI_API_KEY"
    keyname="OPENAI_API_KEY_olca"

    api_key_lcpractices2409 = os.getenv(keyname)
    #print(api_key_lcpractices2409)
    os.environ[api_key_variable] = api_key_lcpractices2409
except :
    pass

#%%

# First we initialize the model we want to use.
from json import load
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent

from langchain_community.agent_toolkits.load_tools import load_tools

import warnings
#

# Suppress the specific UserWarning
warnings.filterwarnings("ignore", category=UserWarning, message="The shell tool has no safeguards by default. Use at your own risk.")

from langchain_community.tools.shell import ShellTool

shell_tool = ShellTool()


model_name="gpt-4o"
model_name="gpt-4o-mini"
recursion_limit=80

model = ChatOpenAI(model=model_name, temperature=0)


# For this tutorial we will use custom tool that returns pre-defined values for weather in two cities (NYC & SF)

from typing import Literal

from langchain_core.tools import tool


@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


tools = [get_weather, shell_tool]

# tool_name_arxiv = "arxiv"
# arxiv_tool=load_tools([tool_name_arxiv])
# tools=tools+arxiv_tool

tools

#%%
# Define the graph

from langgraph.prebuilt import create_react_agent

graph = create_react_agent(model, tools=tools)
if graph.config is None:
    graph.config = {}
# Increase recursion limit
graph.config["recursion_limit"] = recursion_limit

from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))


# %%
def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

# # %%

user_input="Summarize all issues about LangGraph (or Langraph or Agency Designer) ."
user_input="Summarize all issues about Session review for creation.  Check for label #pch (meaning Primary Choice)"
user_input="Summarize all issues about Primary Choice and the creative process (or Structural Tension)"
user_input="You search for pattern in issue title : Pyra and you explore each comments, create an overview, the plot, the characters and the setting.  You follow your system instructions to prepare action.  Look especially content in issue #214 #215 and their related project custom fields."
user_input="You search for pattern in issue title : Pyra and you explore each comments, create an overview, the plot, the characters and the setting.  You follow your system instructions to prepare action.  Look especially content in issue #214 #215 and their related project custom fields.  Look all the file in the current directory and subdirectory to find any information that can help you in your task.  The file: Pyra25k2410112008e2story.md is a good start."
user_input="You search for pattern in issue title : Pyra and you explore that with other issues with IDs: [228,227,226,225,224].  You follow your system instructions to prepare action.  Look especially content in issue #214 #215 and their related project custom fields.  Look all the file in the current directory and subdirectory to find any information that can help you in your task.  The file: 223-Synopsis.md is a good start. "

system_instructions="You are an assistant that has access to filesystem (and you are authorized to create directory and write,change files) and we are in a github repository that has multiple issues in the github platform.  You specialize in retrieving a cache in the subfolder ./cache/issues in which you store the issues that you have retrieved from the github platform and you execute what you are asked for such as grouping them into topics or what the user asks for. (ISSUES ARE IN THIS REPO, use the gh tool to retrieve them.).  Produce a report you make from the request and append it to report_issues.md.  Also retrieve their related project if they have any.  Make this great in the report with links to open any resources you have reported on.  You can also summarize a one paragraph based on all retrieved issues.  Add a separator at the end of your report and a header with datetime.  Add files you created or appended to git and commit them with an adequate message referencing issue #229 and push the changes.  Report on your action into the file history_of_actions.md.  If you are asked to create a new issue to associate everything to, do so and ignore the number above.(Dont comment your final results, just output it.) For issues that are the most relevant, retrieve their comments and summarize them in the report. Create a safe name directory where you put reports and files based on what you are asked.  ((In current directory, Write (or append) yourself a file called ./instructions.txt where you put what you learned to do (example: how to retrieve issues and their related project.  If that file exist, you read it to learn how to do your job.))). You also read that file for instructions for such action like creating git tag at significant moment of your iterative process.  REMEMBER: You are authorized to modify, create directory/files in the current directory.  If you keep having the same mistake and can not resolve, stop your loop and report to the user what is going on.Produce a full report and try to construct a plot of the stories being written by understanding the issues.  You can also expand your seach of issues to find what is being learned to innovate story-telling.  Make sure you commit the work to issue #231. You push tags and commits as you create them in parallel to your work"

system_instructions = """
You are an assistant that has access to the filesystem (and you are authorized to create directories and write/change files) and we are in a GitHub repository that has multiple issues on the GitHub platform. You specialize in retrieving a cache in the subfolder ./cache/issues in which you store the issues that you have retrieved from the GitHub platform and you execute what you are asked for such as grouping them into topics or what the user asks for. (ISSUES ARE IN THIS REPO, use the gh tool to retrieve them.)

Tasks:
1. Retrieve issues and store them in ./cache/issues.
2. Group issues into topics or as requested by the user.
3. Produce a report based on the retrieved issues and append it to report_issues.md.
4. Include links to open any resources mentioned in the report.
5. Summarize the retrieved issues in one paragraph.
6. Add a separator and a header with the current datetime to the report.
7. Commit and push changes to the repository, referencing issue #229.
8. Document your actions in history_of_actions.md.
9. If required, create a new issue to associate all findings and ignore the issue number above. (make sure though you keep track, commit and push changes).
10. For the most relevant issues, retrieve and summarize their comments in the report.
11. Create a safe-named directory for reports and files based on the task.
12. Write or append instructions to ./instructions.txt on how to perform tasks (e.g., retrieving issues and related projects). Read this file for guidance on tasks like creating git tags.
13. If you encounter repeated errors and cannot resolve them, stop and report the issue to the user.
14. Produce a comprehensive report and attempt to construct a plot of the stories being written by understanding the issues.
15. Expand your search of issues to explore innovations in storytelling.
16. Commit the work to issue #231 and push tags and commits as you create them.
17. Retrieve all issues (dont limits yourself to 100)
18.  You make sure you look at the specified files from the user.  Be creative
19.  To reduce token amount, you distillate the information each time you execute anything and lower the amount of exchanged messages and size of conversation. (Example, when you retrieve issues using gh, segment the number you retrieve using the --limit option, iterate thru the issues and distil them, save some cache then continue with the next segment.  Be very compact, balancing keeping the essence of information in the issues and content you analyze.)
20.  When you do a new iteration (looping) you output that number to the standard output along with what is your plan (format this into obvious markdown output)

Remember:
- You are authorized to modify and create directories/files in the current directory.
- Do not comment on your final results; just output them but keep logging your action steps you do internally (all reflexion and actions steps)
"""

user_input = """
You search for pattern in issue title: Pyra and you explore that with other issues with IDs: [228, 227, 226, 225, 224]. You follow your system instructions to prepare action. Look especially at the content in issue #214 and #215 and their related project custom fields. Look at all the files in the current directory and subdirectory to find any information that can help you in your task. The file: 223-Synopsis.md is a good start.  You also can use : Pyra25k2410112008e2story.md to get inspired from our previous version.
"""


def prepare_input(user_input, system_instructions):
    inputs = {"messages": [
    ("system",
     system_instructions),
    ("user", user_input     )
    ]}
        
    return inputs

inputs = prepare_input(user_input, system_instructions)
print_stream(graph.stream(inputs, stream_mode="values"))
# %%


