import yaml

yml_file = 'config.yml'
with open(yml_file) as f:
    parameters = yaml.safe_load(f)

groq_api_key = parameters['groq_api_key']