# IPShifter
Quickly rotate your IP for anonymous bug bounty hunting and secure testing

IPShifter enables quick IP address rotation to enhance anonymity and avoid detection during bug bounty testing. Integrate it with tools like Nuclei and ffuf to maintain privacy while scanning and fuzzing.

Integration Guide
With Nuclei
Install IPShifter: Ensure IPShifter is installed and configured. Follow the installation instructions provided here.

Start IPShifter: Run the tool to begin rotating your IP addresses.

    python3 ipshifter.py
    
Configure Nuclei: Set Nuclei to use the IPShifter proxy. Add the -proxy option to your Nuclei command.

    nuclei -u http://target-url -proxy socks5://127.0.0.1:9050.

Configure ffuf: Set ffuf to use the IPShifter proxy. Add the -proxy option to your ffuf command.

    ffuf -u http://target-url/FUZZ -x socks5://127.0.0.1:9050
