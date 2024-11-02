import copy
import json
import asyncio
from collections import defaultdict
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
from pathlib import Path

from updater.utils.ai_handler import get_openai_response_struct

from updater.utils.reddit_handler import get_subm_from_subm_id, load_all_subm_comments
from updater.pipeline.prep_subm_for_llm import prep_subm_for_llm

# Given subm data, split into blocks, then return a list of opinions
async def identify_opns(prepped_for_llm_subm_data: dict, pd_category: str) -> list[dict]:
  blocks = split_replies(prepped_for_llm_subm_data)
  block_count = len(blocks)
  print(f'\nSubmission split into {block_count} block(s)')
  
  tasks = [asyncio.create_task(process_block(block, i, block_count, pd_category)) for i, block in enumerate(blocks)]
  results = await asyncio.gather(*tasks)
  # Unpack results from list of lists to a single list of dicts, filtering out None values
  flat_extracted_opns = [opn for extracted_opns in results if extracted_opns is not None for opn in extracted_opns]
  
  return flat_extracted_opns


# Given subm data, split along replies into blocks, return list of blocks
def split_replies(data: dict, max_chars: int=5000) -> list[dict]:
  base_data = {key: value for key, value in data.items() if key != 'replies'} # Create a base data dict without replies
  
  blocks = []
  current_block = copy.deepcopy(base_data) # Start a block with the base data
  current_block['replies'] = []
  current_size = len(json.dumps(current_block, indent=2, ensure_ascii=False))

  # For each first level reply...
  for reply in data['replies']:
    reply_size = len(json.dumps(reply, indent=2, ensure_ascii=False))

    if current_size + reply_size > max_chars and len(current_block['replies']) == 0: # Sepcial check - If adding first reply already exceeds max_chars on its own
      current_block['replies'].append(reply)
      blocks.append(current_block)

      # Start a new block
      current_block = copy.deepcopy(base_data)
      current_block['replies'] = []
      current_size = len(json.dumps(current_block, indent=2, ensure_ascii=False))
      continue
    
    elif current_size + reply_size > max_chars: # If adding current reply will exceed,
      blocks.append(current_block) # add current block to list of blocks, 
      current_block = copy.deepcopy(base_data) # then start a new current block with base data
      current_block['replies'] = []
      current_size = len(json.dumps(current_block, indent=2, ensure_ascii=False)) # reset current size to base size

    current_block['replies'].append(reply) # Add reply to current block
    current_size += reply_size # Update current size

  if current_block['replies']: # Add the last block if it has any replies
    blocks.append(current_block)

  return blocks

# Given a block, return a list of opinions
async def process_block(block: dict, index: int, block_count: int, pd_category: str) -> list[dict]:
  class Sentiment(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

  class Verbatim(BaseModel):
    positive: Optional[list[str]] = Field(description="Quotes suggesting Redditor's positive sentiment for the product, if applicable")
    neutral: Optional[list[str]] = Field(description="Quotes suggesting Redditor's neutral sentiment for the product, if applicable")
    negative: Optional[list[str]] = Field(description="Quotes suggesting Redditor's negative sentiment for the product, if applicable")

  class OpinionSummary(BaseModel):
    verbatim: Verbatim
    overall_sentiment: Sentiment = Field(description="The Redditor's overall sentiment for the product. Can be positive, neutral, or negative.")

  class Opinion(BaseModel):
    opinion_summary: OpinionSummary
    username: str = Field(description="Username of Redditor with the opinion")
    pd_brand: Optional[str] = Field(description=f"Brand of the {pd_category}")
    pd_model_or_name: Optional[str] = Field(description=f"Model or name of the {pd_category}")
    pd_key_specs: Optional[str] = Field(description="Key specs - technical specs only e.g. Polycarbonate, 41L, QLED etc). Exclude high level descriptions made by the Redditor about the product, such as lightweight, compact, portable, etc.")
    pd_url: Optional[str] = Field(description=f"Url of the {pd_category}. Exclude query parameters (everything after the ?)")

  class Opinions(BaseModel):
    opinions: Optional[list[Opinion]] = Field(description="If there are no valid opinions, let this field be None or null (as in not the str).")
  
  print(f'Identifying opn for block {index + 1} of {block_count}...')
  
  block_json_str = json.dumps(block, indent=2, ensure_ascii=False)  
  
  sys_prompt, user_prompt = load_identify_opn_prompts(index, block_json_str, pd_category)
  model = 'gpt-4o'
  
  response_format = Opinions
  llm_response = await get_openai_response_struct(sys_prompt, user_prompt, model, response_format, 'identify_opns')
  llm_response_dict = llm_response.model_dump(mode='json') if llm_response else None
  opinions_list = llm_response_dict['opinions'] if llm_response_dict else []
  return opinions_list

def load_identify_opn_prompts(index: int, block_json_str: str, pd_category: str) -> tuple[str, str]: 
  # If not first block, set extra instructions, otherwise leave blank
  if index > 0:
    extra_instructions = ' Do not extract opinions from the submission text, only from the replies.'
  else:
    extra_instructions = ''
    
  current_dir = Path(__file__).parent
  sys_prompt_path = current_dir.parent / "llm_prompts" / "identify_opn_sys.txt"
  with open(sys_prompt_path, "r") as file:
    sys_prompt = file.read()
  sys_prompt = sys_prompt.replace("__EXTRA_INSTRUCTIONS__", extra_instructions)
  
  user_prompt = f'Extract opinions on "{pd_category}" from this Reddit thread from Redditors who have owned them.{extra_instructions}\n\nReddit thread:\n```\n{block_json_str}\n```'
  
  return sys_prompt, user_prompt





if __name__ == '__main__':
  sys_prompt, user_prompt = load_identify_opn_prompts(1, 'testing block json string', 'testing pd category')
  print(sys_prompt)
  print('\n\n')
  print(user_prompt)



  
