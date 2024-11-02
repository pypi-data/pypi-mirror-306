from updater.utils.db_handler import db_get_specs_filters_by_brand_id, db_update_product_specs
from updater.utils.ai_handler import get_openai_response_instr, get_perplexity_response
import asyncio
from pathlib import Path
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

# Initialize current directory
current_dir = Path(__file__).parent


### Main function - checks for missing specs and updates them
async def check_n_update_specs(product: dict, pd_category_dict: dict) -> None:

  # Get specs_filters from pd_category
  specs_filters = pd_category_dict['specs_filters']
  
  if specs_filters:
    # Create list to store all tasks
    tasks = []
    
    # Check if product already has specs that pd_category needs
    for spec_filter in specs_filters:
      if spec_filter['label'] not in product['specs']:
        print(f'Product spec {spec_filter["label"]} missing for product_id {product["id"]}, proceeding to get and update...')
        task = asyncio.create_task(get_spec(spec_filter, product))
        tasks.append(task)
      else:
        print(f'Product spec {spec_filter["label"]} exists for product_id {product["id"]}, skipping.')
    
    # Gather all specs and update product
    if tasks:
      specs_results = await asyncio.gather(*tasks)
      # Filter out None results and merge all dictionaries
      specs_to_update = {}
      for spec_dict in specs_results:
        if spec_dict:  # Only update if not None
          specs_to_update.update(spec_dict)
      product['specs'].update(specs_to_update)
      # Update spec in products table in db
      await db_update_product_specs(product['id'], product['specs'])
  else:
    print(f'No specs_filters found for pd_category: {pd_category_dict["name"]}, skipping...')
     
### Get and update single spec
async def get_spec(spec_filter: dict, product: dict):
  
  product_title = product['title']
  product_features = product['amzn_features']
  product_features_str = '- ' + '\n- '.join(product_features) if product_features else ''
  spec_label = spec_filter['label']
  
  # Try to get spec...
  if spec_filter['type'] == 'range':
    spec_units = spec_filter['units']
    
    spec = await get_range_spec_from_amzn_info(spec_label, spec_units, product_title, product_features_str)
    if spec is None:
      perplex_answer = ask_perplexity_for_spec(spec_label, spec_units, product_title)
      spec = await extract_range_spec_from_perplexity_answer(perplex_answer, spec_label, spec_units)
  
  elif spec_filter['type'] == 'options':
    spec_options = spec_filter['options']
    spec = await get_options_spec_from_amzn_info(spec_label, spec_options, product_title, product_features_str)
    if spec is None:
      perplex_answer = ask_perplexity_for_spec(spec_label, spec_options, product_title)
      spec = await extract_options_spec_from_perplexity_answer(perplex_answer, spec_label, spec_options)
  
  print(f'-> Spec {spec_label}: {spec}')
  
  if spec:
    return spec
  else:
    return {spec_label: 'error'}
    
    
    
    
    
### Try to extract range spec from amazon product title and features
async def get_range_spec_from_amzn_info(spec_label: str, spec_units: list, product_title: str, product_features_str: str):
  
  # Load and configure LLM prompts
  sys_prompt_path = current_dir.parent / "llm_prompts" / "get_range_spec_from_amzn_info_sys.txt"
  with open(sys_prompt_path, "r") as file:
    sys_prompt = file.read()
    
  user_prompt_path = current_dir.parent / "llm_prompts" / "get_range_spec_from_amzn_info_user.txt"
  with open(user_prompt_path, "r") as file:
    user_prompt = file.read()
  user_prompt = user_prompt.replace('__spec__', spec_label).replace('__title__', product_title).replace('__features__', product_features_str)
  
  # Define model for LLM
  UnitsEnum = Enum('UnitsEnum', {unit.upper(): unit for unit in spec_units})
  class IdentifiedSpec(BaseModel):
    value: Optional[float] = Field(description="The value of the requested specification of the product")
    units: Optional[UnitsEnum] = Field(description="The unit of the requested specification of the product")  # type: ignore

  # Define other LLM parameters
  response_model = IdentifiedSpec
  model = 'gpt-4o-mini'
  temp = 0
  
  # Get LLM response
  llm_response = await get_openai_response_instr(sys_prompt, user_prompt, model, temp, response_model)
  llm_response_dict = llm_response.model_dump(mode='json') if llm_response else None
  value = llm_response_dict['value'] if llm_response_dict else None
  units = llm_response_dict['units'] if llm_response_dict else None
  
  # Return spec
  spec = {spec_label: {'type': 'range', 'value': value, 'units': units}} if value is not None else None
  return spec
  
  
  
### Try to extract options spec from amazon product title and features
async def get_options_spec_from_amzn_info(spec_label: str, spec_options: list, product_title: str, product_features_str: str):
  
  options_str = '- ' + '\n- '.join(spec_options)
  
  # Load and configure LLM prompts
  sys_prompt_path = current_dir.parent / "llm_prompts" / "get_options_spec_from_amzn_info_sys.txt"
  with open(sys_prompt_path, "r") as file:
    sys_prompt = file.read()
    
  user_prompt_path = current_dir.parent / "llm_prompts" / "get_options_spec_from_amzn_info_user.txt"
  with open(user_prompt_path, "r") as file:
    user_prompt = file.read()
  user_prompt = user_prompt.replace('__spec_label__', spec_label).replace('__spec_options__', options_str).replace('__title__', product_title).replace('__features__', product_features_str)
  
  # Define model for LLM
  OptionsEnum = Enum('OptionsEnum', {option: option for option in spec_options})
  class CorrectSpec(BaseModel):
    correct_spec: Optional[OptionsEnum] = Field(description="The correct spec from the list of options") # type: ignore
  
  # Define other LLM parameters
  response_model = CorrectSpec
  model = 'gpt-4o-mini'
  temp = 0
  
  # Get LLM response
  llm_response = await get_openai_response_instr(sys_prompt, user_prompt, model, temp, response_model)
  llm_response_dict = llm_response.model_dump(mode='json') if llm_response else None
  correct_spec = llm_response_dict['correct_spec'] if llm_response_dict else None
  
  # Return spec
  spec = {spec_label: {'type': 'options', 'value': correct_spec}} if correct_spec else None
  return spec

# Generate google search query to find spec
def ask_perplexity_for_spec(spec_label: str, units_or_options: list, product_title: str):
  print(f'Asking Perplexity for spec: {spec_label}, for product: {product_title}')
  
  units_or_options_str = ' / '.join(units_or_options)
  
  # Setup LLM prompts
  sys_prompt = 'Answer concisely without explanation.'
  user_prompt = f'What is the spec for the following product?\n\nProduct: {product_title}\nSpec to identify: {spec_label} ({units_or_options_str})'
  
  # Define other LLM parameters
  model = 'llama-3.1-sonar-small-128k-online'
  temp = 0
  
  # Get perplexity response
  perplexity_response = get_perplexity_response(sys_prompt, user_prompt, model, temp)
  
  return perplexity_response
  

async def extract_options_spec_from_perplexity_answer(perplexity_answer: str, spec_label: str, spec_options: list):
  options_str = ' / '.join(spec_options)
  
  # Setup LLM prompts
  sys_prompt = 'You are a helpful and meticulous assistant.'
  user_prompt = f'From the statement, identify the correct spec from the spec options:\n\nStatement: {perplexity_answer}\nSpec label: {spec_label}\nSpec options: {options_str}'
  
  # Define model for LLM
  OptionsEnum = Enum('OptionsEnum', {option: option for option in spec_options})
  class CorrectSpec(BaseModel):
    correct_spec: Optional[OptionsEnum] = Field(description="The correct spec from the list of options") # type: ignore
  
  # Define other LLM parameters
  response_model = CorrectSpec
  model = 'gpt-4o-mini'
  temp = 0
  
  # Get LLM response
  llm_response = await get_openai_response_instr(sys_prompt, user_prompt, model, temp, response_model)
  llm_response_dict = llm_response.model_dump(mode='json') if llm_response else None
  correct_spec = llm_response_dict['correct_spec'] if llm_response_dict else None
  
  # Return spec
  spec = {spec_label: {'type': 'options', 'value': correct_spec}} if correct_spec else None
  return spec
  

async def extract_range_spec_from_perplexity_answer(perplexity_answer: str, spec_label: str, spec_units: list):
  units_str = ' / '.join(spec_units)
  
  # Setup LLM prompts
  sys_prompt = 'You are a helpful and meticulous assistant.'
  user_prompt = f'From the statement, identify the value and units of the spec: {spec_label} ({units_str})\n\nStatement: {perplexity_answer}'
  
  # Define model for LLM
  UnitsEnum = Enum('UnitsEnum', {unit.upper(): unit for unit in spec_units})
  class IdentifiedSpec(BaseModel):
    value: Optional[float] = Field(description="The value of the requested specification of the product")
    units: Optional[UnitsEnum] = Field(description="The unit of the requested specification of the product")  # type: ignore
  
  # Define other LLM parameters
  response_model = IdentifiedSpec
  model = 'gpt-4o-mini'
  temp = 0
  
  # Get LLM response
  llm_response = await get_openai_response_instr(sys_prompt, user_prompt, model, temp, response_model)
  llm_response_dict = llm_response.model_dump(mode='json') if llm_response else None
  value = llm_response_dict['value'] if llm_response_dict else None
  units = llm_response_dict['units'] if llm_response_dict else None
  
  # Return spec
  spec = {spec_label: {'type': 'range', 'value': value, 'units': units}} if value is not None else None
  return spec


if __name__ == "__main__":
  from supabase import create_client, Client
  import os
  supabase_url = os.environ['supabase_url']
  supabase_key = os.environ['supabase_service_key']
  supabase: Client = create_client(supabase_url, supabase_key)

  pd_category_id = 1
  product_id = 3941

  # Get pd_category
  pd_category_dict = supabase.table('pd_categories').select('*').eq('id', pd_category_id).execute().data[0]
  # Get product
  product = supabase.table('products').select('*').eq('id', product_id).execute().data[0]

  asyncio.run(check_n_update_specs(product, pd_category_dict))