import json
import boto3, sys
def loot(func):
    c = boto3.client('lambda')
    cfg = c.get_function_configuration(FunctionName=func)
import json
    print(json.dumps(cfg.get('Environment', {}).get('Variables', {}), indent=2))
if __name__ == "__main__":
    if len(sys.argv) < 2: print("Usage: 124_lambda <func_name>"); sys.exit(1)
    loot(sys.argv[1])
