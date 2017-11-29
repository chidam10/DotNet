1. Copy the p2mpclient.py and p2mpserver.py on desired machines and place the
   input file in the same folder as the p2mpclient.py
2. Run the p2mpserver.py with the port number, output file name and loss 
   probability as command line arguments
   eg: python p2mpserver.py 7735 output.pdf 0.05
3. Run the p2mpclient.py with the destination IP(s), port number, file-name
   and MSS as command line arguments
   eg: python p2mpserver.py 152.1.0.168 152.1.0.169 7735 input.pdf 500

