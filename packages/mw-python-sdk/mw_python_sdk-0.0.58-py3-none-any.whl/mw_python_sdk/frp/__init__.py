import os
import stat
import uuid
import requests
import toml
import subprocess

def fast_reverse_proxy(port: int):
    """
    Set up a Fast Reverse Proxy configuration
    
    Args:
        host (str): Local host address
        port (int): Local port to proxy
        
    Returns:
        str: The proxy URL
    """
    # Generate random ID
    random_id = str(uuid.uuid4()).replace('-', '')[:24]
    
    # Set up cache directory
    cache_dir = os.path.expanduser('~/.cache/mw/bin')
    os.makedirs(cache_dir, exist_ok=True)
    
    # Download frpc if not exists
    frpc_path = os.path.join(cache_dir, 'frpc')
    if not os.path.exists(frpc_path):
        response = requests.get('https://heywhale-public.oss-cn-shanghai.aliyuncs.com/frp-0.61.0/frpc')
        with open(frpc_path, 'wb') as f:
            f.write(response.content)
        # Make executable
        os.chmod(frpc_path, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)

    # Create frpc.toml config in the same cache directory
    config_path = os.path.join(cache_dir, 'frpc.toml')
    
    # Create frpc.toml config
    config = {
        'serverAddr': 'klab-frps-service',
        'serverPort': 8080,
        'proxies': [{
            'name': 'web',
            'type': 'http', 
            'localPort': port,
            'customDomains': [f'{random_id}.frp-test.kesci.com']
        }]
    }
    
    with open(config_path, 'w') as f:
        toml.dump(config, f)
    
    # Get the proxy URL
    proxy_url = f'http://{random_id}.frp-test.kesci.com'
    
    # Print the URL
    print(f"FRP proxy URL: {proxy_url}")
    
    # Execute frpc command
    subprocess.Popen([frpc_path, '-c', config_path])
    
    return
    