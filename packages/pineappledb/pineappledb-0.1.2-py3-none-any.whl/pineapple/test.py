from pineapple import pineappledb



def on_success(message):
    print(message)

def on_error(message):
    print(message)
    
    
execute_query_function = pineappledb('kacafix.db', on_success, on_error,run_app=False)
result_json = execute_query_function("SELECT * FROM users;")
print(result_json)  # Print the JSON result of the query



