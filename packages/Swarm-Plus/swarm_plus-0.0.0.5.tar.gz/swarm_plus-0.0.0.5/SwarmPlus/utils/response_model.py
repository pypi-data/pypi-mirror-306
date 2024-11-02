# Create output class
from pydantic import BaseModel
from typing import List

class AssistantData(BaseModel):
    agent_name:str
    messages :list=[]

class Agentoutput(BaseModel):
    agent_name:str
    response:str
    messages:list=[]
    assistant_agents:List[AssistantData]=[]