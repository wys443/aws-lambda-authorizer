# layer-demo

## layer definition
```yaml
HelloWorldLayer:
  Type: AWS::Serverless::LayerVersion
  Properties:
    LayerName: hello-world-dependencies
    Description: Dependencies for hello world app
    ContentUri: common/
    CompatibleRuntimes:
      - python3.9
```
## layer applied to function
```yaml
HelloWorldFunction:
Type: AWS::Serverless::Function
Properties:
  CodeUri: hello_world/
  Handler: app.lambda_handler
  Runtime: python3.9
  Layers:
    - !Ref HelloWorldLayer      # layer reference
  Architectures:
    - x86_64
  Events:
    HelloWorld:
      Type: Api
      Properties:
        Path: /hello
        Method: get
```
## conditionally import common modules
```python
try:
    from common.python import common    # this import is for local development
except ImportError:
    import common                       # this import is available in lambda layer
```
## initialize and activate venv
```bash
python -m venv venv         # creates a virtual environment called venv using venv module
source venv/bin/activate    # activate the venv
```
## use **setup.py** to set up modules
### Note: this facilitates importing local python modules during development
```bash
pip install -e .
```