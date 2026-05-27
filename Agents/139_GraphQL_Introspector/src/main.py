import sys
import requests
import json
import os

def introspect_schema(endpoint):
    """
    Executes a weaponized introspection query to dump the full GraphQL schema.
    Useful for identifying hidden 'delete', 'update', and 'admin' mutations.
    """
    print(f"[*] Initiating Introspection on: {endpoint}")
    
    # Standard GraphQL Introspection Query
    introspection_query = {
        "query": """
        query IntrospectionQuery {
          __schema {
            queryType { name }
            mutationType { name }
            subscriptionType { name }
            types {
              ...FullType
            }
          }
        }

        fragment FullType on __Type {
          kind
          name
          description
          fields(includeDeprecated: true) {
            name
            description
            args {
              ...InputValue
            }
            type {
              ...TypeRef
            }
            isDeprecated
            deprecationReason
          }
          inputFields {
            ...InputValue
          }
          interfaces {
            ...TypeRef
          }
          enumValues(includeDeprecated: true) {
            name
            description
            isDeprecated
            deprecationReason
          }
          possibleTypes {
            ...TypeRef
          }
        }

        fragment InputValue on __InputValue {
          name
          description
          type { ...TypeRef }
          defaultValue
        }

        fragment TypeRef on __Type {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
        """
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Chimera-Sovereign/13.5"
    }

    try:
        response = requests.post(endpoint, json=introspection_query, headers=headers, timeout=10)
        
        if response.status_code == 200:
            schema_data = response.json()
            if "data" in schema_data:
                print("[!] SCHEMA ACQUIRED. Analyzing for administrative nodes...")
                
                # Save raw JSON to loot
                loot_file = os.path.join("..", "loot", f"graphql_schema_{os.getpid()}.json")
                with open(loot_file, "w") as f:
                    json.dump(schema_data, f, indent=2)
                
                # Highlight sensitive mutations
                mutations = schema_data['data']['__schema'].get('mutationType')
                if mutations:
                    print(f"[+] Mutation Type found: {mutations['name']}")
                
                print(f"[+] Full schema dumped to: {loot_file}")
            else:
                print("[-] Introspection disabled or restricted by server.")
        else:
            print(f"[-] Request failed with status: {response.status_code}")
            
    except Exception as e:
        print(f"[-] Execution Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: 126_graphql <api_endpoint_url>")
        sys.exit(1)
    
    introspect_schema(sys.argv[1])
