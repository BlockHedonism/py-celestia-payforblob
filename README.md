# Celestia UI for submitting PayForBlob

Send data to the Celestia Network using your own node and a beautiful UI solution.

To use this solution, you need to run [Celestia Node](https://docs.celestia.org/nodes/light-node/).

## UI overview
https://user-images.githubusercontent.com/110463138/229602395-17ef7580-5522-4db3-9666-4156a56b4834.mp4

## How to install?

1) Install the required dependencies:
```
pip install -r requirements.txt
```
2) Specify in the ```config.py``` in vartiable ```DEFAULT_NODE_URL``` address of the local node
3) Run script:
```
python main.py
```
4) Go to http://127.0.0.1:8000/ and create PayForBlob transaction.
